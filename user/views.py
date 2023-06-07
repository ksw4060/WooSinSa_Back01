# django.shortcuts 에서 html을 보여주거나, url을 띄워주는 함수 import
# from django.shortcuts import redirect, render
# DRF 에 필요한 함수, 클래스 호출
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
# serializers 호출
from user.serializers import (
    UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer, UserDelSerializer
    )
from user.models import User



# 회원 가입시 토큰 생성
# from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user = serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# ====================== 프로필 상세보기 ================================
class ProfileView(APIView):
    def get_object(self, user_id):
        return get_object_or_404(User, id=user_id)

    # 프로필 상세보기, 권한이 없어도 됨.
    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 프로필 수정, 권한이 있어야함.
    def patch(self, request, user_id):
        user = self.get_object(user_id)
        if user == request.user:
            serializer = UserProfileSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "수정완료!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
    # 이미지 업로드, 교체 가능, 삭제는 없음.

    # 회원 탈퇴 (비밀번호 받아서)
    def delete(self, request, user_id):
        user = self.get_object(user_id)
        datas = request.data.copy()  # request.data → request.data.copy() 변경
        # request.data는 Django의 QueryDict 객체로서 변경이 불가능하여 복사하여 수정한 후 전달하는 방법을 이용!
        datas["is_active"] = False
        serializer = UserDelSerializer(user, data=datas)
        if user.check_password(request.data.get("password")):
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "계정 비활성화 완료"}, status=status.HTTP_204_NO_CONTENT
                )
        else:
            return Response(
                {"message": f"패스워드가 다릅니다"}, status=status.HTTP_400_BAD_REQUEST
                )

# ================================ 프로필 페이지 끝 ================================


# ========================== 팔로우 시작 =====================================
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 팔로우/팔로워 리스트
    def get(self, request, user_id):
        follow = User.objects.filter(id=user_id)
        follow_serializer = FollowSerializer(follow, many=True)
        request_follow = User.objects.filter(id=request.user.id)
        request_follow_serializer = FollowSerializer(request_follow, many=True)
        return Response(
            {
                "follow": follow_serializer.data,
                "request_follow": request_follow_serializer.data,
            }
        )
    # 팔로우 등록/취소
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me.is_authenticated:
            if you != request.user:
                if me in you.followers.all():
                    you.followers.remove(me)
                    return Response("unfollow했습니다.", status=status.HTTP_200_OK)
                else:
                    you.followers.add(me)
                    return Response("follow했습니다.", status=status.HTTP_200_OK)
            else:
                return Response("자신을 팔로우 할 수 없습니다.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("로그인이 필요합니다.", status=status.HTTP_403_FORBIDDEN)

# 로그인 한 유저만 팔로우 할 수 있게 수정함.
# ================================= 팔로우 끝 =================================
