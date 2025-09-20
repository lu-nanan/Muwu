# serializers.py
from rest_framework import serializers

from MarkFlowImpl.models import BaseVocabulary


class BaseVocabularySerializer(serializers.ModelSerializer):
    """
    基础词汇序列化器
    用于序列化BaseVocabulary模型
    """
    class Meta:
        model = BaseVocabulary
        fields = '__all__'

class CachedWordSerializer(serializers.Serializer):
    """
    缓存单词序列化器
    用于序列化缓存中的单词数据
    """
    word_id = serializers.IntegerField()
    user_word_id = serializers.IntegerField()
    word = serializers.CharField()
    pronunciation = serializers.CharField()
    definition = serializers.CharField()
    example_sentence = serializers.CharField()
    synonyms = serializers.CharField()
    confusing_words = serializers.CharField()
    current_learning_count = serializers.IntegerField()
    current_correct_count = serializers.IntegerField()
    learning_level = serializers.IntegerField()
    forget_value = serializers.IntegerField()