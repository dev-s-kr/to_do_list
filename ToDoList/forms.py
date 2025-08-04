from ToDoList.models import ToDoList, Comment
from django import forms

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ("title", "description", "start_date", "end_date", "is_completed")
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].input_formats = ["%Y-%m-%d"]
        self.fields["end_date"].input_formats = ["%Y-%m-%d"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", )
        widgets = {
            "content": forms.TextInput(attrs={"class": "form-control"})
        }
        labels = {
            "content": "댓글"
        }