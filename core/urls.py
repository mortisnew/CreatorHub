from rest_framework import routers
from django.urls import path,include
from . import views

router = routers.DefaultRouter()
router.register('Community',views.CommunityViewSet,basename='Community')
router.register('membership',views.MembershipViewSet,basename='membership')
router.register('create-post',views.CreatePostViewSet,basename='create_post')
router.register('create-comment',views.CommentViewSet,basename='create_comment')
router.register('like',views.LikeViewSet,basename='like')
router.register('report-comment',views.ReportCommentViewSet,basename='report_comment')
router.register('report-post',views.ReportPostViewSet,basename='report_post')
router.register('bookmark',views.BookmarkViewSet,basename='bookmark')
router.register('tag',views.TagViewSet,basename='tag')

urlpatterns = [
    path('',include(router.urls)),
]