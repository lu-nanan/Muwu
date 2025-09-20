import json
import threading
from collections import deque
from django_redis import get_redis_connection
from django.core.serializers.json import DjangoJSONEncoder


class WordCacheManager:
    """
    Redis单词缓存管理类
    使用Redis存储每个用户的单词缓存，每个缓存最多20个单词
    """

    def __init__(self, user_id):
        """
        初始化缓存管理器

        Args:
            user_id (int): 用户ID，用于创建唯一的缓存键
        """
        self.user_id = user_id
        self.cache_key = f"word_cache:{user_id}"  # Redis键格式
        self.max_size = 10  # 每个用户缓存的最大单词数
        self.redis_conn = get_redis_connection("default")  # 获取Redis连接

        # 初始化缓存结构 (如果不存在)
        if not self.redis_conn.exists(self.cache_key):
            self._init_cache()
        self.print_cache_words()

    def _init_cache(self):
        """
        初始化缓存结构
        创建一个空的缓存队列和字典
        """
        cache_data = {
            'words': [],  # 单词队列，保持学习顺序
            'word_dict': {}  # 单词字典，用于快速查找
        }
        # 使用JSON序列化存储到Redis
        self.redis_conn.set(self.cache_key, json.dumps(cache_data, cls=DjangoJSONEncoder))

    def get_cache(self):
        """
        获取当前缓存数据

        Returns:
            dict: 包含words列表和word_dict字典的缓存数据
        """
        cache_json = self.redis_conn.get(self.cache_key)
        if cache_json:
            return json.loads(cache_json)
        return {'words': [], 'word_dict': {}}

    def update_cache(self, cache_data):
        """
        更新缓存数据到Redis

        Args:
            cache_data (dict): 要更新的缓存数据
        """
        self.redis_conn.set(self.cache_key, json.dumps(cache_data, cls=DjangoJSONEncoder))

    def add_word(self, word_data):
        """
        添加单词到缓存

        Args:
            word_data (dict): 单词数据，必须包含word_id字段

        Returns:
            bool: 添加是否成功
        """
        # 获取当前缓存
        cache_data = self.get_cache()

        # 检查是否已达最大容量
        if len(cache_data['words']) >= self.max_size:
            return False

        # 如果单词已存在，先移除
        if word_data['word_id'] in cache_data['word_dict']:
            self.remove_word(word_data['word_id'])

        # 添加学习状态字段
        word_data.update({
            'current_learning_count': 0,  # 本次学习次数
            'current_correct_count': 0,  # 本次正确次数
            'learning_level': 0  # 本次学习程度
            #'forget_level': 0
        })

        # 添加到缓存
        cache_data['words'].append(word_data)
        cache_data['word_dict'][word_data['word_id']] = word_data

        # 更新缓存
        self.update_cache(cache_data)
        return True

    def remove_word(self, word_id):
        """
        从缓存中移除单词

        Args:
            word_id (int): 要移除的单词ID

        Returns:
            bool: 移除是否成功
        """
        cache_data = self.get_cache()
        if word_id in cache_data['word_dict']:
            # 从字典中移除
            del cache_data['word_dict'][word_id]
            old_words = cache_data['words']
            new_words = []  # 用于存储保留的单词
            # 从列表中移除
            print(f"[remove_word] 开始处理words列表（原长度：{len(old_words)}）")
            for idx, word in enumerate(old_words):
                # 打印当前处理的单词信息（关键：查看word_id是否匹配）
                current_word_id = word['word_id']
                #print(f"  第{idx+1}个单词：current_word_id={current_word_id}（类型：{type(current_word_id)}），目标={target_word_id}（类型：{type(target_word_id)}）")

                # 判断是否保留（不匹配目标word_id则保留）
                if current_word_id != int(word_id):
                    new_words.append(word)
                    print(f"  → 保留（current_word_id != 目标）")
                else:
                    print(f"  → 移除（找到目标word_id）")  # 这行不打印说明没匹配上

            # 更新words列表
            cache_data['words'] = new_words
            print(f"[remove_word] words列表处理完成（新长度：{len(new_words)}）")
            
            # 更新缓存
            self.update_cache(cache_data)
            return True
        return False

    def get_word(self, word_id):
        """
        获取缓存中的特定单词

        Args:
            word_id (int): 单词ID

        Returns:
            dict/None: 单词数据，如果不存在返回None
        """
        cache_data = self.get_cache()
        return cache_data['word_dict'].get(word_id)

    def update_word_learning(self, word_id, feedback):
        """
        更新单词学习状态

        Args:
            word_id (int): 单词ID
            feedback (str): 学习反馈，'familiar'/'vague'/'unfamiliar'

        Returns:
            str: 操作结果 'remove'/'move'/'not_found'
        """
        cache_data = self.get_cache()
        word = cache_data['word_dict'].get(word_id)

        if not word:
            return 'not_found'

        # 更新学习状态
        word['current_learning_count'] += 1

        if feedback == 'familiar':  # 认识
            word['current_correct_count'] += 1
            word['learning_level'] += 1
        else:  # 模糊或不认识
            word['learning_level'] = -1

        # 检查是否需要从缓存中移除
        if word['learning_level'] == 1:
            self.remove_word(word_id)
            return 'remove'
        else:
            # 从原位置移除
            cache_data['words'] = [w for w in cache_data['words'] if w['word_id'] != int(word_id)]
            # 添加到末尾
            cache_data['words'].append(word)
            # 更新字典引用
            cache_data['word_dict'][word_id] = word

            # 更新缓存
            self.update_cache(cache_data)
            return 'move'

    def get_words(self, count):
        """
        获取指定数量的单词

        Args:
            count (int): 要获取的单词数量

        Returns:
            list: 单词数据列表
        """
        cache_data = self.get_cache()
        return cache_data['words'][:min(count, len(cache_data['words']))]

    def is_cache_empty(self):
        """
        检查缓存是否为空

        Returns:
            bool: 缓存是否为空
        """
        cache_data = self.get_cache()
        return len(cache_data['words']) == 0

    def clear_cache(self):
        """
        清空缓存
        """
        self._init_cache()

    def get_cache_size(self):
        """
        获取当前缓存大小

        Returns:
            int: 缓存中的单词数量
        """
        cache_data = self.get_cache()
        return len(cache_data['words'])

    def print_cache_words(self):
        """
        打印缓存中所有单词的详细信息，包括整体状态、words列表和word_dict字典
        """
        cache_data = self.get_cache()
        total_words = len(cache_data['words'])
        total_dict_items = len(cache_data['word_dict'])

        # 1. 打印缓存整体信息（新增word_dict数量统计）
        print("\n" + "=" * 70)
        print(f"[WordCacheManager.print_cache_words] 用户{self.user_id}的单词缓存信息")
        print(f"缓存键: {self.cache_key}")
        print(f"缓存状态: {'空' if total_words == 0 else f'words列表含{total_words}个单词（最大{self.max_size}个）'}")
        print(
            f"word_dict状态: {'空' if total_dict_items == 0 else f'含{total_dict_items}个单词（键为word_id，值为单词数据）'}")
        print("=" * 70)

        # 2. 打印words列表（原有逻辑，保持不变）
        if total_words > 0:
            print("\n" + "-" * 50)
            print(f"📋 words列表（按学习优先级排序）:")
            print(f"{'序号':<5} {'word_id':<10} {'学习次数':<8} {'正确次数':<8} {'学习等级':<8}")
            print("-" * 50)
            for idx, word in enumerate(cache_data['words'], 1):
                # 关键：在print前定义forget_level，用get设置默认值0（避免旧数据缺失字段报错）
                #forget_level = word.get('forget_level', 0)  # 这行必须在print之前，且在循环内部
                print(
                    f"{idx:<5} {word['word_id']:<10} {word['current_learning_count']:<8} "
                    f"{word['current_correct_count']:<8} {word['learning_level']:<8} "
                )
            print("-" * 60)

        # 3. 新增：打印word_dict字典（键为word_id，值为核心单词数据）
        if total_dict_items > 0:
            print("\n" + "-" * 80)
            print(f"📋 word_dict字典（键=word_id，值=核心单词数据）:")
            print("-" * 80)
            # 遍历word_dict的键值对，按word_id排序（可选，让输出更整齐）
            sorted_word_ids = sorted(cache_data['word_dict'].keys())
            for word_id in sorted_word_ids:
                word_data = cache_data['word_dict'][word_id]
                # 打印核心字段（避免冗余，可根据需要调整字段）
                core_info = (
                    f"word_id: {word_data['word_id']:>5}, "
                    f"单词: {word_data.get('word', '未设置'):<10}, "
                    f"学习次数: {word_data['current_learning_count']:>2}, "
                    f"正确次数: {word_data['current_correct_count']:>2}, "
                    f"学习等级: {word_data['learning_level']:>2}, "
                    #f"遗忘分数: {word_data.get['forget_value']:>2}"
                )
                print(f"键: {word_id:<10} | 值: {core_info}")
            print("-" * 80)

        print("\n" + "=" * 70 + "\n")

    def get_all_word_data(self):
        """
        获取缓存中的所有单词数据（用于同步）

        Returns:
            list: 所有单词数据
        """
        cache_data = self.get_cache()
        return cache_data['words']