from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    """用户表模型，继承自Django内置用户模型"""
    email = models.EmailField(max_length=100, unique=True, verbose_name='邮箱')
    password_hash = models.CharField(max_length=255, verbose_name='密码哈希')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user_name = models.CharField(max_length=100, null=True,blank=True, verbose_name='用户名')  # 新增用户名字段

    def __str__(self):
        return self.username
    class Meta:
        db_table = "User"  # 自定义表名


class BaseVocabulary(models.Model):
    """基础词汇表模型"""
    word = models.CharField(max_length=100, unique=True, verbose_name='单词')
    pronunciation = models.CharField(max_length=200, blank=True, null=True, verbose_name='发音')
    definition = models.TextField(verbose_name='释义')
    example_sentence = models.TextField(blank=True, null=True, verbose_name='例句')
    synonyms = models.TextField(blank=True, null=True, verbose_name='近义词')
    confusing_words = models.TextField(blank=True, null=True, verbose_name='易混淆词')  # 新增字段

    def __str__(self):
        return self.word
    class Meta:
        db_table = "BaseVocabulary"  # 自定义表名

class UserWords(models.Model):
    """用户词汇表模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    word = models.ForeignKey(BaseVocabulary, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='关联基础词汇Id')
    familiarity_level = models.IntegerField(default=0, verbose_name='熟悉度等级(0-10)')
    priority_score = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, verbose_name='优先级分数')
    learning_count = models.IntegerField(default=0, verbose_name='学习次数')
    correct_count = models.IntegerField(default=0, verbose_name='正确次数')
    last_reviewed_at = models.DateTimeField(blank=True, null=True, verbose_name='最后复习时间')
    forget_value = models.FloatField(default=0.0, verbose_name='遗忘值')

    # SOURCE_CHOICES = [
    #     ('base_vocab', '基础词汇'),
    #     ('custom', '自定义'),
    #     ('image_recognition', '图片识别'),
    # ]
    # source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='来源')

    def __str__(self):
        return self.custom_word or self.word.word
    class Meta:
        db_table = "UserWords"  # 自定义表名


class ImageRecognitionLogs(models.Model):
    """图片识别记录表模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    image_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片路径')
    recognized_words = models.JSONField(blank=True, null=True, verbose_name='识别出的单词')
    selected_words = models.JSONField(blank=True, null=True, verbose_name='用户选择的单词')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"图片识别记录 #{self.id} - {self.user.username}"
    class Meta:
        db_table = "ImageRecognitionLogs"  # 自定义表名


class DailySentences(models.Model):
    """每日一句表模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    generated_sentence = models.TextField(verbose_name='生成的句子')
    translation = models.TextField(verbose_name='翻译')
    used_words = models.JSONField(blank=True, null=True, verbose_name='使用的单词')
    date = models.DateField(verbose_name='生成日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"每日一句 #{self.id} - {self.user.username} ({self.date})"
    class Meta:
        db_table = "DailySentences"  # 自定义表名

