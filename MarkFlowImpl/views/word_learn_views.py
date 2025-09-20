# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, F, ExpressionWrapper, FloatField
from django.utils import timezone
from datetime import timedelta
from MarkFlowImpl.models import UserWords, BaseVocabulary
from MarkFlowImpl.utils.word_cache_manager import WordCacheManager  # 导入Redis缓存管理器
from MarkFlowImpl.utils.base_vocabulary_serializer import BaseVocabularySerializer
import math
import random


class GetWordsView(APIView):
    """
    单词获取接口
    前端提供userid和获取单词数，后端返回指定数量的单词
    使用Redis缓存管理用户当前学习的单词
    """

    def post(self, request):
        """
        处理单词获取请求
        """

        print("\n" + "=" * 50)
        print(f"[GetWordsView.post] 收到新的单词获取请求，请求数据：{request.data}")
        # 获取请求参数
        user_id = request.data.get('userid')
        print(request.data.get('count'))
        count = request.data.get('count', 10)

        print(user_id, count)
        print(f"[GetWordsView.post] 解析到参数 - user_id: {user_id}, 原始count: {count}")

        # 参数验证
        if not user_id:
            print(f"[GetWordsView.post] 验证失败：缺少userid参数")
            return Response(
                {"success":"False", "error": "userid is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            count = int(count)
            if count <= 0:
                print(f"[GetWordsView.post] 验证失败：count为非正数 ({count})")
                return Response(
                    {"success":"False","error": "count must be a positive integer"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            print(f"[GetWordsView.post] 参数验证通过，有效count: {count}")
        except (ValueError, TypeError):
            print(f"[GetWordsView.post] 验证失败：count不是有效整数 ({count})")
            return Response(
                {"success":"False","error": "count must be a valid integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 初始化Redis缓存管理器
        print(f"[GetWordsView.post] 初始化WordCacheManager，用户ID: {user_id}")
        cache_manager = WordCacheManager(user_id)
        cache_manager.print_cache_words()
        # 检查缓存是否为空
        is_empty = cache_manager.is_cache_empty()
        print(f"[GetWordsView.post] 缓存状态检查：{'为空，准备填充' if is_empty else '不为空'}")
        if is_empty:
            print(f"[GetWordsView.post] 开始首次填充缓存")
            self.fill_cache(user_id, cache_manager)

        # 从缓存获取单词
        print(f"[GetWordsView.post] 尝试从缓存获取{count}个单词")
        cached_words = cache_manager.get_words(count)
        print(f"[GetWordsView.post] 本次从缓存实际获取到{len(cached_words)}个单词")

        # 检查缓存是否充足
        if len(cached_words) < count:
            need_supplement = count - len(cached_words)
            print(f"[GetWordsView.post] 缓存单词不足（差{need_supplement}个），准备补充缓存")
            self.fill_cache(user_id, cache_manager, need_supplement)
            # 补充后再次获取
            cached_words = cache_manager.get_words(count)
            print(f"[GetWordsView.post] 补充缓存后，重新获取到{len(cached_words)}个单词")

        # 返回结果
        print(f"[GetWordsView.post] 请求处理完成，返回{len(cached_words)}个单词")
        print("=" * 50 + "\n")
        return Response({"words": cached_words})

    def fill_cache(self, user_id, cache_manager, count=None):
        """
        填充缓存
        """
        print(f"\n[GetWordsView.fill_cache] 进入填充缓存方法，用户ID: {user_id}")

        # 计算需要填充的数量
        if count is None:
            # 若未指定数量，填充至缓存最大容量
            target_count = cache_manager.max_size - cache_manager.get_cache_size()
            print(
                f"[GetWordsView.fill_cache] 未指定填充数量，自动计算需要填充{target_count}个（缓存当前容量: {cache_manager.get_cache_size()}, 最大容量: {cache_manager.max_size}）")
        else:
            target_count = count
            print(f"[GetWordsView.fill_cache] 指定需要填充{target_count}个单词")

        if target_count <= 0:
            print(f"[GetWordsView.fill_cache] 无需填充（目标数量<=0）")
            return

        # 获取需要学习的单词
        print(f"[GetWordsView.fill_cache] 开始获取{target_count}个用户需要学习的单词")
        words_to_learn = self.get_words_for_user(user_id, target_count)
        print(f"[GetWordsView.fill_cache] 成功获取到{len(words_to_learn)}个待学习单词")

        # 添加到缓存
        added_count = 0
        for idx, word in enumerate(words_to_learn, 1):
            try:
                # 获取单词详细信息
                base_word = BaseVocabulary.objects.get(id=word.word_id)
                word_data = BaseVocabularySerializer(base_word).data
                word_data['word_id'] = word.word_id
                word_data['user_word_id'] = word.id
                word_data['forget_value'] = word.forget_value
                print(word.forget_value)
                print(f"[GetWordsView.fill_cache] 处理第{idx}个单词：word_id={word.word_id}, user_word_id={word.id}")

                # 尝试添加到缓存
                success = cache_manager.add_word(word_data)
                if success:
                    added_count += 1
                    print(f"[GetWordsView.fill_cache] 第{idx}个单词成功添加到缓存")
                else:
                    print(f"[GetWordsView.fill_cache] 第{idx}个单词添加失败（缓存已满）")
                    break  # 缓存已满，停止添加
            except Exception as e:
                print(f"[GetWordsView.fill_cache] 处理第{idx}个单词时出错：{str(e)}")
                continue

        print(f"[GetWordsView.fill_cache] 填充缓存完成，共成功添加{added_count}个单词")

    def get_words_for_user(self, user_id, count):
        """
        根据用户学习情况获取单词
        """
        print(f"\n[GetWordsView.get_words_for_user] 进入获取用户单词方法，用户ID: {user_id}, 需要数量: {count}")

        # 首先获取新加入的单词（学习次数为0）
        print(f"[GetWordsView.get_words_for_user] 尝试获取新单词（learning_count=0）")
        new_words = UserWords.objects.filter(
            user_id=user_id,
            learning_count=0
        )
        new_words_count = new_words.count()
        print(f"[GetWordsView.get_words_for_user] 获取到新单词{new_words_count}个")

        # 检查是否需要补充其他单词
        words_to_learn = []
        if new_words_count < count:
            need_other = count - new_words_count
            print(f"[GetWordsView.get_words_for_user] 新单词不足，需要补充{need_other}个非新单词")

            # 获取非新单词并按优先级降序排列
            other_words = UserWords.objects.filter(
                user_id=user_id,
                learning_count__gt=0
            ).order_by('-priority_score')[:need_other]
            other_words_count = other_words.count()
            print(f"[GetWordsView.get_words_for_user] 获取到非新单词{other_words_count}个（优先级排序）")

            words_to_learn = list(new_words) + list(other_words)
            print(
                f"[GetWordsView.get_words_for_user] 合并后共{len(words_to_learn)}个单词（新单词{new_words_count}+非新单词{other_words_count}）")
        else:
            words_to_learn = list(new_words)
            print(f"[GetWordsView.get_words_for_user] 新单词数量充足，无需补充")

        return words_to_learn


class LearningFeedbackView(APIView):
    """
    单词学习反馈接口
    前端提供用户ID、单词ID和学习情况，后端更新学习状态
    """

    def post(self, request):
        """
        处理学习反馈请求
        """
        print("\n" + "=" * 50)
        print(f"[LearningFeedbackView.post] 收到新的学习反馈请求，请求数据：{request.data}")

        # 获取请求参数
        user_id = request.data.get('userid')
        word_id = str(request.data.get('wordid'))
        feedback = request.data.get('feedback')  # 'familiar', 'vague', 'unfamiliar'
        print(f"[LearningFeedbackView.post] 解析到参数 - user_id: {user_id}, word_id: {word_id}, feedback: {feedback}")

        # 参数验证
        if not user_id or not word_id or not feedback:
            missing = []
            if not user_id:
                missing.append('userid')
            if not word_id:
                missing.append('wordid')
            if not feedback:
                missing.append('feedback')
            print(f"[LearningFeedbackView.post] 参数验证失败：缺少必要参数 {missing}")
            return Response(
                {"success":"False","error": "userid, wordid and feedback are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if feedback not in ['familiar', 'vague', 'unfamiliar']:
            print(
                f"[LearningFeedbackView.post] 参数验证失败：feedback值无效（{feedback}），必须是familiar/vague/unfamiliar")
            return Response(
                {"success":"False","error": "feedback must be 'familiar', 'vague' or 'unfamiliar'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(f"[LearningFeedbackView.post] 参数验证通过，开始处理反馈")

        # 初始化Redis缓存管理器
        print(f"[LearningFeedbackView.post] 初始化WordCacheManager，用户ID: {user_id}")
        cache_manager = WordCacheManager(user_id)
        #cache_manager.print_cache_words()
        # 更新缓存中的单词学习状态
        print(f"[LearningFeedbackView.post] 开始更新缓存中单词（word_id: {word_id}）的学习状态，反馈类型: {feedback}")
        result = cache_manager.update_word_learning(word_id, feedback)
        print(
            f"[LearningFeedbackView.post] 缓存更新结果: {result}（'not_found'=未找到, 'updated'=已更新, 'remove'=已移除）")

        if result == 'not_found':
            print(f"[LearningFeedbackView.post] 缓存中未找到单词（word_id: {word_id}），返回404")
            return Response(
                {"success":"False","error": "Word not found in cache"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 获取用户单词记录
        print(f"[LearningFeedbackView.post] 从数据库查询用户（user_id: {user_id}）的单词记录（word_id: {word_id}）")
        try:
            user_word = UserWords.objects.get(user_id=user_id, word_id=word_id)
            print(
                f"[LearningFeedbackView.post] 找到用户单词记录，当前学习次数: {user_word.learning_count}, 正确次数: {user_word.correct_count}, 当前优先级: {user_word.priority_score}")
        except UserWords.DoesNotExist:
            print(f"[LearningFeedbackView.post] 数据库中未找到用户（user_id: {user_id}）的单词记录（word_id: {word_id}）")
            return Response({"success":"False","error": "Word not found for user"}, status=status.HTTP_404_NOT_FOUND)

        # 更新数据库中的学习数据
        old_learning_count = user_word.learning_count
        user_word.learning_count += 1
        print(f"[LearningFeedbackView.post] 更新学习次数：{old_learning_count} → {user_word.learning_count}")

        if feedback == 'familiar':
            old_correct_count = user_word.correct_count
            user_word.correct_count += 1
            print(
                f"[LearningFeedbackView.post] 反馈为'familiar'，更新正确次数：{old_correct_count} → {user_word.correct_count}")

        # 如果单词从缓存中移除，更新优先级分数
        if result == 'remove':
            print(f"[LearningFeedbackView.post] 单词已从缓存移除，开始重新计算优先级分数")
            old_priority = user_word.priority_score
            user_word.priority_score = self.calculate_priority_score(user_word)
            user_word.last_reviewed_at = timezone.now()
            print(
                f"[LearningFeedbackView.post] 优先级分数更新：{old_priority} → {user_word.priority_score}，最后复习时间更新为：{user_word.last_reviewed_at}")
        cache_manager.print_cache_words()
        # 保存数据库更新
        user_word.save()
        print(f"[LearningFeedbackView.post] 用户单词记录已成功保存到数据库")

        # 返回响应
        response_data = {
            "success":"True",
            "action": result,
            "updated_score": user_word.priority_score
        }
        print(f"[LearningFeedbackView.post] 反馈处理完成，返回数据：{response_data}")
        print("=" * 50 + "\n")
        return Response(response_data)

    def calculate_priority_score(self, user_word):
        """
        计算单词优先级分数
        基于正确率和学习次数计算
        """
        print(
            f"\n[LearningFeedbackView.calculate_priority_score] 开始计算优先级分数 - 学习次数: {user_word.learning_count}, 正确次数: {user_word.correct_count}")

        if user_word.learning_count == 0:
            print(f"[LearningFeedbackView.calculate_priority_score] 学习次数为0，返回最高优先级10.0")
            return 10.0  # 最高优先级

        # 计算正确率
        correctness_rate = user_word.correct_count / user_word.learning_count
        print(
            f"[LearningFeedbackView.calculate_priority_score] 正确率计算：{user_word.correct_count}/{user_word.learning_count} = {correctness_rate:.2f}")

        # 正确率越低，优先级越高
        priority_score = 10 * (1 - correctness_rate)
        priority_score = round(priority_score, 2)
        print(f"[LearningFeedbackView.calculate_priority_score] 计算完成，优先级分数: {priority_score}")

        return priority_score