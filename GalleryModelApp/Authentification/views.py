from django.urls import reverse
from django.db.models import Max
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import  render

from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def index(request):
    #img = gallery.objects.all()[:6]
    return render(request,'imagesApp/index.html',{'img':gallery.objects.all()})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        # print(username,password)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            # print(request.session['user_id'])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "authentication/login.html", {
                "message": "Invalid username and/or password."
            })

    if request.method == "GET":
        return render(request, "authentication/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "authentication/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            request.session['user_id'] = user.id
            print(request.session['user_id'])
            print(" register")

        except IntegrityError as er:
            print(er)
            return render(request, "authentication/register.html", {
                "message": "Username or Email already taken."
            })
        login(request, user)
        return render(request, "authentication/userdetails.html")
    else:
        return render(request, "authentication/register.html")


@login_required
def UserDetailsView(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        card = request.POST["card"]
        userid = request.session.get("user_id")

        print(card, phone, userid)
        try:
            if not luhn_checksum(card):
                user = UserDetails.objects.create(userid=userid, phone=phone, card_number=card)
                user.save()
            else:
                return render(request, "authentication/userdetails.html", {
                    "message": "Card Invalid."
                })

        except IntegrityError as er:
            print(er)
            return render(request, "authentication/userdetails.html", {
                "message": "Username or Phone already taken."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "imagesApp/index.html")

def createListing(request):
        title = request.POST["title"]
        description = request.POST["description"]
        startBid = request.POST["startBid"]
        category = Category.objects.get(id=request.POST["category"])
        user = request.user
        image = request.FILES["image"]
        image2 = request.FILES["image2"]
        vrmodel = request.FILES["vrmodel"]
        if image:
            print(image)
            listing = AuctionListing.objects.create(
                name=title, category=category, date=timezone.now(), startBid=startBid, description=description,
                user=user, image=image, image2=image2, vrmodel=vrmodel, active=True)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("createListing"))
        return render(request, "auctions/createListing.html")