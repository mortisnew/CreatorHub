from rest_framework import serializers
from .models import CreatorLink,CreatorUser

class CreatorUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CreatorUser
        fields = ('id',
                  'username',
                  'email',
                  'gender',
                  'age','password','password2')
        extra_kwargs = {'password': {'write_only': True}}

        def validate(self, data):
            if data['password'] != data['password2']:
                raise serializers.ValidationError('Passwords must match.')
            return data

        def create(self, validated_data):
            validated_data.pop('password2')
            password = validated_data.pop('password')
            return CreatorUser.objects.create_user(password=password,
                                                   **validated_data)


class CreatorLinkSerializer(serializers.ModelSerializer):
    creator = CreatorUserSerializer(read_only=True)
    class Meta:
        model = CreatorLink
        fields = ('id',
                  'creator',
                  'link',
                  'title')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    links = CreatorLinkSerializer(many=True)
    class Meta:
        model = CreatorUser
        fields = ('id',
                  'username',
                  'email',
                  'gender',
                  'age',
                  'avatar',
                  'bio',
                  'links')
        read_only_fields = ('id','email')
