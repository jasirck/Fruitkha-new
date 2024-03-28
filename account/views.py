from django.shortcuts import render, redirect
from login.models import user_address, Customer
from order.models import order, order_items
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
from my_admin.models import myprodect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from wallet.models import Wallet, Wallet_list
from coupon.models import Coupon
from offer.models import Referral
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa  # Import the library for PDF generation


# Create your views here.


@login_required
def Account(request):
    if request.user.is_authenticated:
        log = True
    else:
        log = False
    username = request.user
    coupon = Coupon.objects.filter(is_expired=True, active=True)
    user_obj = (
        Customer.objects.filter(username=username)
        .prefetch_related("current_address")
        .first()
    )
    address = user_address.objects.filter(user_id=user_obj.id)
    ord = order.objects.filter(user=user_obj.id).order_by("-created")
    count = order.objects.filter(user=user_obj.id).count()
    refer = None
    if Referral.objects.filter(user_id=user_obj.id).exists():
        temp = Referral.objects.get(user_id=user_obj.id)
        refer = temp.code
        print(refer)
    return render(
        request,
        "account.html",
        {
            "user": user_obj,
            "address": address,
            "order": ord,
            "count": count,
            "coupon": coupon,
            "referral": refer,
        },
    )


@login_required
def add_address(request):
    username = request.user
    user_obj = Customer.objects.get(username=username)
    count = order.objects.filter(user=user_obj.id).count()

    if request.method == "POST":
        name = request.POST.get("name")
        call_number = request.POST.get("call_number")
        house_name = request.POST.get("housename")
        lanmark = request.POST.get("lanmark")
        post = request.POST.get("post")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        print("before")
        if (
            "" != name.strip()
            and "" != call_number.strip()
            and "" != house_name.strip()
            and "" != lanmark.strip()
            and "" != post.strip()
            and "" != city.strip()
            and "" != state.strip()
            and "" != pincode.strip()
        ):
            address = user_address(
                user_id=user_obj,
                name=name,
                call_number=call_number,
                house_name=house_name,
                lanmark=lanmark,
                post=post,
                city=city,
                state=state,
                pincode=pincode,
            )
            print("after")
            print(
                address.user_id,
                address.name,
                address.call_number,
                type(address.call_number),
                address.house_name,
                address.lanmark,
                address.post,
                address.city,
                address.pincode,
                address.state,
            )
            address.save()
            return redirect("account")

        else:
            messages.error(request, "address field id null")
            return redirect("add_address")
    return render(
        request, "account_add_address.html", {"user": user_obj, "count": count}
    )


@login_required
def edit_address(request, id, a_id):
    if request.user.is_authenticated:
        log = True
    else:
        log = False
    user_obj = Customer.objects.get(id=id)
    count = order.objects.filter(user=user_obj.id).count()
    address = user_address.objects.get(id=a_id)
    if request.method == "POST":
        address.name = request.POST.get("name")
        address.call_number = request.POST.get("call_number")
        address.house_name = request.POST.get("housename")
        address.lanmark = request.POST.get("lanmark")
        address.post = request.POST.get("post")
        address.city = request.POST.get("city")
        address.state = request.POST.get("state")
        address.pincode = request.POST.get("pincode")
        address.user_id = Customer.objects.get(id=id)
        print("before")
        # address=user_address(user_id=user_id,name=name,call_number=call_number,house_name=house_name,lanmark=lanmark,post=post,city=city,state=state,pincode=pincode)
        print("after")
        print(
            address.user_id,
            address.name,
            address.call_number,
            type(address.call_number),
            address.house_name,
            address.lanmark,
            address.post,
            address.city,
            address.pincode,
            address.state,
        )
        address.save()
        return redirect("account")
    return render(
        request,
        "account_edit_address.html",
        {"user": user_obj, "address": address, "count": count},
    )


