from rest_framework import serializers


# ============== 상품 후기 시작 ================

class ReviewCreateSerializer(serializers.ModelSerializer):
    pass


class ReviewListserializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return {"username": obj.user.username, "id": obj.user.id, "profile_img": str(obj.user.profile_img)}

    class Meta:
        model = PurchaseReview
        fields = ["id", "title", "user", "hearts"]

# ============== 상품 후기 끝================
