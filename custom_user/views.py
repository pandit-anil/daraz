from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.views import View
from . models import *
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.contrib import auth
import random
from django.contrib.auth import authenticate, login

def generate_otp():
    return random.randint(100000, 999999)





class LogoutView(TemplateView):
    template_name = 'authentication/signup.html'

class Signup(View):
    def get(self, request):
        return render(request,'authentication/signup.html')

    def post(self, request):
        if request.method == "POST":
            data = request.POST
            name = data.get('name')
            username = data.get('username')
            email = data.get('email')
            mobile_number = data.get('mobile')
            password = data.get('password')
            c_password = data.get('confirmPassword')
            
            if User.objects.filter(username = email).exists():
                messages.error(request, "User already Exists")
            if password != c_password:
                messages.error(request,"Password not Matched ")

            if not all ([name,username, email, mobile_number]):
                messages.error(request, "All fields Required")

            if 'image' in request.FILES:
                profile = request.FILES['image']
                user = User.objects.create_user(
                    name = name,
                    mobile_number = mobile_number,
                    username = email,
                    profile_pic = profile,
                    password = password
                )
                print(user)
                user.is_active = False
                user.save()
                
                otp = generate_otp()
                request.session['registration_otp'] = otp
                request.session['user_id'] = user.id

                # Send OTP email
                subject = 'Your OTP Code'
                from_email = '*********@gmail.com'
                recipient_list = [email]
                text_content = f"Your OTP code is {otp}."
                email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
                email.send()

                messages.success(request, 'An OTP has been sent to your email address.')
                return redirect('verify_otp')            
          
        return redirect('signup')
    

class Verify_otp(View):
    def get(self, request):
        return render(request, 'authentication/verify_otp.html')
    
    def post(self, request):
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('registration_otp')
        user_id = request.session.get('user_id')
        if entered_otp == str(stored_otp):
            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
                messages.success(request, 'Your account has been verified successfully.')
                return redirect('login')  # Redirect to login page or wherever you want
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

        return redirect('signup')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully.')
            return redirect('index')  # Redirect to a success page.
        else:
            messages.error(request, 'Invalid email or password.')
        
        return render(request, 'authentication/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')


class ShippingAddressView(View):

    def get(self, request):
        return render(request, 'authentication/address.html')
  
    def post(self, request):
        data = request.POST
        if request.user.is_authenticated:
            dis = data.get('dis')
            address = data.get('add')
            addre = ShippingAddress(user=request.user, district= dis, address =address)
            addre.save()
            return render(request, 'authentication/address.html')
        


