from  django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    #path('admin/', admin.site.urls, name='admin' ),
    path('footer',views.footer,name='footer'),
    path('', views.index, name ='index'),
    path('navbar',views.navbar,name='navbar'),
    path('show_album',views.show_album,name='show_album'),
    path('about',views.about,name='about'),
    path('gallery_all',views.gallery_all,name='gallery_all'),
    #path('create',views.createListing,name='createListing'), --- template sup , aprés je va ajouter

    ]