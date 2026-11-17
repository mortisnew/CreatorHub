from rest_framework import routers
from django.urls import path,include
from . import views

router = routers.DefaultRouter()
router.register('Community',views.CommunityViewSet)
router.register('membership',views.MembershipViewSet)
router.register('create-post',views.CreatePostViewSet)
router.register('create-comment',views.CommentViewSet)
router.register('like',views.LikeViewSet)
router.register('report-comment',views.ReportCommentViewSet)
router.register('report-post',views.ReportPostViewSet)

urlpatterns = [
    path('',include(router.urls)),
]