from django.views.generic import (ListView, DetailView,
CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import PostForm
from .models import Post,Subscription,Category
from datetime import datetime as dt
from django.urls import resolve, reverse_lazy
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from News_paper.settings import DEFAULT_FROM_EMAIL
from django.conf import settings

DEFAULT_FROM_EMAIL=settings.DEFAULT_FROM_EMAIL


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class PostCategory(ListView):
    model=Post
    template_name='category.html'
    context_object_name='posts'
    ordering=['-name']
    paginate_by=10
    def get_queryset(self):
        self.id=resolve(self.request.path_info).kwargs['pk']
        c=Category.objects.get(id=self.id)
        queryset=Post.objects.filter(category=c)
        return queryset
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        category=Category.objects.get(id=self.id)
        sub=category.sub.filter(email=user.email) # type: ignore
        if not sub:
            context['category']=category
        return context
class AllView(ListView):
    model=Post
    ordering='title'
    template_name='posts.html'
    context_object_name='posts'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
class PostsUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'
    

    
class PostsCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        a = form.save(commit=False)
        a.choose = 'news'
        return super().form_valid(form)

class PostsDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post',)
    model=Post
    template_name='posts_delete.html'
    success_url=reverse_lazy('posts_list')

    
class PostsDetail(DetailView):

    model=Post
    template_name='post.html'
    context_object_name='post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = dt.utcnow()
        return context
    
















    