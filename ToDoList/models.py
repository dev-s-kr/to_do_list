from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from utils.models import TimestampModel
from PIL import Image
from pathlib import Path

User = get_user_model()

class ToDoList(TimestampModel):
    title = models.CharField("제목", max_length=50)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField("내용")
    image = models.ImageField("이미지", null=True, blank=True, upload_to="ToDoList/%Y/%m/%d")
    thumbnail = models.ImageField("썸네일", null=True, blank=True, upload_to="ToDoList/%Y/%m/%d/thumbnail")
    start_date = models.DateField("시작일")
    end_date = models.DateField("마감일")
    is_completed = models.BooleanField("완료여부", default=False)

    def __str__(self):
        return self.title[:10]

    def get_absolute_url(self):
        return reverse("ToDoList:info", kwargs={"pk": self.pk})

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)
        image = Image.open(self.image)
        image.thumbnail((300, 300))
        image_path = Path(self.image.name)
        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix.lower()
        thumbnail_filename = f"{thumbnail_name}_thumb{thumbnail_extension}"
        if thumbnail_extension in [".jpg", ".jpeg"]:
            file_type = "JPEG"
        elif thumbnail_extension == [".gif"]:
            file_type = "GIF"
        elif thumbnail_extension == [".png"]:
            file_type = "PNG"
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "할 일"
        verbose_name_plural = "할 일 목록"

class Comment(TimestampModel):
    ToDoList = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    content = models.CharField("내용", max_length=255)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ToDoList.title} 댓글"

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ['-created_at']