from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from ToDoList import views

app_name = "ToDoList"

urlpatterns = [
    path("", views.ToDoListView.as_view(), name="list"),
    path("<int:pk>/", views.ToDoInfo.as_view(), name="info"),
    path("create/", views.ToDoCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.ToDoUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.ToDoDelete.as_view(), name="delete"),
    path("comment/create/<int:todolist_pk>/", views.CommentCreate.as_view(), name="comment_create"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)