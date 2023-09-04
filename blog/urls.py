from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('posts/', views.PostListView.as_view(), name='posts'),
]
