from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('message', views.message),
    path('destroy', views.destroy),
    path('comment/<int:msg_id>', views.post_comment),
    path('destroy/<int:msg_id>', views.destroy_message),

]