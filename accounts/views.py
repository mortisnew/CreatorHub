from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CreatorUser,CreatorLink
from .serializers import (CreatorLinkSerializer, CreatorUserSerializer,
                          LoginSerializer, ProfileSerializer)

class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        user = CreatorUserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data,status=status.HTTP_201_CREATED)
        return Response(user.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        serialiser = LoginSerializer(data=request.data)
        if serialiser.is_valid():
            user = authenticate(username=serialiser.validated_data['username']
                                  ,password=serialiser.validated_data['password'])
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({
                'detail': 'Incorrect username or password.'},
                status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'detail': 'Invalid username or password.'
        },status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({'detail':'Refresh token is required'},
            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh)
            if str(token['user_id']) != request.user.id:
                return Response({'detail':'invalid refresh token'},
                                status=status.HTTP_400_BAD_REQUEST)
            token.blacklist()
            return Response({'detail':'logout successful'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail':'invalid refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)



class CreatorLinkViewSet(viewsets.ModelViewSet):
    queryset = CreatorLink.objects.all()
    serializer_class = CreatorLinkSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CreatorUser.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['patch'],url_path='edit')
    def edit_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'profile':serializer.data},
                        status=status.HTTP_200_OK)
