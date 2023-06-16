from django.urls import path
from shop import views

# /api/v1/shop/
urlpatterns = [
    # 전체 상품 보기, 상품 게시하기
    path('product/', views.ProductView.as_view(), name='product'),
    # 상품 상세 보기, 수정, 삭제
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),

    # 상품 문의 보기, 작성하기
    path('product/inquery/', views.ProductInqueryView.as_view(), name='inquery'),
    # 상품 문의 수정, 삭제하기
    path('product/inquery/<int:inquery_id>/', views.ProductInqueryDetailView.as_view(), name='inquery_detail'),

    # 상품 문의 댓글 보기, 작성하기
    path('product/inquery/comment/', views.ProductInqueryView.as_view(), name='inquery_comment'),
    # 상품 문의 댓글 수정, 삭제하기
    path('product/inquery/comment/<int:comment_id>/', views.ProductInqueryDetailView.as_view(), name='inquery_comment_detail'),
]
