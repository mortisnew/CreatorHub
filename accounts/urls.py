from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()


router.register("link",views.CreatorLinkViewSet,"link")
router.register("block",views.BlocklistViewSet,"block")

urlpatterns = [
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('',include(router.urls)),
]