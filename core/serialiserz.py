from rest_framework import serializers
from accounts.serializers import CreatorUserSerializer
from .models import (Tag,Comment,Community,CreatePost,
                     ReportComment,ReportPost,Like,Membership)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name'
        ]

class CommunitySerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True,many=True)
    class Meta:
        model = Community
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'tag',
            'active',
            'required_post_approval',
            'created_at'
        ]
        read_only_fields = ['id','owner','created_at']


class MembershipSerializer(serializers.ModelSerializer):
    community = serializers.PrimaryKeyRelatedField(
        queryset=Community.objects.all()
    )
    user = CreatorUserSerializer(read_only=True)
    class Meta:
        model = Membership
        fields = [
            'id',
            'community',
            'role',
            'user'
        ]
        read_only_fields = ['id', 'user', 'role']

class CreatePostSerializer(serializers.ModelSerializer):
    community = serializers.PrimaryKeyRelatedField(
        queryset=Community.objects.all()
    )
    user = CreatorUserSerializer(read_only=True)
    class Meta:
        model = CreatePost
        fields = [
            'id',
            'user',
            'community',
            'title',
            'content',
            'file',
            'is_allowed',
            'created_at',
            'published_at'
        ]
        read_only_fields = ['id','user','is_allowed',
                            'created_at','published_at']


class CommentSerializer(serializers.ModelSerializer):
    user = CreatorUserSerializer(read_only=True)
    post = (serializers.PrimaryKeyRelatedField
            (queryset=CreatePost.objects.all()))

    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'post',
            'parent',
            'content',
            'created_at'
        ]
        read_only_fields = ['id','user','created_at']
    def validate(self, validated_data):
        parent = validated_data.get('parent')
        post = validated_data.get('post')
        if parent and parent.post_id != post.id:
            raise serializers.ValidationError(
                'Parent comment must belong to the same post'
            )
        return validated_data


class ReportPostSerializer(serializers.ModelSerializer):
    user = CreatorUserSerializer(read_only=True)
    post = (serializers.PrimaryKeyRelatedField
            (queryset=CreatePost.objects.all()))
    class Meta:
        model = ReportPost
        fields = [
            'id',
            'user',
            'post',
            'problem',
            'image',
            'created_at'
        ]
        read_only_fields = ['id','user','created_at']


class ReportCommentSerializer(serializers.ModelSerializer):
    user = CreatorUserSerializer(read_only=True)
    comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all()
    )
    class Meta:
        model = ReportComment
        fields = [
            'id',
            'user',
            'problem',
            'comment',
            'image',
            'created_at'
        ]
        read_only_fields = ['id','user','created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = CreatorUserSerializer(read_only=True)
    post = (serializers.PrimaryKeyRelatedField
            (queryset=CreatePost.objects.all()))
    class Meta:
        model = Like
        fields = [
            'id',
            'user',
            'post',
            'created_at'
        ]
        read_only_fields = ['id','created_at']