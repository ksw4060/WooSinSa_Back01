from django.db import models
from user.models import User
from shop.validators import rename_imagefile_to_uuid



# 23년 6월 12일 월요일
# 상품 모델링
class Product(models.Model):
    class Meta:
        db_table = "product"
    PRODUCT_TYPE = [
        ("상의", "상의"),
        ("하의", "하의"),
        ("신발", "신발"),
        ("etc", "기타등등"),
    ]
    product_type = models.CharField("상품 종류", choices=PRODUCT_TYPE, null=False, max_length=30,blank=False)
    product_name = models.CharField("상품 이름", null=False, max_length=100, unique=True)
    product_price = models.PositiveIntegerField("상품 가격", null=False)
    product_info = models.TextField(verbose_name="상품 정보")
    product_registed_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    product_updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 시간")
    product_likes = models.ManyToManyField(
        User, verbose_name="좋아하는 상품", symmetrical=False, related_name='like_products', blank=True
        ) # symmetrical 대칭 여부 False, 유저->상품(O), 상품->유저(X)
    manufacturer = models.CharField("제조사", max_length=30)
    product_img = models.ImageField(
        upload_to=rename_imagefile_to_uuid, verbose_name="상품 이미지", blank=True, null=True
    )

# ---------------- 좋아요 갯수 ------------------
    def count_product_likes(self):
        return self.product_likes.count()

    def __str__(self):
        return str(self.product_name)



class ProductSize(models.Model):
    PRODUCT_TYPE = [
        ("상의", "상의"),
        ("하의", "하의"),
        ("신발", "신발"),
        ("etc", "기타등등"),
    ]
    product_type = models.CharField("사이즈", choices=PRODUCT_TYPE, max_length=50, default="기타등등")
    size_value = models.CharField("사이즈 값", max_length=10, unique=True)

    def __str__(self):
        return str(self.product_type)+" : "+str(self.size_value)


class ProductColor(models.Model):
    color = models.CharField("색상", max_length=50, unique=True)

    def __str__(self):
        return str(self.color)


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    stockquantity = models.PositiveIntegerField("재고수량", default=0)

    def __str__(self):
        return f"{self.product} - {self.size} - {self.color}"

    def decrease_stockquantity(self, stockquantity):
        if self.stockquantity >= stockquantity:
            self.stockquantity -= stockquantity
            self.save()
            return True
        return False



# 23년 6월 12일 월요일
# 구매하든, 안하든 사용자에게 1개이상으로 마음대로 상품에 대한 문의를 할 수 있다.
# 상품 정보랑 연결
class ProductQuestion(models.Model):
    class Meta:
        db_table = "ProductQuestion"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_question"
    )
    product_name = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="question"
    )
    QUESTION_TYPE = [
        ("상품", "상품"),
        ("배송", "배송"),
        ("환불/취소", "환불/취소"),
        ("교환/반품", "교환/반품"),
        ("기타등등", "기타등등"),
    ]
    question_type = models.CharField("상품 문의 종류", choices=QUESTION_TYPE, max_length=50, default="기타등등")
    question_title = models.CharField("상품 문의 제목", null=False, max_length=50)
    question_content = models.TextField(verbose_name="문의 내용")
    is_complete = models.BooleanField("관리자 답변 여부", blank=False, default=False)

    def __str__(self):
        return str(self.question_title)


class QuestionComment(models.Model):
    class Meta:
        db_table = "AdminQuestionComment"

    product_question = models.ForeignKey(
        ProductQuestion, on_delete=models.CASCADE, related_name="product_question"
    )
    comment_title = models.CharField("관리자 댓글 제목", null=False, max_length=50)
    comment_content = models.TextField(verbose_name="관리자 댓글내용")

    def __str__(self):
        return str(self.comment_title)
