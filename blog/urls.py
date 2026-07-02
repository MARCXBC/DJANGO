from django.urls import path
from .views import CreateBlogView, BlogListView, BlogDetailView, UpdateBlogView, DeleteBlogView, MyBlogView


urlpatterns = [
    path("create-blog/", CreateBlogView.as_view()),
    path("",BlogListView.as_view()),
    path("<int:id>/",BlogDetailView.as_view()),
    path("update/<int:id>/",UpdateBlogView.as_view()),
    path("delete/<int:id>/",DeleteBlogView.as_view()),
    path("my-blogs/",MyBlogView.as_view()),
    

]