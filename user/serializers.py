
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user.models import User
from django.conf import settings



# 작성자 : 김성우
# 내용 : JWT_Token에 "email, account, username"을 추가하여, 로그인할 때 쓰임
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['account'] = user.account
        token['username'] = user.username
        return token


# 작성자 : 김성우
# 내용 : followings제외하고 시리얼라이저
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("followings",)

    # 회원가입
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    # 회원 정보 수정
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


# 작성자 : 김성우
# 내용 : 유저 상세정보(프로필)
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("account", "username", "age",
                  "email", "profile_img", "gender",
                  "followings","followers",)

    followings = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)

    profile_img = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=False,  # 입력값이 없어도 유효성 검사를 통과
        # allow_null=True,
        # default='default/die1_1.png'
    )

    def clean_img(self):
        img = self.cleaned_data.get('profile_img')
        if img and img.size > 2 * 1024 * 1024:  # 2mb
            raise serializers.ValidationError('이미지 크기는 최대 2mb까지 가능해요.')
        return img



# 작성자 : 김성우
# 내용 : 회원 탈퇴시, is_active값만 체크해준다.
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class UserDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("is_active",)


