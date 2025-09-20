from rest_framework import serializers
from MarkFlowImpl.models import UserWords, BaseVocabulary
from django.contrib.auth import get_user_model

# 获取User模型（兼容自定义User模型）
User = get_user_model()


# 1. 请求参数验证序列化器（校验前端传入的userid、type、label）
class WordFilterRequestSerializer(serializers.Serializer):
    userid = serializers.IntegerField(
        required=True,
        error_messages={"required": "userid不能为空", "invalid": "userid必须是整数"}
    )
    type = serializers.ChoiceField(
        required=True,
        choices=[("familiar", "熟悉"), ("vague", "模糊"), ("unfamiliar", "不熟悉")],
        error_messages={"required": "type不能为空", "invalid": "type必须是familiar/vague/unfamiliar"}
    )
    label = serializers.BooleanField(
        required=True,
        error_messages={"required": "label不能为空", "invalid": "label必须是true/false"}
    )

    # 自定义校验：确保userid对应的用户存在
    def validate_userid(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"用户ID={value}不存在")
        return value


# 2. 响应数据序列化器（关联BaseVocabulary，返回完整单词信息）
class WordFilterResponseSerializer(serializers.ModelSerializer):
    # 关联BaseVocabulary的基础字段（用source指定关联路径）
    word_text = serializers.CharField(source="word.word", label="单词文本")
    pronunciation = serializers.CharField(
        source="word.pronunciation",
        label="发音",
        allow_null=True,
        allow_blank=True
    )
    definition = serializers.CharField(source="word.definition", label="释义")
    example_sentence = serializers.CharField(
        source="word.example_sentence",
        label="例句",
        allow_null=True,
        allow_blank=True
    )
    synonyms = serializers.CharField(
        source="word.synonyms",
        label="近义词",
        allow_null=True,
        allow_blank=True
    )
    confusing_words = serializers.CharField(
        source="word.confusing_words",
        label="易混淆词",
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = UserWords
        # 返回字段：用户学习数据 + 关联的基础词汇数据
        fields = [
            "id", "word_text", "pronunciation", "definition", "example_sentence",
            "synonyms", "confusing_words", "priority_score", "familiarity_level",
            "learning_count", "correct_count", "last_reviewed_at", "forget_value"
        ]
        read_only_fields = fields  # 所有字段均为只读（仅用于响应）