
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user.models import User
from django.conf import settings



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['account'] = user.account
        token['username'] = user.username
        return token

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

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("account", "username", "age",
                  "email", "profile_img", "gender",
                  "followings","followers",
                  "hearted_articles_count", "bookmarked_articles_count")

    followings = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)
    # articles_count = ArticlesSerializer  # 작성한 게시글
    # receive_hearts_count = serializers.SerializerMethodField()  # 받은 좋아요 수
    hearted_articles_count = serializers.SerializerMethodField()  # 내가 하트한 수
    bookmarked_articles_count = serializers.SerializerMethodField()  # 내가 북마크한 수

    profile_img = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=False,  # 입력값이 없어도 유효성 검사를 통과
        # allow_null=True,
        # default='default/die1_1.png'
    )

    def get_hearted_articles_count(self, obj):
        return obj.hearts.count()

    def get_bookmarked_articles_count(self, obj):
        return obj.bookmarks.count()

    def clean_img(self):
        img = self.cleaned_data.get('profile_img')
        if img and img.size > 2 * 1024 * 1024:  # 2mb
            raise serializers.ValidationError('이미지 크기는 최대 2mb까지 가능해요.')
        return img


# 회원탈퇴 serializer
class UserDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("is_active",)


class FollowSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    def get_followings(self, obj):
        followings = obj.followings.all()
        return [
            {
                "nickname": following.nickname,
                "id": following.id,
                "profile_image": self.get_profile_image_url(following.profile_img),
            }
            for following in followings
        ]

    def get_followers(self, obj):
        followers = obj.followers.all()
        return [
            {
                "nickname": follower.nickname,
                "id": follower.id,
                "profile_image": self.get_profile_image_url(follower.profile_img),
            }
            for follower in followers
        ]

    def get_profile_image_url(self, profile_img):
        if profile_img:
            return f"{settings.MEDIA_URL}{profile_img}"
        return None

    class Meta:
        model = User
        fields = ["followings", "followers"]
