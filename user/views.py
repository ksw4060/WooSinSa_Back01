# DRF 에 필요한 함수, 클래스 호출
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# serializers 호출
from user.serializers import (
    UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer
    )
from user.models import User



# 회원 가입시 토큰 생성
# from django.contrib.auth.tokens import PasswordResetTokenGenerator


# 내용 : JWTTOKEN으로 로그인
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 아이디 찾기
class FindUserIDView(APIView):
    def post(self, request):
        account = request.data.get("account")
        if User.objects.filter(account=account).exists():
            user = User.objects.get(account=account)
            if user.login_type == "normal":
                return Response((user.username), status=status.HTTP_200_OK)
            else:
                return Response(("소셜로그인을 이용해주세요"), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "해당 이메일에 일치하는 회원이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST
            )


# 내용 : 회원 탈퇴시, is_active값만 체크해준다.
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
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


# 내용 : 프로필 상세보기, 프로필 수정, 회원 탈퇴
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 이 함수를 실행하면, get_object_or_404를 실행한다.
    def get_object(self, user_id):
        return get_object_or_404(User, id=user_id)

    # 회원 정보 프로필은, 쇼핑몰이기 때문에 자기 자신의 프로필만 볼 수 있도록 해줄 것임
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
                return Response({"message": "프로필 수정이 완료되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다. 내 프로필만 수정 가능해요."}, status=status.HTTP_403_FORBIDDEN)
        # 이미지 업로드, 교체 가능, 삭제는 없음.

    # 회원 탈퇴 (비밀번호 받아서)
    def delete(self, request, user_id):
        user = self.get_object(user_id)
        datas = request.data.copy()  # request.data → request.data.copy() 변경
        # request.data는 Django의 QueryDict 객체로서 변경이 불가능하여 복사하여 수정한 후 전달하는 방법을 이용!
        datas["is_active"] = False
        # 회원 탈퇴 시, 계정을 비활성화 하는 것으로 설정.
        serializer = UserDelSerializer(user, data=datas)
        if user.check_password(request.data.get("password")):
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "계정이 비활성화 되었습니다"}, status=status.HTTP_204_NO_CONTENT
                )
        else:
            return Response(
                {"message": "비밀번호가 다릅니다"}, status=status.HTTP_400_BAD_REQUEST
                )

