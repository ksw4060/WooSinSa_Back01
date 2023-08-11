from django.db import models
from user.models import User
from shop.models import Product
from shop.validators import rename_imagefile_to_uuid


class Payment(models.Model):
    pass

class Address(models.Model):
    pass

class Cart(models.Model):
    pass

class Order(models.Model):
    pass

class OrderDetail(models.Model):
    pass


# 23년 6월 12일 월요일
# 상품을 구매한 사용자에게 오직 1개의 상품리뷰를 작성할 수 있는 권한을 부여한다.
# -> 구매내역과 연결
class PurchaseReview(models.Model):
    class Meta:
        db_table = "PurchaseReview"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="review_user"
    )
    product_name = models.ForeignKey(Product, verbose_name="상품 이름", on_delete=models.CASCADE)
    review_title = models.CharField("상품 리뷰 제목", null=False, max_length=50)
    review_content = models.TextField(verbose_name="리뷰 내용")
    review_image = models.ImageField(
        upload_to=rename_imagefile_to_uuid, verbose_name="리뷰 이미지", blank=True, null=True
    )

    def __str__(self):
        return str(self.review_title)
