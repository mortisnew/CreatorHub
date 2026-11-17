
from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()


router.register("link",views.CreatorLinkViewSet,"link")
router.register("profile",views.ProfileViewSet,"profile")

urlpatterns = [
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path('',include(router.urls)),
]