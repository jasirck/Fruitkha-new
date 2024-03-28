from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Customer
from django.contrib.auth import authenticate, login
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import logout

# from my_admin.models import myprodect,AdminCategory
from offer.models import Referral
from wallet.models import Wallet, Wallet_list


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_active:
                # user==Customer.objects.get(username==username)
                user.action = "Login"
                user.save()
                return redirect("homepage")
            else:
                messages.error(request, "Sorry, your account is blocked.")
                return redirect("login_view")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        email_exists = Customer.objects.filter(email=email).exists()

        if email_exists:
            messages.info(request, "Email is taken !")
            return redirect("otp")
        else:
            user_email = email
            otp = random.randrange(100000, 999999)
            time = str(timezone.now())
            email_from = "muhammedjck1@gmail.com"
            subject = "OTP for Login Verification"
            message = "Your One Time Password: " + str(otp)
            if "otp" in request.session:
                del request.session["otp"]
            if "time" in request.session:
                del request.session["time"]
            if "user_email" in request.session:
                del request.session["user_email"]
            request.session["otp"] = otp
            request.session["time"] = time
            request.session["user_email"] = user_email
            send_mail(subject, message, email_from, [email], fail_silently=False)
            return redirect("validation")
    return render(request, "otp.html")


def forgot_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        email_exists = Customer.objects.filter(email=email).exists()
        try:
            if email_exists:
                for_email = email
                fotp = random.randrange(100000, 999999)
                ftime = str(timezone.now())
                email_from = "muhammedjck1@gmail.com"
                subject = "OTP for Login Verification"
                message = "Your One Time Password: " + str(fotp)
                if "fotp" in request.session:
                    del request.session["fotp"]
                if "ftime" in request.session:
                    del request.session["ftime"]
                if "for_email" in request.session:
                    del request.session["for_email"]
                request.session["fotp"] = fotp
                request.session["ftime"] = ftime
                request.session["for_email"] = for_email
                send_mail(subject, message, email_from, [email], fail_silently=False)
                return redirect("forgot_validation")
            else:
                messages.info(request, "Email does not exist")
                return redirect("forgot_otp")
        except:
            messages.info(request, "time out")
            return redirect("forgot_otp")
    return render(request, "forgot_otp.html")


def forgot_validation(request):
    if request.method == "POST":
        fotp = request.session.get("fotp")
        ftime = request.session.get("ftime")
        ftime = datetime.fromisoformat(ftime)

        time_difference = timezone.now() - ftime
        user_otp = request.POST.get("otp")
        if fotp == int(user_otp) and time_difference.total_seconds() <= 60:
            del request.session["fotp"]
            del request.session["ftime"]
            return redirect("new_password")
        else:
            messages.info(request, "OTP not match or time out")
            return redirect("forgot_validation")
    return render(request, "forgot_validation.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        number = request.POST.get("number")
        check_num = number
        number = int(number)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        referral = request.POST.get("referral")
        #  global user_email
        user_email = request.session.get("user_email")
        wal = False
        if password1 == password2 and len(check_num) == 10 and check_num[0] != "0":
            if Customer.objects.filter(username=username).exists():
                messages.info(request, "Username is already taken!")
                return redirect("register")
            if username.strip() == "":
                messages.info(request, "Username is emty!")
                return redirect("register")
            else:
                try:
                    if referral:
                        if Referral.objects.filter(code=referral).exists():
                            wal = True
                            old_user = Referral.objects.get(code=referral)
                            wallet = Wallet.objects.get(user_id=old_user.id)
                            wallet.amount += 200
                            wallet.save()
                            Wallet_list.objects.create(
                                wallet=wallet,
                                is_credit=True,
                                amount=200,
                                msg=f"{username} joined with your referal",
                            )
                        else:
                            messages.info(request, "Refferal is Not Valid !")
                            return redirect("register")
                    user_obj = Customer(
                        first_name=first_name,
                        email=user_email,
                        last_name=last_name,
                        username=username,
                        customer_number=number,
                    )
                    user_obj.set_password(password1)
                    user_obj.save()
                    if wal:
                        new_wallet = Wallet.objects.create(user_id=user_obj, amount=500)
                        new_wallet.save()
                        Wallet_list.objects.create(
                            wallet=new_wallet,
                            is_credit=True,
                            amount=500,
                            msg=f"Your used {old_user.user_id.username} Referral",
                        )
                    del request.session["user_email"]
                    messages.success(request, "User registered")
                    return redirect("login_view")  # Redirect to a success page\
                except Exception as e:
                    messages.info(request, "somthig error!")
                    return redirect("register")
        else:
            messages.info(request, "Passwords do not match or number not exixt")
    return render(request, "register.html")


def validation(request):
    if request.method == "POST":
        # global otp
        otp = request.session.get("otp")
        time = request.session.get("time")
        time = datetime.fromisoformat(time)
        # global time
        time_difference = timezone.now() - time
        user_otp = request.POST.get("otp")
        try:
            if otp == int(user_otp) and time_difference.total_seconds() <= 60:
                del request.session["otp"]
                return redirect("register")
            else:
                if "otp" in request.session:
                    del request.session["oyp"]
                if "time" in request.session:
                    del request.session["time"]
                messages.info(request, "OTP not match or time out")
                return redirect("validation")
        except:
            return render(request, "validation.html")
    return render(request, "validation.html")


def new_password(request):
    if request.method == "POST":
        for_email = request.session.get("for_email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            chenge = Customer.objects.get(email=for_email)
            chenge.set_password(password1)
            chenge.save()
            del request.session["for_email"]
            messages.info(request, "Password change succesfully")
            return redirect("login_view")
        else:
            messages.info(request, "Password not match")
            return redirect("validation")
    return render(request, "new_password.html")


def logout_user(request):
    username = request.user
    user = Customer.objects.get(username=username)
    user.action = "Logout"
    user.save()
    logout(request)
    messages.info(request, "Logout")
    return redirect("login_view")
