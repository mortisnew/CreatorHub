from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (Community, CreatePost, Comment, ReportComment,
                     Like, Membership, ReportPost, MemberStatus)
from .serialiserz import CommunitySerializer, CreatePostSerializer, ReportPostSerializer, LikeSerializer, \
    MembershipSerializer, ReportCommentSerializer, CommentSerializer
from django.db import transaction

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    @transaction.atomic
    def perform_create(self, serializer):
        community = serializer.save(owner=self.request.user)

        Membership.objects.create(user=self.request.user,
                                  community=community,
                                  role=MemberStatus.ADMIN)


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=True, methods=['patch'])
    def change_role(self, request, pk=None):
        membership = self.get_object()
        role = request.data.get('role')

        if not role and MemberStatus.values:
            raise serializers.ValidationError({'role': 'invalid role.'})
        membership.role = role
        membership.save(update_fields=['role'])
        return Response(MembershipSerializer(membership).data)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreatePostViewSet(viewsets.ModelViewSet):
    queryset = CreatePost.objects.all()
    serializer_class = CreatePostSerializer

    def get_queryset(self):
        return CreatePost.objects.filter(is_allowed=True)


    def perform_create(self, serializer):
        community = serializer.validated_data['community']

        is_owner = self.request.user == community.owner

        is_member = Membership.objects.filter(user=self.request.user,
                                              community=community).exists()

        if not is_owner and not is_member:
            raise serializers.ValidationError({'detail': 'You must be a member of this community to post.'})


        serializer.save(user=self.request.user,
                        is_allowed = not community.required_post_approval)
    
class ReportPostViewSet(viewsets.ModelViewSet):
    queryset = ReportPost.objects.all()
    serializer_class = ReportPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportCommentViewSet(viewsets.ModelViewSet):
    queryset = ReportComment.objects.all()
    serializer_class = ReportCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)