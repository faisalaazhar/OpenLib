from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.blogs, name="blogs"),
    path('addBlog', views.addBlog, name="addBlog"),
    path('updateBlog/<str:id>', views.updateBlog, name="updateBlog"),
    path('deleteBlog/<str:id>', views.deleteBlog, name="deleteBlog"),
    path('search', views.blogSearch, name="blogSearch")
]
