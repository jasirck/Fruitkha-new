from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from my_admin.models import myprodect, AdminCategory, myvariant
from login.models import Customer
from .forms import prodectsForm
from functools import wraps
from django.urls import reverse
from order.models import order, order_items
from wallet.models import Wallet, Wallet_list
from coupon.models import Coupon
from django.db.models import Q, Sum
from django.db.models import Count
import datetime
from django.db.models.functions import TruncMonth, TruncYear
import datetime
from django.utils.timezone import now
from django.db.models.functions import TruncDay
from django.db.models.functions import Coalesce


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            user = request.user
            if user.is_authenticated and user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                messages.info(request, "your logout")
                return redirect(reverse("admin_login"))
        except:
            logout(request)
            messages.info(request, "your logout")
            return redirect(reverse("admin_login"))

    return _wrapped_view


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if request.user.is_authenticated:
            return redirect("dashboard")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("dashboard")
        else:
            # Authentication failed
            messages.success(request, "Username or Password is Wrong !")
            return redirect("admin_login")
    return render(request, "login_admin.html")


@admin_required
def dashbord(request):
    count = Customer.objects.count()
    order_count = order.objects.filter(
        Q(status="Deliverd") | Q(status="Return Requested")
    ).count()
    total_amount = order.objects.filter(
        Q(status="Deliverd") | Q(status="Return Requested")
    ).aggregate(total_amount=Sum("total_price"))
    amount = total_amount["total_amount"]
    off = order_items.objects.filter(
        Q(order_item__status="Deliverd") | Q(order_item__status="Return Requested")
    )
    offers = 0
    for i in off:
        if i.product.price > i.price_now:
            offers += i.product.price - i.price_now
    monthly_orders = (
        order.objects.filter(Q(status="Deliverd") | Q(status="Return Requested"))
        .annotate(month=TruncMonth("created"))
        .values("month")
        .annotate(order_count=Count("id"))
        .order_by("month")
    )

    # Extract month and order count for each month
    months = []
    order_counts = []
    for item in monthly_orders:
        months.append(item["month"].strftime("%B %Y"))
        order_counts.append(item["order_count"])

    yearly_orders = (
        order.objects.filter(Q(status="Deliverd") | Q(status="Return Requested"))
        .annotate(year=TruncYear("created"))
        .values("year")
        .annotate(order_count=Count("id"))
        .order_by("year")
    )

    # Extract year and order count for each year
    years = []
    yearly_order_counts = []
    for item in yearly_orders:
        years.append(item["year"].year)
        yearly_order_counts.append(item["order_count"])

    # Pass the initial state of the chart (monthly or yearly) to the template
    initial_chart = "monthly"

    # Calculate the start date for the last 30 days
    start_date = now() - datetime.timedelta(days=30)

    # Retrieve order count for each day within the last 30 days
    last_30_days_orders = (
        order.objects.annotate(day=TruncDay("created"))
        .filter(created__gte=start_date)
        .filter(Q(status="Deliverd") | Q(status="Return Requested"))
        .values("day")
        .annotate(order_count=Count("id"))
        .order_by("day")
    )

    # Extract dates and order counts for the last 30 days
    last_30_days_data = {
        item["day"].strftime("%Y-%m-%d"): item["order_count"]
        for item in last_30_days_orders
    }

    # 3d chart
    online = order.objects.filter(
        payment_method="COD", status__in=["Deliverd", "Return Requested"]
    ).count()
    offline = order.objects.filter(
        payment_method="Online", status__in=["Deliverd", "Return Requested"]
    ).count()
    wallet = order.objects.filter(
        payment_method="Wallet", status__in=["Deliverd", "Return Requested"]
    ).count()
    sale = wallet + offline + online

    monthly_delivered_orders = (
        order.objects.filter(Q(status="Delivered") | Q(status="Return Requested"))
        .annotate(month=TruncMonth("created"))
        .values("month")
        .annotate(order_count=Coalesce(Count("id"), 0))
        .order_by("month")
    )

    # Extract month and order count for each month
    months = []
    order_counts = []
    for item in monthly_delivered_orders:
        months.append(item["month"].strftime("%B %Y"))
        order_counts.append(item["order_count"])

    top_products = (
        myprodect.objects.filter(
            order_items__order_item__status__in=["Delivered", "Return Requested"]
        )
        .annotate(num_orders=Count("order_items"))
        .order_by("-num_orders")[:10]
    )

    return render(
        request,
        "dashboard.html",
        {
            "users": count,
            "ord": order_count,
            "amount": amount,
            "offers": offers,
            "months": months,
            "order_counts": order_counts,
            "years": years,
            "yearly_order_counts": yearly_order_counts,
            "initial_chart": initial_chart,
            "last_30_days_data": last_30_days_data,
            "online": online,
            "offline": offline,
            "wallet": wallet,
            "sale": sale,
            "months": months,
            "order_counts": order_counts,
            "top_products": top_products,
        },
    )


