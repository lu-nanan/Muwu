from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Q, F, ExpressionWrapper, FloatField  # 导入复杂查询依赖
from MarkFlowImpl.models import UserWords, BaseVocabulary, User


# 获取User模型（兼容自定义User，注释打开避免冲突）
# User = get_user_model()


class SimpleUserWordFilterAPIView(APIView):
    """
    简化版单词筛选接口（按正确率筛选）
    接收参数：userid（整数）、type（familiar/vague/unfamiliar/all）、label（布尔值）
    筛选逻辑：
    - label=true：按type筛选；label=false：返回空
    - familiar：正确率（correct_count/learning_count）<0.33（仅学习次数>0）
    - vague：学习次数=0 或 正确率0.33~0.66（学习次数>0）
    - unfamiliar：正确率>0.66（仅学习次数>0）
    - all：返回所有关联单词（排除无基础单词的记录）
    """

    def post(self, request):
        print("\n" + "=" * 80)
        print(f"[SimpleUserWordFilterAPIView] 收到新的单词筛选请求，开始处理")
        print("=" * 80)

        # -------------------------- 1. 手动接收请求参数 --------------------------
        print(f"\n[Step 1/5] 开始接收并解析请求参数")
        try:
            request_data = request.data if isinstance(request.data, dict) else request.POST.dict()
            userid = request_data.get("userid")  # 用户ID
            type_filter = request_data.get("type")  # 筛选类型（新增all）
            label_str = request_data.get("label")  # 筛选开关

            # 打印原始参数
            print(f"[Step 1/5] 解析到原始参数：")
            print(f"  - userid（原始）: {userid}")
            print(f"  - type（原始）: {type_filter}")
            print(f"  - label（原始）: {label_str}")
            print(f"[Step 1/5] 参数接收完成，进入校验阶段")

        except Exception as e:
            error_msg = f"[Step 1/5] 参数解析失败：{str(e)}"
            print(error_msg)
            print("=" * 80 + "\n")
            return Response(
                {"success": False, "message": error_msg},
                status=400
            )

        # -------------------------- 2. 手动校验参数合法性 --------------------------
        print(f"\n[Step 2/5] 开始校验参数合法性")
        # 2.1 校验参数是否缺失
        if not all([userid, type_filter, label_str]):
            error_msg = f"[Step 2/5] 参数校验失败：缺失必要参数（需传userid、type、label）"
            print(error_msg)
            print("=" * 80 + "\n")
            return Response(
                {"success": False, "message": error_msg},
                status=400
            )
        print(f"[Step 2/5] 校验1/4（参数缺失）：通过")

        # 2.2 校验userid：必须是整数且用户存在（修复：User.id是整数，转int而非str）
        try:
            userid = int(userid)  # 关键修正：转整数（之前是str，可能导致查询不到用户）
            if not User.objects.filter(id=userid).exists():
                error_msg = f"[Step 2/5] 参数校验失败：用户不存在（userid={userid}）"
                print(error_msg)
                print("=" * 80 + "\n")
                return Response(
                    {"success": False, "message": error_msg},
                    status=400
                )
            print(f"[Step 2/5] 校验2/4（userid合法性）：通过（userid={userid}，用户存在）")
        except ValueError:
            error_msg = f"[Step 2/5] 参数校验失败：userid必须是整数（当前值：{userid}）"
            print(error_msg)
            print("=" * 80 + "\n")
            return Response(
                {"success": False, "message": error_msg},
                status=400
            )

        # 2.3 校验type：新增"all"类型，更新合法列表
        valid_types = ["familiar", "vague", "unfamiliar", "all"]
        if type_filter not in valid_types:
            error_msg = f"[Step 2/5] 参数校验失败：type不合法（当前值：{type_filter}，仅支持{valid_types}）"
            print(error_msg)
            print("=" * 80 + "\n")
            return Response(
                {"success": False, "message": error_msg},
                status=400
            )
        print(f"[Step 2/5] 校验3/4（type合法性）：通过（type={type_filter}）")

        # 2.4 校验label：必须是true/false
        try:
            if isinstance(label_str, str):
                label_str = label_str.lower()
                if label_str not in ["true", "false"]:
                    raise ValueError(f"label字符串值非法：{label_str}")
                label = label_str == "true"
            else:
                label = bool(label_str)
            print(f"[Step 2/5] 校验4/4（label合法性）：通过（原始值：{label_str}，转换后：{label}）")
            print(f"[Step 2/5] 所有参数校验完成，均合法")
        except Exception as e:
            error_msg = f"[Step 2/5] 参数校验失败：label必须是true/false（错误：{str(e)}）"
            print(error_msg)
            print("=" * 80 + "\n")
            return Response(
                {"success": False, "message": error_msg},
                status=400
            )

        # -------------------------- 3. 按条件筛选单词（核心逻辑变更） --------------------------
        print(f"\n[Step 3/5] 开始按条件筛选单词（label={label}）")
        # 3.1 label=false时直接返回空
        if not label:
            print(f"[Step 3/5] 筛选逻辑：label=false，无需筛选，返回空列表")
            print(f"\n[Step 5/5] 请求处理完成（label=false）")
            print("=" * 80 + "\n")
            return Response({
                "success": False,
                "message": "label=false，无需返回单词",
                "data": {"total": 0, "words": []}
            })

        # 3.2 核心：构建正确率筛选条件（处理学习次数=0的特殊情况）
        # 先定义基础条件：用户ID+有基础单词关联
        base_conditions = Q(user_id=userid) & Q(word__isnull=False)
        # 用annotate计算正确率（避免除以零：仅学习次数>0时计算）
        queryset = UserWords.objects.filter(base_conditions).annotate(
            # 计算正确率：correct_count / learning_count（仅learning_count>0有效）
            correct_rate=ExpressionWrapper(
                F('correct_count') / F('learning_count'),
                output_field=FloatField()
            )
        ).select_related("word")  # 关联基础单词，优化查询

        # 根据新需求定义各type的筛选条件
        if type_filter == "familiar":
            # familiar：学习次数>0 且 正确率>0.75
            filter_conditions = Q(learning_count__gt=0) & Q(correct_rate__gt=0.75)
            condition_desc = "学习次数>0 且 正确率（correct_count/learning_count）>0.75"
        elif type_filter == "vague":
            # vague：学习次数=0 或（学习次数>0 且 正确率0.45~0.75）
            filter_conditions = Q(learning_count__exact=0) | (
                    Q(learning_count__gt=0) & Q(correct_rate__gte=0.45) & Q(correct_rate__lte=0.75)
            )
            condition_desc = "学习次数=0 或（学习次数>0 且 正确率0.45≤correct_rate≤0.75）"
        elif type_filter == "unfamiliar":
            # unfamiliar：学习次数>0 且 正确率<0.45
            filter_conditions = Q(learning_count__gt=0) & Q(correct_rate__lt=0.45)
            condition_desc = "学习次数>0 且 正确率（correct_count/learning_count）<0.45"
        else:  # type=all
            filter_conditions = Q()
            condition_desc = "无额外筛选（返回所有关联基础单词的记录）"

        # 执行最终筛选
        print(f"[Step 3/5] 筛选条件：")
        print(f"  - 用户ID：{userid}")
        print(f"  - 筛选类型：{type_filter}")
        print(f"  - 具体条件：{condition_desc}")
        print(f"[Step 3/5] 开始执行数据库查询...")

        try:
            filtered_words = queryset.filter(filter_conditions).order_by(
                "-last_reviewed_at",  # 优先返回最近复习的单词
                "correct_rate"        # 相同复习时间按正确率升序（familiar在前，unfamiliar在后）
            )
            total_count = filtered_words.count()
            print(f"[Step 3/5] 数据库查询完成：共找到{total_count}个符合条件的单词")
        except Exception as e:
            error_msg = f"[Step 3/5] 筛选单词失败（数据库错误）：{str(e)}"
            print(error_msg)
            print("=" * 80 + "\n")
            return Response(
                {"success": False, "message": error_msg},
                status=500
            )

        # -------------------------- 4. 手动构造返回数据（新增正确率字段） --------------------------
        print(f"\n[Step 4/5] 开始构造返回数据（共{total_count}个单词）")
        word_list = []
        for idx, user_word in enumerate(filtered_words, 1):
            base_word = user_word.word
            # 计算显示用的正确率（处理学习次数=0的情况）
            if user_word.learning_count == 0:
                show_correct_rate = "未学习（学习次数=0）"
            else:
                show_correct_rate = round(user_word.correct_rate, 4)  # 保留4位小数

            # 构造单条单词数据（新增正确率字段）
            word_info = {
                # 基础单词字段
                "word_text": base_word.word,
                "pronunciation": base_word.pronunciation or "",
                "definition": base_word.definition,
                "example_sentence": base_word.example_sentence or "",
                "synonyms": base_word.synonyms or "",
                "confusing_words": base_word.confusing_words or "",
                # 用户学习数据字段（新增正确率）
                "user_word_id": user_word.id,
                "learning_count": user_word.learning_count,
                "correct_count": user_word.correct_count,
                "correct_rate": show_correct_rate,  # 新增：显示用的正确率
                "familiarity_level": user_word.familiarity_level,
                "last_reviewed_at": user_word.last_reviewed_at.strftime(
                    "%Y-%m-%d %H:%M:%S") if user_word.last_reviewed_at else "",
                "forget_value": user_word.forget_value ,
                "priority_score": user_word.priority_score,
            }
            word_list.append(word_info)

            # 打印前3个单词的关键信息（便于调试）
            if idx <= 3:
                print(f"  - 第{idx}个单词：word_text={base_word.word}，学习次数={user_word.learning_count}，正确率={show_correct_rate}")

        print(f"[Step 4/5] 返回数据构造完成：共{len(word_list)}个单词（与筛选结果一致）")

        # -------------------------- 5. 返回最终响应 --------------------------
        print(f"\n[Step 5/5] 开始返回响应结果")
        response_data = {
            "success": True,
            "message": f"成功获取{type_filter}类型单词（共{len(word_list)}个）",
            "data": {
                "userid": userid,
                "type": type_filter,
                "total": len(word_list),
                "words": word_list
            }
        }
        print(f"[Step 5/5] 响应内容摘要：")
        print(f"  - 成功状态：{response_data['success']}")
        print(f"  - 单词总数：{response_data['data']['total']}")
        print(f"  - 筛选类型：{response_data['data']['type']}")
        print(f"\n[SimpleUserWordFilterAPIView] 请求处理完成，响应已返回")
        print("=" * 80 + "\n")

        return Response(response_data)