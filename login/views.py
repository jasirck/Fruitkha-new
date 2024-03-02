from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth import authenticate,login ,logout
import random
from django.core.mail import send_mail
from django.utils import timezone
# from my_admin.models import myprodect,AdminCategory
from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'user:{username}, pass:{password}')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        
        print(user)
        # if user is not None:
        if user is not None:
            
            
            # User is authenticated, login and redirect to the homepage
            login(request, user)
            if user.action == 'allow':
                # Redirect to the homepage if the user is allowed
                return redirect('homepage')
            else:
                # Block user if action is not 'allow'
                messages.error(request, 'Sorry, your account is blocked.')
                return redirect('login_views')
        else:
            # Authentication failed, display error message
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

otp=0
time=0
fotp=0
ftime=0
user_email='' 
# user_obj=

def otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        email_exists = Customer.objects.filter(email=email).exists()
        
        if email_exists:
            messages.info(request, 'Email is taken !')
            return redirect('otp')
        else:
            global otp
            global time
            global user_email
            user_email = email
            print(email)
            otp = random.randrange(100000, 999999)
            time =  timezone.now()
            email_from = 'muhammedjck1@gmail.com'
            subject = 'OTP for Login Verification'
            message = 'Your One Time Password: ' + str(otp)
            print(otp)
            send_mail(subject, message, email_from, [email], fail_silently=False)
            return redirect('validation')
    return render(request, 'otp.html')

for_email=''
def forgot_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        email_exists = Customer.objects.filter(email=email).exists()
        
        if email_exists:
            global fotp
            global for_email
            global ftime
            for_email = email
            fotp = random.randrange(100000, 999999)
            ftime= timezone.now()
            email_from = 'muhammedjck1@gmail.com'
            subject = 'OTP for Login Verification'
            message = 'Your One Time Password: ' + str(fotp)
            print(fotp)
            send_mail(subject, message, email_from, [email], fail_silently=False)
            return redirect('forgot_validation')
        else:
            messages.info(request, 'Email does not exist')
            return redirect('forgot_otp')
    
    return render(request, 'forgot_otp.html')

def forgot_validation(request):
    if request.method == 'POST':
        global fotp
        global ftime
        time_difference = timezone.now() - ftime
        user_otp = request.POST.get('otp')
        print(fotp,'utfydydrykdytdktyd',int(user_otp))
        if fotp == int(user_otp) and time_difference.total_seconds() <= 60 :
            print('success')
            return redirect ('new_password')
        else:
            messages.info(request, 'OTP not match or time out')
            return redirect('forgot_validation')
    return render(request,'forgot_validation.html')


# user_obj=
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        number = request.POST.get('number')
        check_num=number
        number=int(number)
        print(check_num)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        global user_email
        print(user_email)
        if password1 == password2 and len(check_num)==10 and check_num[0]!='0':
            
            if Customer.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken!')
                print('username take!!!!')
                return redirect('register')
            if username.strip() == '':
                messages.info(request, "Username is emty!")
                print('username emty!!!!')
                return redirect('register')
            else:
                 try:
                     print(username,'eleseEeEeEeee')
                     user_obj = Customer(first_name=first_name,email=user_email,last_name=last_name,username=username,customer_number=number)
                     print(type(number))
                     user_obj.set_password(password1)
                     user_obj.save()
                     messages.success(request, 'User registered')
                     return redirect('login_view')  # Redirect to a success page\
                 except Exception as e:
                      messages.info(request, 'somthig error!')
                      print(e)
                      return redirect('register')
        else:
            messages.info(request, 'Passwords do not match or number not exixt')
    return render(request,'register.html')

def validation(request):
    if request.method == 'POST':
        global otp
        global time
        time_difference = timezone.now() - time
        user_otp = request.POST.get('otp')
        print(otp,"||",user_otp)
        try :
            if otp == int(user_otp) and time_difference.total_seconds() <= 60 :
                print('success')
                global for_email
                # user_obj.save()
            
                return redirect ('register')
            else:
                messages.info(request, 'OTP not match or time out')
                return redirect('validation')
        except:
            return render(request,'validation.html')
    return render(request,'validation.html')

def new_password(request):
    if request.method == 'POST':
        global for_email
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(otp,'utfydydrykdytdktyd',for_email)
        if password1== password2:
            print('success')
            chenge=Customer.objects.get(email=for_email)
            print(chenge.password)
            chenge.password=int(password1)
            chenge.save()
            print(password1)
            print(chenge.password)
            return redirect ('login')
        else:
            messages.info(request, 'Password not match')
            return redirect('validation')
    return render(request,'new_password.html')

def logout_user(request):
    logout(request)
    if 'username'in request.session:
        logout(request)
        print('user logout')
        messages.info(request, 'your logout')
        return redirect('login_view')
    else:
        return redirect('homepage')
