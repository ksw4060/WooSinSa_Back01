from django.contrib import admin
from shop.models import (
    Product, ProductSize, ProductColor, ProductOption, ProductQuestion, QuestionComment
    )




# Register your models here



admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ProductOption)
admin.site.register(ProductQuestion)
admin.site.register(QuestionComment)
