from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from utils.models import TimestampModel

User = get_user_model()

class ToDoList(TimestampModel):
    title = models.CharField("제목", max_length=50)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField("내용")
    start_date = models.DateField("시작일")
    end_date = models.DateField("마감일")
    is_completed = models.BooleanField("완료여부", default=False)

    def __str__(self):
        return self.title[:10]

    def get_absolute_url(self):
        return reverse("ToDoList:info", kwargs={"pk": self.pk})

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