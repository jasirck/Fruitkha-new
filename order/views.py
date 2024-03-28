from django.shortcuts import render, redirect
from login.models import Customer, user_address
from my_admin.views import myprodect
from cart.models import cart
from django.db.models import Sum
from order.models import order, order_items
import random
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from wallet.models import Wallet, Wallet_list
from coupon.models import Coupon
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@login_required
def checkout(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj = (
            Customer.objects.filter(username=username)
            .prefetch_related("current_address")
            .first()
        )
        address = user_address.objects.filter(user_id=user_obj.id)
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related(
            "product_id"
        )
        subtotal = cart.objects.filter(user_id=user_obj.id).aggregate(
            subtotal=Sum("cart_total")
        )
        subtotal = (
            subtotal["subtotal"]
            if subtotal["subtotal"] is not None
            else subtotal["subtotal"]
        )
        if subtotal is None:
            return redirect("shop/")
        if subtotal is None:
            shipping = 0
            subtotal = 0  # Set subtotal to 0 if it's None
        elif subtotal > 1000:
            shipping = 0
        else:
            shipping = 40

        total = subtotal + shipping
        log = True
        if Wallet.objects.filter(user_id=user_obj).exists():
            wallet = Wallet.objects.get(user_id=user_obj)
            print("hello waaa")
            t_amout = wallet.amount
        else:
            t_amout = 0.00
        # coupon management
        coupon_discount = 0
        coupon = False
        coupon_code = request.session.get("coupon_code")
        if coupon_code:
            coupon = True
            print(coupon_code)
            coupon_id = Coupon.objects.get(code=coupon_code.strip())
            coupon_discount = subtotal * (coupon_id.discount / 100)
            new_subtotal = subtotal
            new_subtotal -= coupon_discount
            total = new_subtotal + shipping
            # del request.session['coupon_code']
            print("coupon is here")
        else:
            print("coupon is note here")
        # end coupon management
        return render(
            request,
            "checkout.html",
            {
                "coupon": coupon,
                "coupon_discount": coupon_discount,
                "log": log,
                "user": user_obj,
                "cart_obj": cart_obj,
                "subtotal": subtotal,
                "ship": shipping,
                "total": total,
                "address": address,
                "wallet": t_amout,
            },
        )
    return render(request, "login.html")


@login_required
def chenge(request, id):
    if request.user.is_authenticated:
        user_obj = Customer.objects.get(id=id)
        address = user_address.objects.filter(user_id=user_obj.id)
        test = False
        if not address.exists():
            test = True
        print(test)
        if request.method == "POST":
            address = request.POST.get("address")
            add = user_address.objects.get(id=address)
            user_id = Customer.objects.get(id=id)
            user_id.current_address = add
            user_id.save()
            return redirect("checkout")
        print(address)
        return render(
            request,
            "chenge.html",
            {"user": user_obj, "address": address, "test": test, "check": True},
        )
    return render(request, "login.html")


@login_required
def add_address_order(request):
    username = request.user
    user_obj = Customer.objects.get(username=username)

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
            return redirect("checkout")

        else:
            messages.error(request, "address field id null")
            return redirect("add_address_order")
    return render(request, "checkout_add_address.html", {"user": user_obj})


@login_required
def cod_order(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj = (
            Customer.objects.filter(username=username)
            .prefetch_related("current_address")
            .first()
        )
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related(
            "product_id"
        )
        subtotal = cart.objects.filter(user_id=user_obj.id).aggregate(
            subtotal=Sum("cart_total")
        )
        subtotal = (
            subtotal["subtotal"]
            if subtotal["subtotal"] is not None
            else subtotal["subtotal"]
        )
        shipping = 0 if subtotal > 1000 else 40
        total = subtotal + shipping
        # coupun here
        coupon = False
        temp = "fruitkha" + str(random.randint(111111, 999999))
        while order.objects.filter(order_id=temp) is None:
            temp = "fruitkha" + str(random.randint(111111, 999999))
        address_text = f"{user_obj.current_address.name},{user_obj.current_address.call_number},{user_obj.current_address.house_name},{user_obj.current_address.lanmark},{user_obj.current_address.post},{user_obj.current_address.city},{user_obj.current_address.state},{user_obj.current_address.pincode}"
        coupon_code = request.session.get("coupon_code")
        if coupon_code:
            coupon = True
            print(coupon_code)
            coupon_id = Coupon.objects.get(code=coupon_code.strip())
            coupon_discount = subtotal * (coupon_id.discount / 100)
            new_subtotal = subtotal
            new_subtotal -= coupon_discount
            total = new_subtotal + shipping
            # del request.session['coupon_code']
            print("coupon is here")
        else:
            print("coupon is note here")
        if coupon:
            ord = order(
                user=user_obj,
                total_price=total,
                payment_method="COD",
                order_id=temp,
                address=address_text,
                coupon_id=coupon_id,
            )
        else:
            ord = order(
                user=user_obj,
                total_price=total,
                payment_method="COD",
                order_id=temp,
                address=address_text,
            )
        ord.save()
        for i in cart_obj:
            ord_it = order_items(
                order_item=ord,
                product=i.product_id,
                price_now=i.product_id.price,
                quantity_now=i.book_quantity,
            )
            prod = myprodect.objects.get(id=i.product_id.id)
            print(i.product_id.id)
            prod.quantity -= i.book_quantity
            prod.save()
            ord_it.save()
        cart_obj.delete()
        log = True
        return render(
            request, "order_succes.html", {"log": log, "order_id": temp, "total": total}
        )
    return render("shop.html")


@login_required
def razorpaychek(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj = (
            Customer.objects.filter(username=username)
            .prefetch_related("current_address")
            .first()
        )
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related(
            "product_id"
        )
        subtotal = cart.objects.filter(user_id=user_obj.id).aggregate(
            subtotal=Sum("cart_total")
        )
        subtotal = (
            subtotal["subtotal"]
            if subtotal["subtotal"] is not None
            else subtotal["subtotal"]
        )
        shipping = 0 if subtotal > 1000 else 40
        total = subtotal + shipping
        # coupon  here
        print(subtotal)
        temp = "fruitkha" + str(random.randint(111111, 999999))
        while order.objects.filter(order_id=temp) is None:
            temp = "fruitkha" + str(random.randint(111111, 999999))
        print("hello razor pay here")
        coupon_code = request.session.get("coupon_code")
        if coupon_code:
            coupon = True
            print(coupon_code)
            coupon_id = Coupon.objects.get(code=coupon_code.strip())
            coupon_discount = subtotal * (coupon_id.discount / 100)
            new_subtotal = subtotal
            new_subtotal -= coupon_discount
            total = new_subtotal + shipping
            # del request.session['coupon_code']
            print("coupon is here")

        else:
            print("coupon is note here")
        return JsonResponse({"total_price": total, "order_id": temp})
    return render("login")


@login_required
def online_order(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj = (
            Customer.objects.filter(username=username)
            .prefetch_related("current_address")
            .first()
        )
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related(
            "product_id"
        )
        payment_id = request.POST.get("payment_id")
        order_id = request.POST.get("order_id")
        total = request.POST.get("total")
        print(total)
        address_text = f"{user_obj.current_address.name},{user_obj.current_address.call_number},{user_obj.current_address.house_name},{user_obj.current_address.lanmark},{user_obj.current_address.post},{user_obj.current_address.city},{user_obj.current_address.state},{user_obj.current_address.pincode}"
        ord = order(
            user=user_obj,
            total_price=total,
            payment_method="Online",
            order_id=order_id,
            payment_id=payment_id,
            address=address_text,
        )
        coupon_code = request.session.get("coupon_code")
        if coupon_code:
            coupon = True
            print(coupon_code)
            coupon_id = Coupon.objects.get(code=coupon_code.strip())
            ord.coupon_id = coupon_id
            if "coupon_code" in request.session:
                del request.session["coupon_code"]
            print("coupon is here")
            # ord.save()
        else:
            print("coupon is note here")
        ord.save()

        for i in cart_obj:
            ord_it = order_items(
                order_item=ord,
                product=i.product_id,
                price_now=i.current_price,
                quantity_now=i.book_quantity,
            )
            prod = myprodect.objects.get(id=i.product_id.id)
            print(i.product_id.id)
            prod.quantity -= i.book_quantity
            prod.save()
            ord_it.save()
            cart_obj.delete()
        coupon_code = request.session.get("coupon_code")
        if coupon_code:
            coupon = True
            print(coupon_code)
            coupon_id = Coupon.objects.get(code=coupon_code.strip())
            # del request.session['coupon_code']
            print("coupon is here")

        else:
            print("coupon is note here")
        return JsonResponse({"status": "Your Order Placed Succesfully"})
    return redirect("login")


@login_required
def failed_order(request):
    print("inside order failed out of post")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            total = data.get("total")
            csrf_token = data.get("csrfmiddlewaretoken")
            if order.objects.filter(order_id=order_id).exists():
                return JsonResponse({"status": "Order Failed"})
            else:
                # Decode JSON data from request body
                data = json.loads(request.body)

                # Access the data

                username = request.user
                user_obj = (
                    Customer.objects.filter(username=username)
                    .prefetch_related("current_address")
                    .first()
                )
                cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related(
                    "product_id"
                )
                # payment_id = request.POST.get("payment_id")
                # order_id = request.POST.get("order_id")
                # total = request.POST.get("total")
                # print(total)
                address_text = f"{user_obj.current_address.name},{user_obj.current_address.call_number},{user_obj.current_address.house_name},{user_obj.current_address.lanmark},{user_obj.current_address.post},{user_obj.current_address.city},{user_obj.current_address.state},{user_obj.current_address.pincode}"
                ord = order(
                    user=user_obj,
                    total_price=total,
                    payment_method="Failed",
                    order_id=order_id,
                    address=address_text,
                    status="Pending",
                )
                coupon_code = request.session.get("coupon_code")
                if coupon_code:
                    coupon = True
                    print(coupon_code)
                    coupon_id = Coupon.objects.get(code=coupon_code.strip())
                    ord.coupon_id = coupon_id
                if "coupon_code" in request.session:
                    del request.session["coupon_code"]
                    print("coupon is here")
                # ord.save()
                else:
                    print("coupon is note here")
                ord.save()

                for i in cart_obj:
                    ord_it = order_items(
                        order_item=ord,
                        product=i.product_id,
                        price_now=i.current_price,
                        quantity_now=i.book_quantity,
                    )
                    prod = myprodect.objects.get(id=i.product_id.id)
                    print(i.product_id.id)
                    prod.quantity -= i.book_quantity
                    prod.save()
                    ord_it.save()
                    cart_obj.delete()
                coupon_code = request.session.get("coupon_code")
                if coupon_code:
                    coupon = True
                    print(coupon_code)
                    coupon_id = Coupon.objects.get(code=coupon_code.strip())
                    # del request.session['coupon_code']
                    print("coupon is here")

                else:
                    print("coupon is note here")
                # return JsonResponse({"status": "Your Order Placed Succesfully"})
                return JsonResponse({"status": "Order Failed"})
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({"status": "error", "message": "Invalid JSON data"})
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({"status": "error", "message": "Invalid request method"})


@login_required
def wallet_order(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj = (
            Customer.objects.filter(username=username)
            .prefetch_related("current_address")
            .first()
        )
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related(
            "product_id"
        )
        subtotal = cart.objects.filter(user_id=user_obj.id).aggregate(
            subtotal=Sum("cart_total")
        )
        subtotal = (
            subtotal["subtotal"]
            if subtotal["subtotal"] is not None
            else subtotal["subtotal"]
        )
        shipping = 0 if subtotal > 1000 else 40
        total = subtotal + shipping
        # add coupon here
        temp = "fruitkha" + str(random.randint(111111, 999999))
        while order.objects.filter(order_id=temp) is None:
            temp = "fruitkha" + str(random.randint(111111, 999999))
        address_text = f"{user_obj.current_address.name},{user_obj.current_address.call_number},{user_obj.current_address.house_name},{user_obj.current_address.lanmark},{user_obj.current_address.post},{user_obj.current_address.city},{user_obj.current_address.state},{user_obj.current_address.pincode}"
        coupon_code = request.session.get("coupon_code")
        if coupon_code:
            coupon = True
            print(coupon_code)
            coupon_id = Coupon.objects.get(code=coupon_code.strip())
            coupon_discount = subtotal * (coupon_id.discount / 100)
            new_subtotal = subtotal
            new_subtotal -= coupon_discount
            total = new_subtotal + shipping
            # del request.session['coupon_code']
            print("coupon is here")
        else:
            print("coupon is note here")
        ord = order(
            user=user_obj,
            total_price=total,
            payment_method="Wallet",
            order_id=temp,
            address=address_text,
            coupon_id=coupon_id,
        )
        ord.save()
        wallet = Wallet.objects.get(user_id=user_obj)
        print(wallet.amount, total)
        wallet.amount -= total
        print(wallet.amount)
        wallet.save()
        Wallet_list.objects.create(
            wallet=wallet, is_credit=False, amount=total, msg="Purcherce"
        )
        for i in cart_obj:
            ord_it = order_items(
                order_item=ord,
                product=i.product_id,
                price_now=i.product_id.price,
                quantity_now=i.book_quantity,
            )
            prod = myprodect.objects.get(id=i.product_id.id)
            print(i.product_id.id)
            prod.quantity -= i.book_quantity
            prod.save()
            ord_it.save()
        cart_obj.delete()
        log = True
        return render(
            request, "order_succes.html", {"log": log, "order_id": temp, "total": total}
        )
    return render("shop.html")


@login_required
def online_sucess(request):
    return HttpResponse("MyOrder is succesfuly placed")


@login_required
def address_check(request, id, a_id):
    if request.user.is_authenticated:
        user_obj = Customer.objects.get(id=id)
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
            return redirect("checkout")
        return render(
            request, "check_edit_address.html", {"user": user_obj, "address": address}
        )
    return render(request, "login.html")


@login_required
def succes(request):
    log = True
    order_id = request.POST.get("order_id")
    total = request.POST.get("total")
    print(order_id, total)
    return render(
        request, "order_succes.html", {"log": log, "order_id": order_id, "total": total}
    )
