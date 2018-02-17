from rest_framework import serializers


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255,required=True)
    description = serializers.CharField(max_length=1000,required=True)
    photo = serializers.URLField(max_length=1000,required=True)
    video = serializers.URLField(max_length=1000,required=True)
    video_count = serializers.IntegerField(required=True)
    hour_count = serializers.IntegerField(required=True)
    cost = serializers.IntegerField(required=True)
    advanteges = serializers.StringRelatedField(many=True)
    active = serializers.BooleanField()
