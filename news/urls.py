from django.urls import path
from .views import *


urlpatterns = [ 
   path('', AllView.as_view(),name='posts_list'), 
   path('<int:pk>', PostsDetail.as_view(),name='post_detail'),
   path('create/',PostsCreate.as_view(),name='post_create'),
   # path('article/create/',ArticleCreate.as_view(),name='article_create'),
   path('<int:pk>/delete/',PostsDelete.as_view(),name='posts_delete'),
   path('<int:pk>/edit/',PostsUpdate.as_view(),name='post_edit'),
   path('subscribtions/', subscriptions, name='subscriptions'),
   path('categories/', subscriptions, name='category'),

]