from django.shortcuts import render
from my_admin.models import AdminCategory

# Create your views here.


def homepage(request):
    if request.user.is_authenticated:
        # If the user is authenticated, you can access the user instance
        # user = request.user
        log = True
    else:
        log = False
    print("homepage here")
    main_category = AdminCategory.objects.filter(status="list")
    # top_3_products = order_items.objects.values('product__name').annotate(total_orders=Count('product')).order_by('-total_orders')[:3]
    return render(
        request, "homepage.html", {"log": log, "main_category": main_category}
    )


def news(request):
    if request.user.is_authenticated:
        log = True
    else:
        log = False
    print("newspage here")
    return render(request, "news.html", {"log": log})


def contact(request):
    if request.user.is_authenticated:
        log = True
    else:
        log = False
    print("contactpage here")
    return render(request, "contact.html", {"log": log})


def about(request):
    if request.user.is_authenticated:
        log = True
    else:
        log = False
    print("homepage here")
    main_category = AdminCategory.objects.all()
    return render(
        request, "homepage.html", {"main_category": main_category, "log": log}
    )
