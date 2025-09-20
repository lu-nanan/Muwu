# timing_tasks.py
import json
from django_redis import get_redis_connection
from django.utils import timezone
from MarkFlowImpl.models import UserWords
from MarkFlowImpl.utils.word_cache_manager import WordCacheManager
import threading
import time
from datetime import timedelta


class CacheSyncManager:
    """
    缓存同步管理类
    负责定时将缓存中的单词学习状态同步到数据库
    """

    def __init__(self, sync_interval_minutes=10):
        """
        初始化缓存同步管理器

        Args:
            sync_interval_minutes (int): 同步间隔时间（分钟）
        """
        self.sync_interval = sync_interval_minutes * 60  # 转换为秒
        self.redis_conn = get_redis_connection("default")
        self.is_running = False
        self.thread = None

    def start_sync(self):
        """
        启动定时同步任务
        """
        if self.is_running:
            print("同步任务已经在运行中")
            return

        self.is_running = True
        self.thread = threading.Thread(target=self._sync_loop)
        self.thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        self.thread.start()
        print(f"启动缓存同步任务，间隔: {self.sync_interval / 60} 分钟")

    def stop_sync(self):
        """
        停止定时同步任务
        """
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)  # 等待线程结束，最多等待5秒
        print("缓存同步任务已停止")

    def _sync_loop(self):
        """
        同步循环
        """
        while self.is_running:
            try:
                self.sync_all_caches_to_db()
                # 等待指定的间隔时间
                time.sleep(self.sync_interval)
            except Exception as e:
                print(f"同步任务发生错误: {e}")
                # 发生错误时等待一段时间再重试
                time.sleep(60)

    def sync_all_caches_to_db(self):
        """
        同步所有缓存到数据库
        """
        print(f"[{timezone.now()}] 开始同步所有缓存到数据库")

        # 获取所有缓存键
        cache_keys = self.redis_conn.keys("word_cache:*")
        print(f"找到 {len(cache_keys)} 个用户缓存")

        synced_count = 0
        error_count = 0

        for key in cache_keys:
            try:
                # 从键名中提取用户ID
                user_id = key.decode().split(":")[1]
                success = self.sync_user_cache_to_db(user_id)
                if success:
                    synced_count += 1
                else:
                    error_count += 1
            except Exception as e:
                print(f"同步缓存 {key} 时发生错误: {e}")
                error_count += 1

        print(f"同步完成: 成功 {synced_count}, 失败 {error_count}")

    def sync_user_cache_to_db(self, user_id):
        """
        同步指定用户的缓存到数据库

        Args:
            user_id (int): 用户ID

        Returns:
            bool: 同步是否成功
        """
        try:
            # 初始化缓存管理器
            cache_manager = WordCacheManager(user_id)
            cache_data = cache_manager.get_cache()

            if not cache_data['words']:
                print(f"用户 {user_id} 的缓存为空，无需同步")
                return True

            print(f"开始同步用户 {user_id} 的缓存，包含 {len(cache_data['words'])} 个单词")

            # 同步每个单词的学习状态
            for word_data in cache_data['words']:
                self._sync_word_to_db(user_id, word_data)

            print(f"用户 {user_id} 的缓存同步完成")
            return True

        except Exception as e:
            print(f"同步用户 {user_id} 的缓存时发生错误: {e}")
            return False

    def _sync_word_to_db(self, user_id, word_data):
        """
        同步单个单词的学习状态到数据库

        Args:
            user_id (int): 用户ID
            word_data (dict): 单词数据
        """
        try:
            # 获取用户单词记录
            user_word, created = UserWords.objects.get_or_create(
                user_id=user_id,
                word_id=word_data['word_id'],
                defaults={
                    'familiarity_level': 0,
                    'priority_score': 5.00,
                    'learning_count': 0,
                    'correct_count': 0,
                    'last_reviewed_at': timezone.now()
                }
            )

            # 更新学习数据
            user_word.learning_count += word_data['current_learning_count']
            user_word.correct_count += word_data['current_correct_count']

            # 根据学习等级更新熟悉度
            if word_data['learning_level'] > 0:
                user_word.familiarity_level = min(10, user_word.familiarity_level + 1)
            elif word_data['learning_level'] < 0:
                user_word.familiarity_level = max(0, user_word.familiarity_level - 1)

            # 重新计算优先级分数
            user_word.priority_score = self._calculate_priority_score(user_word)

            # 更新最后复习时间
            user_word.last_reviewed_at = timezone.now()

            user_word.save()

            # 重置缓存中的学习计数（可选）
            # word_data['current_learning_count'] = 0
            # word_data['current_correct_count'] = 0

        except Exception as e:
            print(f"同步单词 {word_data.get('word_id', '未知')} 到数据库时发生错误: {e}")

    def _calculate_priority_score(self, user_word):
        """
        计算优先级分数

        Args:
            user_word (UserWords): 用户单词记录

        Returns:
            float: 优先级分数
        """
        if user_word.learning_count == 0:
            return 10.0  # 最高优先级

        correctness_rate = user_word.correct_count / user_word.learning_count
        # 正确率越低，优先级越高
        priority_score = 10 * (1 - correctness_rate)

        return round(priority_score, 2)

    def set_sync_interval(self, minutes):
        """
        设置同步间隔时间

        Args:
            minutes (int): 同步间隔时间（分钟）
        """
        self.sync_interval = minutes * 60
        print(f"同步间隔已设置为 {minutes} 分钟")