@login_required
def delete_address(request, id, a_id):
    address = user_address.objects.get(id=a_id)
    address.delete()
    return redirect("account")


@login_required
def current_address(request, id):
    user_obj = Customer.objects.get(id=id)
    address = user_address.objects.filter(user_id=user_obj.id)
    count = order.objects.filter(user=user_obj.id).count()
    if request.method == "POST":
        address = request.POST.get("address")
        add = user_address.objects.get(id=address)
        user_id = Customer.objects.get(id=id)
        user_id.current_address = add
        user_id.save()
        return redirect("account")
    return render(
        request,
        "current_address.html",
        {"user": user_obj, "address": address, "count": count},
    )


@login_required
def edit_user(request, id):
    user_obj = Customer.objects.get(id=id)
    count = order.objects.filter(user=user_obj.id).count()
    if request.method == "POST":
        print("inside")
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        number = request.POST.get("number")
        if "image" in request.FILES:
            image = request.FILES["image"]
            user_obj.user_dp = image
        if 10 != len(number) or number[1] == "0":
            print("failed")
            return redirect("account")
        user_obj.username = username
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.customer_number
        user_obj.save()
        return redirect("account")
    print("outside")
    return redirect("account")


@login_required
def chenge_password(request):
    if request.method == "POST":
        username = request.user
        user_obj = Customer.objects.get(username=username)
        count = order.objects.filter(user=user_obj.id).count()
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check if the old password matches
        if check_password(old_password, user_obj.password):
            # Check if the new password and confirm password match
            if new_password == confirm_password:
                # Set the new password and save the user object
                user_obj.set_password(new_password)
                user_obj.save()
                messages.success(request, "Password has been changed successfully")
                return redirect("login_view")
            else:
                messages.error(
                    request, "New password and confirm password do not match"
                )
        else:
            messages.error(request, "Old password is incorrect")

    return render(request, "chenge_password.html")


@login_required
def chenge_email(request):
    username = request.user
    user_obj = Customer.objects.get(username=username)
    count = order.objects.filter(user=user_obj.id).count()
    if request.method == "POST":
        email = request.POST.get("email")
        email_exists = Customer.objects.filter(email=email).exists()
        if email_exists:
            messages.info(request, "Email is taken!")
            return redirect("chenge_email")
        else:
            print(email)
            otp = random.randrange(100000, 999999)
            time = timezone.now().isoformat()  # Convert to string representation
            print(time)
            email_from = "muhammedjck1@gmail.com"
            subject = "OTP for Login Verification"
            message = "Your One Time Password: " + str(otp)
            print(otp)
            if "otp" in request.session:
                del request.session["otp"]
            if "time" in request.session:
                del request.session["time"]
            if "email" in request.session:
                del request.session["email"]
            request.session["otp"] = otp
            request.session["time"] = time
            request.session["email"] = email
            send_mail(subject, message, email_from, [email], fail_silently=False)
            return redirect("chenge_email_validation")
    return render(request, "chenge_email.html", {"user": user_obj, "count": count})


@login_required
def chenge_email_validation(request):
    username = request.user
    user_obj = Customer.objects.get(username=username)
    count = order.objects.filter(user=user_obj.id).count()
    if request.method == "POST":
        otp = request.session.get("otp")
        time = request.session.get("time")
        time = datetime.fromisoformat(time)
        email = request.session.get("email")
        now = timezone.now()
        print(timezone.now(), time, "|||", type(timezone.now()), type(time), type(now))
        time_difference = timezone.now() - time
        user_otp = request.POST.get("OTP")
        print(otp, type(otp), "||", user_otp, type(user_otp))
        if int(time_difference.total_seconds()) <= 60:
            if otp == int(user_otp):
                print("success")
                print(email)
                user_obj.email = email
                user_obj.save()
                messages.info(request, "Email chenged")
                return redirect("account")
            else:
                messages.info(request, "OTP not match ")
                return redirect("chenge_email_validation")
        else:
            messages.info(request, "time out")
            return redirect("chenge_email")
    return render(
        request, "chenge_email_validation.html", {"user": user_obj, "count": count}
    )


