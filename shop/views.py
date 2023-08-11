# rest frame work
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# my app
from shop.serializers import (
    InqueryCreateSerializer, InqueryListserializer, ProductListSerializer,
    ProductCreateSerializer, ProductDetailSerializer, CommentCreateSerializer,
    CommentListserializer
)
from shop.models import (
    Product, ProductInquery, ProductInqueryComment
    )


# Create your views here.
# 23년 6월 12일
# 상품문의모델 : Product
# 시리얼라이저 : ProductListSerializer, ProductCreateSerializer, ProductDetailSerializer
class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all().order_by("-created_at")
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 로그인 된 사용자에 대해서 상품 게시글 작성 가능
    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
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
        product = get_object_or_404(Product, id=product_id)
        if request.user == product.user:
            product.delete()
            return Response({"message": "삭제완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

# 23년 6월 12일, 상품 문의 글 전체 불러오기, 상품 문의 글 작성하기 뷰
# 23년 6월 16일, 비밀글 체크 여부에 따라 문의글을 보여줄 지 말지 결정하도록 수정
# 상품문의모델 : ProductInquery
# 시리얼라이저 : InqueryCreateSerializer, InqueryListserializer
class ProductInqueryView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        inqueries = ProductInquery.objects.all().order_by("-created_at")
        serializer = InqueryListserializer(inqueries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = InqueryCreateSerializer(data=request.data)
        if serializer.is_valid():
            is_private = request.data.get('is_private', False)  # 비밀글 체크 여부 확인
            if is_private:
                serializer.save(user=request.user, is_private=True)
            else:
                serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 생성일 : 23년 6월 12일, 상품 문의 수정 및 삭제 뷰
# 수정일 : 23년 6월 16일, 상품 문의 수정 및 삭제는 작성자와 관리자만 가능
class ProductInqueryDetailView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticated]
    def put(self, request, inquery_id):
        inquery = get_object_or_404(ProductInquery, id=inquery_id)
        if request.user == inquery.user:
            serializer = InqueryCreateSerializer(
                inquery, data=request.data)
            if serializer.is_valid():
                is_private = request.data.get('is_private', False)  # 비밀글 체크 여부 확인
                if is_private:
                    serializer.save(user=request.user, is_private=True)
                else:
                    serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'권한이 없습니다.'}, status.HTTP_403_FORBIDDEN)

    def delete(self, request, inquery_id):
        inquery = get_object_or_404(ProductInquery, id=inquery_id)
        if request.user == inquery.user:
            inquery.delete()
            return Response({"message": "삭제완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)




# 23년 6월 12일 작성
# 23년 6월 13일 수정 및 체크 완료
# 23년 6월 16일 관리자만 댓글을 달 수 있도록 수정
# 상품문의댓글모델 : ProductInqueryComment
# 시리얼라이저 : CommentListserializer, CommentCreateSerializer
class CommentView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]
    # is_staff 가 아닌 경우는 댓글을 달 수 없습니다. 읽기만 가능합니다.
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        comments = product.comments.all().order_by("-created_at")
        serializer = CommentListserializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_staff:  # 관리자인 경우에만 저장
                serializer.save(product=product, user=request.user)
                return Response({"message": "댓글 작성 완료!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "관리자만 댓글을 작성할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 6월 13일 댓글 수정 및 삭제 뷰
# 6월 16일 관리자만 수정, 삭제 가능하도록 수정
class CommentDetailView(APIView):
    # 관리자만 댓글 수정/삭제 가능 - 상품 리뷰, 상품 문의에 대한 답변기능
    permission_classes = [IsAdminUser]
    # 댓글 수정하기
    def put(self, request, comment_id):
        comment = get_object_or_404(ProductInqueryComment, id=comment_id)
        serializer = CommentCreateSerializer(comment, data=request.data)
        if comment.user == request.user:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(({"message": "댓글 수정 완료!"}, serializer.data), status=status.HTTP_200_OK)
        else:
            return Response({"message": "나의 댓글만 수정할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    # 댓글 삭제하기
    def delete(self, request, comment_id):
        comment = get_object_or_404(ProductInqueryComment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response({"message": "댓글 삭제 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "나의 게시물만 삭제할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 23년 6월 12일, 상품 찜하기(좋아요)
# POST : 좋아요 or 취소 , GET : 유저가 좋아요 한 게시글 불러오기
# 상품모델 : Product
# 시리얼라이저 : ProductListSerializer
class ProductLikeView(APIView):
    # 로그인한 사람만 좋아요 가능
    permission_classes = [IsAuthenticated]

    def get_product(self, product_id):
        return get_object_or_404(Product, id=product_id)

    def post(self, request, product_id):
        product = self.get_product(product_id)
        if request.user in product.likes.all():
            product.likes.remove(request.user)
            return Response({"massage":"좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            product.likes.add(request.user)
            return Response({"massage":"좋아요"}, status=status.HTTP_200_OK)
    # 회원 정보 페이지에서 유저가 좋아요 한 게시글만 모두 가져오기
    def get(self, request):
        user = request.user
        products = user.likes.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 23년 6월 16일, 상품 상세 게시글에 좋아요 개수 나타낼 때 쓰는 뷰
# POST : 좋아요 or 취소 , GET : 유저가 좋아요 한 게시글 불러오기
class LikeProductView(APIView):
    # 로그인한 사람만 좋아요 가능
    permission_classes = [IsAuthenticated]

    # 상품 상세 게시글에서 좋아요 개수가 몇개인지 보여준다.
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_like_counts = product.count_likes() # 유저가 좋아요 한 게시글만 모두 가져오기
        return Response({'likes': product_like_counts})
