from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth

# Create your views here.


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': "Email n'est pas valide"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email est deja utilisé, veuillez choiser un autre'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': "le nom d'utilisateur ne doit contenir que des caractères alphanumériques"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': "désolé nom d'utilisateur utilisé, choisissez-en un autre"}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password est trés court")
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'id': user.pk,
                    'token': account_activation_token.make_token(user),
                }
                print(email_body)
                link = reverse('activate', kwargs={
                               'uidb64': email_body['id'], 'token': email_body['token']})

                email_subject = 'activer votre compte'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username +
                    ', Please click to the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Votre compte est active')
                return render(request, 'authentication/login.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, id, token):
        # id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        if not account_activation_token.check_token(user, token):
            return redirect('login')

        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html', context={'username': '', 'password': ''})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        context = {'username': username, 'password': ''}
        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Bienvenue ' +
                                     user.username+' ,Vous êtes maintenant connecté')
                    return redirect('visite')
                messages.error(
                    request, "Le compte n'est pas actif, veuillez vérifier votre email")
                return render(request, 'authentication/login.html')
            messages.error(
                request, "Identifiants non valides, réessayez")
            return render(request, 'authentication/login.html', context)

        messages.error(
            request, "Merci de compléter tous les champs")
        return render(request, 'authentication/login.html', context)


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "vous avez été déconnecté")
        return redirect('login')