@admin_required
def management(request):
    users = Customer.objects.exclude(is_superuser=True).order_by("username")
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    return render(
        request,
        "management.html",
        {"users": count, "user": users, "pro": count_pro, "ord": order_count},
    )


@admin_required
def add_prodect(request):
    option = AdminCategory.objects.all()
    variant_option = myvariant.objects.all()
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    form = prodectsForm(request.POST, request.FILES)

    if request.method == "POST":
        prodect_name = request.POST.get("prodect_name")
        category = request.POST.get("category")
        variant = request.POST.get("variant")
        price = request.POST.get("price")
        description = request.POST.get("description")
        quantity = request.POST.get("quantity")
        prodect_image1 = request.FILES.get("image1", None)
        prodect_image2 = request.FILES.get("image2", None)
        prodect_image3 = request.FILES.get("image3", None)
        variant_id = myvariant.objects.get(id=variant)
        category_id = AdminCategory.objects.get(id=category)
        try:
            add = myprodect(
                prodect_name=prodect_name,
                price=price,
                description=description,
                quantity=quantity,
                category=category_id,
                variant=variant_id,
                prodect_image1=prodect_image1,
                prodect_image2=prodect_image2,
                prodect_image3=prodect_image3,
            )
            add.save()
            messages.success(request, "added prodect")
            return redirect("add_prodect")
        except:
            messages.success(request, "prodect takin awey")
            return redirect("add_prodect")
    return render(
        request,
        "add_prodect.html",
        {
            "users": count,
            "form": form,
            "categories": option,
            "variants": variant_option,
            "pro": count_pro,
        },
    )


