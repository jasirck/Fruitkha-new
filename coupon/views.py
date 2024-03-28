from django.shortcuts import render, redirect
from my_admin.views import admin_required
from login.models import Customer
from my_admin.models import myprodect
from order.models import order
from coupon.models import Coupon
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from cart.models import cart
from django.db.models import Sum


# Create your views here.
@admin_required
def add_coupon(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    print("coupon outside")
    try:
        if request.method == "POST":
            print("coupon inside")
            Coupon_name = request.POST.get("coupon_name")
            code = request.POST.get("code")
            discount = request.POST.get("discount")
            minimum_amount = request.POST.get("minimum")
            start_time = request.POST.get("staring")
            expiration_time = request.POST.get("ending")
            msg = request.POST.get("msg")

            if Coupon.objects.filter(code=code, active=True).exists():
                messages.info(request, "Coupon Exist Take Another")
                return render(
                    request,
                    "add_coupon.html",
                    {"users": count, "pro": count_pro, "ord": order_count},
                )
            Coupon.objects.create(
                coupon_name=Coupon_name,
                code=code,
                discount=discount,
                minimum_amount=minimum_amount,
                start_time=start_time,
                expiration_time=expiration_time,
                msg=msg,
            )
            messages.info(request, "Coupon Created")
            return redirect("coupon")
    except Exception as e:
        messages.info(request, "somthig error!")
        print(e)
        return render(
            request,
            "add_coupon.html",
            {"users": count, "pro": count_pro, "ord": order_count},
        )
    return render(
        request,
        "add_coupon.html",
        {"users": count, "pro": count_pro, "ord": order_count},
    )


@admin_required
def coupon_action(request, id):
    try:
        active = Coupon.objects.get(id=id)
        if active.active:
            active.active = False
        else:
            active.active = True
        active.save()
        return redirect("coupon")
    except Exception as e:
        messages.info(request, "somthing Error")
        print(e)
        return redirect("coupon")


def check_coupon_validity(request):
    if request.method == "POST" and request.is_ajax():
        coupon_code = request.POST.get("coupon_code")
        user = request.user
        user_id = Customer.objects.get(username=user)

        try:
            coupon = Coupon.objects.get(code=coupon_code.strip())
            amount = cart.objects.filter(user_id=user_id.id).aggregate(
                subtotal=Sum("cart_total")
            )
            now = timezone.now()
            start_time = coupon.start_time
            expiration_time = coupon.expiration_time
            if (
                coupon.active
                and coupon.is_expired
                and start_time < now < expiration_time
            ):
                if order.objects.filter(user=user_id, coupon_id=coupon.id).exists():
                    return JsonResponse({"valid": False, "message": "Coupon is Used."})
                elif amount["subtotal"] < coupon.minimum_amount:
                    return JsonResponse(
                        {
                            "valid": False,
                            "message": f"Minimum amount is {coupon.minimum_amount}.",
                        }
                    )
                else:
                    request.session["coupon_code"] = coupon_code
                    return JsonResponse({"valid": True, "message": "Coupon is valid."})
            else:
                return JsonResponse(
                    {"valid": False, "message": "Coupon is either inactive or expired."}
                )
        except Coupon.DoesNotExist:
            return JsonResponse({"valid": False, "message": "Invalid coupon code."})
    else:
        return JsonResponse({"error": "Invalid request"})


def coupon_cancel(request):
    if request.method == "POST" and request.is_ajax():
        del request.session["coupon_code"]
        return JsonResponse({"message": "Coupon Canceled."})
    else:
        return JsonResponse({"error": "Invalid request"})


def coupon_edit(request, id):
    coupon = Coupon.objects.get(id=id)
    print("coupon edit")
    try:
        print("coupon edit")
        if request.method == "POST":
            print("coupon edit")
            Coupon_name = request.POST.get("coupon_name")
            code = request.POST.get("code")
            discount = request.POST.get("discount")
            minimum_amount = request.POST.get("minimum")
            start_time = request.POST.get("staring")
            expiration_time = request.POST.get("ending")
            msg = request.POST.get("msg")
            print(
                Coupon_name, code, discount, minimum_amount, start_time, expiration_time
            )
            if Coupon_name:
                coupon.coupon_name = Coupon_name
            if code:
                coupon.code = code
            if discount:
                coupon.discount = discount
            if minimum_amount:
                coupon.minimum_amount = minimum_amount
            if start_time:
                coupon.start_time = start_time
            if expiration_time:
                coupon.expiration_time = expiration_time
            if msg:
                coupon.msg = msg
            coupon.save()
            messages.info(request, "Coupon Edited")
            return redirect("coupon")

    except Exception as e:
        print(e)
    return render(request, "coupon_edit.html", {"coupon": coupon})
