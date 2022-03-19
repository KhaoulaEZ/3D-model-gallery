from django.shortcuts import render
from .models import gallery
from django.http import HttpResponse

# Create your views here.            HttpResponse('hello khaoula vvvv')
def index(request):
    fi = gallery.objects.all()[:6]
    return render(request,'imagesApp/index.html',{'img':fi})
def gallery_all(request):
    return render(request,'imagesApp/index.html',{'img':gallery.objects.all()})
def footer(request):
    return render(request,'imagesApp/footer.html')
def navbar(request):
    return render(request,'imagesApp/navbar.html')
def show_album(request):
    return render(request,'imagesApp/show_album.html')
def about(request):
    return render(request, 'imagesApp/about.html')

#def gallery(request):
 #   img = gallery.objects.all()
  #  eturn render(request, 'gallery/gallery.html', {'gallery':img})
#def createListing(request):
#    title = request.POST["title"]
 #   description = request.POST["description"]
 #   image = request.FILES["image"]
 #   image2 = request.FILES["image2"]
 #   vrmodel = request.FILES["vrmodel"]
  #  if image:
  #      print(image)
 #       listing = gallery.objects.create(
  #          nom=title, description=description,date_pub=timezone.now(),photo=vrmodel, active=True)
  #      listing.save()
   #     return HttpResponseRedirect(reverse("index"))
  #  else:
   #     return HttpResponseRedirect(reverse("createListing"))
   #     return render(request, "auctions/createListing.html")