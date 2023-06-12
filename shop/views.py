from django.shortcuts import render
# rest frame work
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
# my app
from shop.serializers import (
    ProductCreateSerializer, ProductListSerializer,
    QuestionCreateSerializer, QuestionListserializer, ProductDeleteSerializer
)
from shop.models import (
    Product, ProductQuestion, AdminComment
    )


# Create your views here.

class ProductView(APIView):
    def get(self, request):
        products =ProductArticle.objects.all().order_by("-created_at")
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(ProductArticle, id=product_id)
        serializer = ProductListSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        product = get_object_or_404(ProductArticle, id=product_id)
        if request.user == product.user:
            serializer = ProductCreateSerializer(
                product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'권한이 없습니다.'}, status.HTTP_403_FORBIDDEN)

    def delete(self, request, product_id):
        product = get_object_or_404(ProductArticle, id=product_id)
        if request.user == product.user:
            serializer = ProductDeleteSerializer(data=request.data)
            return


class PurchaseReview(APIView):
    pass


class CommentView(APIView):
    # 관리자만 댓글 가능 - 상품 리뷰, 상품 문의에 대한 답변기능
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, product_id):
        product = get_object_or_404(Article, id=product_id)
        comments = article.comments.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        product = get_object_or_404(Article, id=product_id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article=article, user=request.user)
            return Response(({"message": "댓글 작성 완료!"}, serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    # 관리자만 댓글 수정/삭제 가능 - 상품 리뷰, 상품 문의에 대한 답변기능
    permission_classes = [permissions.IsAdminUser]
    # 댓글 수정하기
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentCreateSerializer(comment, data=request.data)
        if comment.user == request.user:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(({"message": "댓글 수정 완료!"}, serializer.data), status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    # 댓글 삭제하기
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response({"message": "댓글 삭제 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)


class ProductLikeView(APIView):
    # 로그인한 사람만 좋아요 가능
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(ProductArticle, id=product_id)
        if request.user in product.product_likes.all():
            product.product_likes.remove(request.user)
            return Response({"massage":"좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            product.product_likes.add(request.user)
            return Response({"massage":"좋아요"}, status=status.HTTP_200_OK)
