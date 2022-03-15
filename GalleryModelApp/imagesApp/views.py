from django.shortcuts import render
from .models import gallery
from django.http import HttpResponse

# Create your views here.            HttpResponse('hello khaoula vvvv')
def index(request):
    gallerys = gallery.objects.all()[:6]
    return render(request,'imagesApp/index.html',{'gallery':gallerys})
def footer(request):
    return render(request,'imagesApp/footer.html')
def navbar(request):
    return render(request,'imagesApp/navbar.html')
def show_album(request):
    return render(request,'imagesApp/show_album.html')
#def gallery(request):
 #   img = gallery.objects.all()
  #  eturn render(request, 'gallery/gallery.html', {'gallery':img})
