from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator



# 작성자 : 김성우
# 내용 : 유저 및 슈퍼유저를 생성할 때 매니저
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월8일
class UserManager(BaseUserManager):

    def create_user(self, email, account, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not account:
            raise ValueError('사용자 계정은 필수 입력 사항 입니다.')
        elif not phone:
            raise ValueError('휴대폰 번호는 필수 입력 사항 입니다.')
        elif not email:
            raise ValueError('사용자 이메일은 필수 입력 사항 입니다.')

        user = self.model(
            email=self.normalize_email(email),
            account=account,
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account,  password = None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            account=account,
            password=password,
            **extra_fields
        )
        user.is_admin = True # 슈퍼 유저는 관리자 권한이 있음
        user.save(using=self._db)
        return user



# 작성자 : 김성우
# 내용 : 유저 모델
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class User(AbstractUser):
    # 메타 클래스는, DB 정보들에 대한 정보를 입력하는 곳
    class Meta:
        db_table = "user" # DB 테이블 이름을 user 로 설정해줌

    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True,)
    # Email , account 는 unique 해야 한다.
    account = models.CharField("계정이름", null=False, max_length=50, unique=True)
    username = models.CharField("유저이름", null=False, blank=False, max_length=50)
    age = models.PositiveIntegerField("나이", null=True)
    GENDERS = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('None', '선택하지않음'),
    )
    gender = models.CharField("성별", choices=GENDERS, max_length=10)
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone = models.CharField("휴대폰번호", validators = [phoneNumberRegex], max_length = 11, unique = True)
    # 핸드폰 번호 전용 필드가 있지만, CharField를 사용해서 RegexValidator를 사용하면 휴대폰번호 형식을 입력받을 수 있다.
    profile_img = models.ImageField(
        "프로필 이미지",
        upload_to='users/%Y%m%d',
        blank=True,
    )

    joined_at = models.DateField("계정 생성일", auto_now_add=True)
    is_active = models.BooleanField("활성화 여부", default=True)
    is_staff = models.BooleanField("스태프 여부", default=False)
    is_admin = models.BooleanField("관리자 여부", default=False)
    is_certify = models.BooleanField("폰번호 인증 여부", default=False)

    objects = UserManager()

    USERNAME_FIELD = 'account' # 회원가입시, 계정이름으로 가입하기 때문에, Unique=True 로 해주어야 하는 필드
    REQUIRED_FIELDS = ['email', 'username', "phone",]


    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# 회원
class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    introduce = models.TextField("자기소개", null=True, blank=True)
    # 주문 목록
    # 찜한 상품
    # 나의 구매 후기
    # 최근 본 상품
    # 결제 수단
    # 고객 센터
    # 힐인 쿠폰
    def __str__(self):
        return str(self.user.username)+"의 프로필정보"