@admin_required
def edit_prodect(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    prodect = myprodect.objects.filter(status="list").order_by("prodect_name")
    return render(
        request,
        "edit_prodect.html",
        {"values": prodect, "users": count, "pro": count_pro},
    )


@admin_required
def category(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category_description = request.POST.get("category_description")
        category_image = request.FILES.get("category_image", None)
        category_obj = AdminCategory(
            name=category_name,
            category_description=category_description,
            category_image=category_image,
        )
        category_obj.save()
        messages.success(request, "category aded")
        return redirect("category")  # Redirect to a success page
    return render(
        request, "category.html", {"users": count, "pro": count_pro, "ord": order_count}
    )


@admin_required
def edit_category(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    category = AdminCategory.objects.filter(status="list").order_by("name")
    order_count = order.objects.count()
    return render(
        request,
        "edit_category.html",
        {"category": category, "users": count, "pro": count_pro, "ord": order_count},
    )


@admin_required
def delete_category(request, id):
    delete_ca = AdminCategory.objects.get(id=id)
    delete_ca.status = "unlist"
    delete_ca.save()
    messages.success(request, "delete category")
    return redirect("edit_category")


@admin_required
def edit_category_page(request, id):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    category = AdminCategory.objects.get(id=id)
    if request.method == "POST":
        category.name = request.POST["category_name"]
        category.category_description = request.POST["category_description"]
        if "image1" in request.FILES:
            category.category_image = request.FILES["image1"]
        category.save()
        messages.success(request, "edit category")
        return redirect("edit_category")
    return render(
        request,
        "edit_category_page.html",
        {"category": category, "users": count, "pro": count_pro},
    )


@admin_required
def category_deleted(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    unlist = AdminCategory.objects.filter(status="unlist")
    return render(
        request,
        "category_deleted.html",
        {"unlist": unlist, "users": count, "pro": count_pro},
    )


@admin_required
def readd_category(request, id):
    deleted = AdminCategory.objects.get(id=id)
    deleted.status = "list"
    deleted.save()
    return redirect("category_deleted")


@admin_required
def variant(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    if request.method == "POST":
        name = request.POST.get("variant_name")
        variant_obj = myvariant(variant_name=name)
        variant_obj.save()
        messages.success(request, "variant aded")
        return redirect("edit_variant")
    return render(request, "variant.html", {"users": count})


@admin_required
def edit_variant(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    variant = myvariant.objects.all()
    return render(
        request,
        "edit_variant.html",
        {"variant": variant, "users": count, "pro": count_pro},
    )


@admin_required
def delete_variant(request, id):
    de = myvariant.objects.get(id=id)
    de.status = "unlist"
    de.save()
    messages.success(request, "variant aded")
    return redirect("edit_variant")


@admin_required
def edit_prodect_page(request, id):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    option = AdminCategory.objects.all()
    variant_option = myvariant.objects.all()
    prodect = myprodect.objects.get(id=id)
    if request.method == "POST":
        prodect.prodect_name = request.POST["prodect_name"]
        category = request.POST.get("category")
        variant = request.POST.get("variant")
        variant_id = myvariant.objects.get(id=variant)
        category_id = AdminCategory.objects.get(id=category)
        prodect.category = category_id
        prodect.price = request.POST["price"]
        prodect.description = request.POST["description"]
        quantity = float(request.POST["quantity"])
        prodect.quantity = int(quantity)
        prodect.variant = variant_id

        if "image1" in request.FILES:
            prodect.prodect_image1 = request.FILES["image1"]
        if "image2" in request.FILES:
            prodect.prodect_image2 = request.FILES["image2"]
        if "image3" in request.FILES:
            prodect.prodect_image3 = request.FILES["image3"]

        prodect.save()
        messages.success(request, "edit prodect")
        return redirect("edit_prodect")
    return render(
        request,
        "edit_prodect_page.html",
        {
            "prodect": prodect,
            "users": count,
            "pro": count_pro,
            "categories": option,
            "variants": variant_option,
        },
    )


@admin_required
def action(request, id):
    act = Customer.objects.get(id=id)
    if act.is_active:
        act.is_active = False
        act.save()
        return redirect("management")
    else:
        act.is_active = True
        act.save()
        return redirect("management")


@admin_required
def unlist(request, id):
    deleted = myprodect.objects.get(id=id)
    deleted.status = "unlist"
    deleted.save()
    return redirect("edit_prodect")


@admin_required
def deleted(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    unlist = myprodect.objects.filter(status="unlist")
    return render(
        request, "deleted.html", {"unlist": unlist, "users": count, "pro": count_pro}
    )


@admin_required
def delete(request, id):
    deleted = myprodect.objects.objects.get(id=id)
    deleted.delete()
    return redirect("deleted")


@admin_required
def readd(request, id):
    deleted = myprodect.objects.get(id=id)
    deleted.status = "list"
    deleted.save()
    return redirect("deleted")


@admin_required
def admin_logout(request):
    logout(request)
    messages.info(request, "your logout")
    return render(request, "login_admin.html")


@admin_required
def orders(request):
    ord = order.objects.all().order_by("-created")
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    return render(
        request,
        "orders.html",
        {"order": ord, "users": count, "pro": count_pro, "ord": order_count},
    )


@admin_required
def orders_deteils(request, id):
    ord = order.objects.get(id=id)
    products = order_items.objects.filter(order_item=id)
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    return render(
        request,
        "orders_deteils_admin.html",
        {
            "order": ord,
            "order_item": products,
            "users": count,
            "pro": count_pro,
            "ord": order_count,
        },
    )


@admin_required
def order_back_pending(request, id):
    block = order.objects.get(id=id)
    block.status = "Pending"
    block.msg = ""
    block.save()
    return redirect("orders")


@admin_required
def orders_deliverd(request, id):
    block = order.objects.get(id=id)
    block.status = "Deliverd"
    block.msg = ""
    block.save()
    return redirect("orders")


@admin_required
def orders_cancel(request, id):
    block = order.objects.get(id=id)
    block.status = "Cancel"
    block.msg = "admin Cancel"
    block.save()
    readd = order_items.objects.filter(order_item=block.id)
    for i in readd:
        temp_id = i.product.id
        temp = myprodect.objects.get(id=temp_id)
        temp.quantity += i.quantity_now
        temp.save()
    return redirect("orders_deteils", id)


@admin_required
def return_accept(request, id):
    ord = order.objects.get(id=id)
    ord.status = "Returned"
    ord.save()
    readd = order_items.objects.filter(order_item=ord.id)
    for i in readd:
        temp_id = i.product.id
        temp = myprodect.objects.get(id=temp_id)
        temp.quantity += i.quantity_now
        temp.save()
    if Wallet.objects.filter(user_id=ord.user).exists():
        wallet_instance = Wallet.objects.get(user_id=ord.user)
        wallet_instance.amount += ord.total_price
        wallet_instance.save()
        Wallet_list.objects.create(
            wallet=wallet_instance,
            is_credit=True,
            amount=ord.total_price,
            msg="Order Returned",
        )
        return redirect("orders_deteils", id)
    else:
        new_wallet = Wallet.objects.create(user_id=ord.user, amount=ord.total_price)
        new_wallet.save()
        Wallet_list.objects.create(
            wallet=new_wallet,
            is_credit=True,
            amount=ord.total_price,
            msg="Order Canceled",
        )
        return redirect("orders_deteils", id)


@admin_required
def coupon(request):
    count = Customer.objects.count()
    count_pro = myprodect.objects.count()
    order_count = order.objects.count()
    coupon = Coupon.objects.all().order_by("id")
    return render(
        request,
        "coupon.html",
        {"coupon": coupon, "users": count, "pro": count_pro, "ord": order_count},
    )
