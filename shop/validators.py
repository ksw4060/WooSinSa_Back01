from uuid import uuid4
from datetime import date
import os


# 이미지 파일 이름 uuid형식으로 바꾸기
def rename_imagefile_to_uuid(instance, filename):
    now = date.today() # 오늘 날짜 불러오기
    # 업로드 되는 장소
    upload_to = f"product/{now.year}/{now.month}/{now.day}/{instance}"
    ext = filename.split(".")[-1]
    uuid = uuid4().hex

    if instance:
        filename = "{}_{}.{}".format(uuid, instance, ext)
    else:
        filename = "{}.{}".format(uuid, ext)
    return os.path.join(upload_to, filename)