@login_required
def detail_page(request, id):
    ord = order.objects.get(id=id)

    username = request.user
    user_obj = (
        Customer.objects.filter(username=username)
        .prefetch_related("current_address")
        .first()
    )
    count = order.objects.filter(user=user_obj.id).count()
    products = order_items.objects.filter(order_item=id)
    address = ord.address.split(",")
    if request.method == "POST":
        msg = request.POST.get("msg")
        status = request.POST.get("status")
        ord.msg = msg
        ord.status = status
        ord.save()
        readd = order_items.objects.filter(order_item=ord.id)
        for i in readd:
            temp_id = i.product.id
            temp = myprodect.objects.get(id=temp_id)
            temp.quantity += i.quantity_now
            temp.save()
        if ord.payment_method == "Online":
            print("inside the wallet if")
            if Wallet.objects.filter(user_id=user_obj.id).exists():
                wallet_instance = Wallet.objects.get(user_id=user_obj.id)
                print(type(ord.total_price))
                wallet_instance.amount += ord.total_price
                wallet_instance.save()
                Wallet_list.objects.create(
                    wallet=wallet_instance,
                    is_credit=True,
                    amount=ord.total_price,
                    msg="Order Canceled",
                )
            else:
                new_wallet = Wallet.objects.create(
                    user_id=user_obj, amount=ord.total_price
                )
                Wallet_list.objects.create(
                    wallet=new_wallet,
                    is_credit=True,
                    amount=ord.total_price,
                    msg="Order Canceled",
                )
                return redirect("detail_page", id)
        return render(
            request,
            "detail_page.html",
            {
                "user": user_obj,
                "ord": ord,
                "products": products,
                "address": address,
                "count": count,
            },
        )
    return render(
        request,
        "detail_page.html",
        {
            "user": user_obj,
            "ord": ord,
            "products": products,
            "address": address,
            "count": count,
        },
    )


@login_required
def invoice(request, id):
    ord = order.objects.get(id=id)
    username = request.user
    user_obj = (
        Customer.objects.filter(username=username)
        .prefetch_related("current_address")
        .first()
    )
    count = order.objects.filter(user=user_obj.id).count()
    products = order_items.objects.filter(order_item=id)
    address = ord.address.split(",")
    context = {
        "user": user_obj,
        "ord": ord,
        "products": products,
        "address": address,
        "count": count,
    }
    html_content = render(request, "invoice.html", context).content.decode("utf-8")
    # html_content = render_to_string("invoice.html", context)  # Render the HTML content
    # return HttpResponse(html_content)
    return render(
        request,
        "invoice.html",
        {
            "user": user_obj,
            "ord": ord,
            "products": products,
            "address": address,
            "count": count,
            "html_content": html_content,
            "pdf": True,
        },
    )


@csrf_exempt
def generate_pdf(request):
    print("genoreter pdf")
    html_content = request.POST.get("html_content")
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse("PDF generation error")
    return response


@login_required
def retry_razo(request):
    if request.user.is_authenticated:
        order_id = request.POST.get("order_id")
        ord = order.objects.get(order_id=order_id)
        print("order fail deteil", order_id)
        return JsonResponse({"order_id": order_id, "total_price": ord.total_price})
    return render("login")


@login_required
def retry_succes(request):
    if request.user.is_authenticated:
        payment_id = request.POST.get("payment_id")
        order_id = request.POST.get("order_id")
        total = request.POST.get("total")
        ord = order.objects.get(order_id=order_id)
        ord.payment_id = payment_id
        ord.payment_method = "Online"
        ord.status = "Ordered"
        ord.save()
        return JsonResponse({"status": "Your Order Placed Succesfully"})
    return redirect("login")
