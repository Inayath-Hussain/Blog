from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('my-blogs/', views.listuserblogs, name='list-userblog'),
    path('my-blogs/<int:pk>/', views.detailuserblogs, name='detail-userblog'),
    path('', views.listblogs, name='home'),
    path('<int:pk>/', views.detailblogs, name='detail-blog'),
    path('login/', views.BlogLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.BlogRegistrationView.as_view(), name='register'),
    path('postblog/', views.postblog, name='postblog'),
    path('deleteblog/<int:pk>/', views.deleteblog, name='deleteblog'),
    path('deletecomment/<int:b>/<int:pk>',
         views.deletecomment, name='deletecomment')
]
