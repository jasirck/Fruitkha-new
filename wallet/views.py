from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Wallet_list
from login.models import Customer
from order.models import order

# Create your views here.


@login_required
def wallet(request):
    username = request.user
    id = Customer.objects.get(username=username)
    count = order.objects.filter(user=id.id).count()
    if Wallet.objects.filter(user_id=id).exists():
        wallet = Wallet.objects.get(user_id=id)
        history = Wallet_list.objects.filter(wallet=wallet).order_by("-date")
        return render(
            request,
            "wallet.html",
            {"t_amount": wallet.amount, "history": history, "count": count},
        )
    else:
        t_amout = 0.00
    return render(request, "wallet.html", {"t_amount": t_amout, "count": count})


@login_required
def return_order(request, id):
    username = request.user
    user_obj = Customer.objects.get(username=username)
    ord = order.objects.get(id=id)
    if request.method == "POST":
        msg = request.POST.get("msg")
        status = request.POST.get("status")
        ord.msg = msg
        ord.status = status
        ord.save()
        
        return redirect("detail_page", id)
