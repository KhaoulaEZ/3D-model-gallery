from  django.urls import path
from . import views


urlpatterns = [
    #path('',views.index,name='index'),
    path('footer',views.footer,name='footer'),
    path('', views.index, name ='index'),
    path('navbar',views.navbar,name='navbar'),
    path('show_album',views.show_album,name='show_album'),

    ]