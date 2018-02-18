from rest_framework import serializers


class FaqSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(max_length=255,required=True)
    answer = serializers.CharField(max_length=1000,required=True)

class ResultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    photo = serializers.URLField(max_length=1000,required=True)
    description = serializers.CharField(max_length=1000,required=True)
    title = serializers.CharField(max_length=50,required=True)