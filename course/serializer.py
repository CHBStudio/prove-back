from rest_framework import serializers


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=1000, required=True)
    photo = serializers.SerializerMethodField('get_mediaphoto')
    video = serializers.SerializerMethodField('get_mediavideo')
    video_count = serializers.IntegerField(required=True)
    hour_count = serializers.IntegerField(required=True)
    cost = serializers.IntegerField(required=True)
    advanteges = serializers.StringRelatedField(many=True)
    active = serializers.BooleanField()
    food = serializers.CharField(required=True)
    extra = serializers.CharField(required=True)


    def get_mediaphoto(self, obj):
        return obj.photo.url[1:]

    def get_mediavideo(self, obj):
        return obj.video.url[1:]


class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    video = serializers.SerializerMethodField('get_mediavideo')
    description = serializers.CharField(max_length=1000, required=True)

    def get_mediavideo(self, obj):
        return obj.video.url[1:]
