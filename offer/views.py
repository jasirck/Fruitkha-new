from django.shortcuts import render, redirect
from my_admin.views import admin_required
from my_admin.models import myprodect, AdminCategory
from login.models import Customer
from order.models import order
from django.contrib import messages
from offer.models import Product_Offer, Category_Offer, Referral
from django.contrib.auth.decorators import login_required
import random


# Create your views here.


@admin_required
def add_product_offer(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    product_all = myprodect.objects.all()
    print("Offer outside")
    try:
        if request.method == "POST":
            print("product offer inside")
            product = request.POST.get("product")
            discount = request.POST.get("discount")
            start_time = request.POST.get("staring")
            expiration_time = request.POST.get("ending")
            if Product_Offer.objects.filter(produc_id=product).exists():
                messages.info(request, "Offer Exists")
                return render(
                    request,
                    "add_product_offer.html",
                    {
                        "product": product_all,
                        "users": count,
                        "pro": count_pro,
                        "ord": order_count,
                    },
                )  #
            product_id = myprodect.objects.get(id=product)
            Product_Offer.objects.create(
                produc_id=product_id,
                percentage=discount,
                start_date=start_time,
                end_date=expiration_time,
            )
            messages.info(request, "Offer Created")
            return render(
                request,
                "add_product_offer.html",
                {
                    "product": product_all,
                    "users": count,
                    "pro": count_pro,
                    "ord": order_count,
                },
            )  #
    except Exception as e:
        messages.info(request, "somthig error!")
        print(e)
        return render(
            request,
            "add_product_offer.html",
            {
                "product": product_all,
                "users": count,
                "pro": count_pro,
                "ord": order_count,
            },
        )
    return render(
        request,
        "add_product_offer.html",
        {"product": product_all, "users": count, "pro": count_pro, "ord": order_count},
    )


@admin_required
def product_offer(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    # product_all = myprodect.objects.all()
    offer = Product_Offer.objects.all().order_by("id")

    return render(
        request,
        "product_offer.html",
        {"offer": offer, "users": count, "pro": count_pro, "ord": order_count},
    )


@admin_required
def product_offer_action(request, id):
    try:
        active = Product_Offer.objects.get(id=id)
        if active.is_active:
            active.is_active = False
        else:
            active.is_active = True
        active.save()
        return redirect("product_offer")
    except Exception as e:
        messages.info(request, "somthing Error")
        print(e)
        return redirect("product_offer")


@admin_required
def edit_product_offer(request, id):
    all = Product_Offer.objects.get(id=id)
    try:
        if request.method == "POST":
            print("product offer inside")
            discount = request.POST.get("discount")
            start_time = request.POST.get("staring")
            expiration_time = request.POST.get("ending")
            product = Product_Offer.objects.get(id=id)
            if discount:
                product.percentage = discount
            if start_time:
                product.start_date = start_time
            if expiration_time:
                product.end_date = expiration_time
            product.save()
            messages.info(request, "Offer edited")
            return redirect("product_offer")  #
    except Exception as e:
        messages.info(request, "somthig error!")
        print(e)
        return render(request, "edit_product_offer.html", {"all": all})
    return render(request, "edit_product_offer.html", {"all": all})


# @admin_required
def add_category_offer(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    category_all = AdminCategory.objects.all()
    print("Offer outside")
    try:
        if request.method == "POST":
            print("Category offer inside")
            category = request.POST.get("category")
            discount = request.POST.get("discount")
            start_time = request.POST.get("staring")
            expiration_time = request.POST.get("ending")
            if Category_Offer.objects.filter(category_id=category).exists():
                messages.info(request, "Offer Exists")
                return render(
                    request,
                    "add_product_offer.html",
                    {
                        "category": category_all,
                        "users": count,
                        "pro": count_pro,
                        "ord": order_count,
                    },
                )  #
            category_id = AdminCategory.objects.get(id=category)
            Category_Offer.objects.create(
                category_id=category_id,
                percentage=discount,
                start_date=start_time,
                end_date=expiration_time,
            )
            messages.info(request, "Offer Created")
            return redirect("category_offer")  #
    except Exception as e:
        messages.info(request, "somthig error!")
        print(e)
        return render(
            request,
            "add_category_offer.html",
            {
                "category": category_all,
                "users": count,
                "pro": count_pro,
                "ord": order_count,
            },
        )
    return render(
        request,
        "add_category_offer.html",
        {
            "category": category_all,
            "users": count,
            "pro": count_pro,
            "ord": order_count,
        },
    )


@admin_required
def category_offer(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    # product_all = myprodect.objects.all()
    offer = Category_Offer.objects.all().order_by("id")

    return render(
        request,
        "category_offer.html",
        {"offer": offer, "users": count, "pro": count_pro, "ord": order_count},
    )


@admin_required
def category_offer_action(request, id):
    try:
        active = Category_Offer.objects.get(id=id)
        if active.is_active:
            active.is_active = False
        else:
            active.is_active = True
        active.save()
        return redirect("category_offer")
    except Exception as e:
        messages.info(request, "somthing Error")
        print(e)
        return redirect("category_offer")


def edit_category_offer(request, id):
    all = Category_Offer.objects.get(id=id)
    try:
        if request.method == "POST":
            print("product offer inside")
            discount = request.POST.get("discount")
            start_time = request.POST.get("staring")
            expiration_time = request.POST.get("ending")
            product = Category_Offer.objects.get(id=id)
            if discount:
                product.percentage = discount
            if start_time:
                product.start_date = start_time
            if expiration_time:
                product.end_date = expiration_time
            product.save()
            messages.info(request, "Offer edited")
            return redirect("category_offer")  #
    except Exception as e:
        messages.info(request, "somthig error!")
        print(e)
        return render(request, "edit_category_offer.html", {"all": all})
    return render(request, "edit_category_offer.html", {"all": all})


@login_required
def referral(request, id):
    user = str(request.user)  # Convert request.user to string
    user_id = Customer.objects.get(username=user)
    if not Referral.objects.filter(user_id=id).exists():
        temp = user + str(random.randint(1111, 9999))
        while Referral.objects.filter(code=temp).exists():
            temp = user + str(random.randint(1111, 9999))
        Referral.objects.create(user_id=user_id, code=temp)
    return redirect("account")
