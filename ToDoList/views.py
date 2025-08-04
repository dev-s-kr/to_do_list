from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from ToDoList.models import ToDoList, Comment
from ToDoList.forms import ToDoForm, CommentForm
from django.urls import reverse, reverse_lazy


class ToDoListView(LoginRequiredMixin, ListView):
    queryset = ToDoList.objects.all()
    ordering = "end_date"
    template_name = "to_do_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(username=self.request.user)

class ToDoInfo(ListView):
    model = Comment
    # queryset = ToDoList.objects.all().prefetch_related("comment_set", "comment_set__username")
    template_name = "to_do_info.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(ToDoList, pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(ToDoList=self.object).prefetch_related("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["todo"] = self.object
        return context

    # def post(self, *args, **kwargs):
    #     comment_form = CommentForm(self.request.POST)
    #
    #     if not comment_form.is_valid():
    #         self.object = self.get_object()
    #         context = self.get_context_data(object=self.object)
    #         context["comment_form"] = comment_form
    #         return self.render_to_response(context)
    #
    #     if not self.request.user.is_authenticated:
    #         raise Http404
    #
    #     comment = comment_form.save(commit=False)
    #     comment.ToDoList_id = self.kwargs["pk"]
    #     comment.username = self.request.user
    #     comment.save()
    #
    #     return HttpResponseRedirect(reverse_lazy("ToDoList:info", kwargs={"pk": self.kwargs["pk"]}))

class ToDoCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    form_class = ToDoForm
    template_name = "to_do_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("ToDoList:info", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sub_title"] = "작성"
        context["btn_name"] = "생성"
        return context

class ToDoUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoList
    form_class = ToDoForm
    template_name = "to_do_form.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(username=self.request.user)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sub_title"] = "수정"
        context["btn_name"] = "수정"
        return context

class ToDoDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(username=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy("ToDoList:list")

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        todolist = self.get_todolist()
        self.object = form.save(commit=False)
        self.object.username = self.request.user
        self.object.ToDoList = todolist
        self.object.save()
        return HttpResponseRedirect(reverse("ToDoList:info", kwargs={"pk": todolist.pk}))

    def get_todolist(self):
        pk = self.kwargs.get("todolist_pk")
        todolist = get_object_or_404(ToDoList, pk=pk)
        return todolist