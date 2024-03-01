from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields ='__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    owner = ProfileSerializer(many=False)
    reviews = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        result = ReviewSerializer(reviews, many=True)
        return result.data

    def get_total(self, obj):
        result = obj.review_set.all().count()
        return result




