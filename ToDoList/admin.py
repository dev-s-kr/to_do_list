from django.contrib import admin
from ToDoList.models import ToDoList, Comment
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["content", "username"]

@admin.register(ToDoList)
class ToDoListAdmin(SummernoteModelAdmin):
    summernote_fields = ["description", ]
    # list_display = ('title', 'description', 'is_completed', 'start_date', 'end_date')
    # list_filter = ('is_completed',)
    # search_fields = ('title',)
    # ordering = ('start_date',)
    # fieldsets = (
    #     ('Todo Info', {
    #         'fields': ('title', 'description', 'is_completed')
    #     }),
    #     ('Date Range', {
    #         'fields': ('start_date', 'end_date')
    #     }),
    # )
    inlines = [
        CommentInline
    ]