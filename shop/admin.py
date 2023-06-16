from django.contrib import admin
from shop.models import (
    Product, ProductSize, ProductColor, ProductOption, ProductInquery, ProductInqueryComment
    )


# Register your models here


admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ProductOption)
admin.site.register(ProductInquery)
admin.site.register(ProductInqueryComment)
