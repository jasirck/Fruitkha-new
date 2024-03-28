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
    print(id)
    count = order.objects.filter(user=id.id).count()
    if Wallet.objects.filter(user_id=id).exists():
        wallet = Wallet.objects.get(user_id=id)
        print("hello waaa")
        history = Wallet_list.objects.filter(wallet=wallet).order_by("-date")
        print(f"{username} wallet", wallet.amount, history)
        return render(
            request, "wallet.html", {"t_amount": wallet.amount, "history": history,"count": count}
        )
    else:
        t_amout = 0.00
        print(f"{username}{t_amout} wallet")
        print("hellowweee")
    return render(request, "wallet.html", {"t_amount": t_amout,"count": count})


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
        # readd=order_items.objects.filter(order_item=ord.id)
        # for i in readd:
        #     temp_id=i.product.id
        #     temp=myprodect.objects.get(id=temp_id)
        #     temp.quantity+=i.quantity_now
        #     temp.save()
        # if ord.payment_method == 'Online':
        #     print('inside the wallet if')
        #     if Wallet.objects.filter(user_id=user_obj.id).exists():
        #         wallet_instance = Wallet.objects.get(user_id=user_obj.id)
        #         wallet_instance.amount += ord.total_price
        #         wallet_instance.save()
        #         Wallet_list.objects.create(wallet=wallet_instance, is_credit=True, amount=ord.total_price, msg='Order Canceled')
        #     else:
        #         new_wallet = Wallet.objects.create(user_id=user_obj, amount=ord.total_price)
        #         Wallet_list.objects.create(wallet=new_wallet, is_credit=True, amount=ord.total_price, msg='Order Canceled')
        #         return redirect('detail_page', id)
        return redirect("detail_page", id)
