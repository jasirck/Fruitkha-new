from django.shortcuts import render,redirect
from login.models import Customer,user_address
from my_admin.views import myprodect
from cart.models import cart
from django.db.models import Sum
from order.models import order,order_items
import random
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def checkout(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj =Customer.objects.filter(username=username).prefetch_related('current_address').first()
        address = user_address.objects.filter(user_id=user_obj.id)
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related("product_id")
        subtotal= cart.objects.filter(user_id=user_obj.id).aggregate(subtotal=Sum('cart_total'))
        subtotal = subtotal['subtotal'] if subtotal['subtotal'] is not None else subtotal['subtotal']
        if subtotal is None:
            shipping = 0
            subtotal = 0  # Set subtotal to 0 if it's None
        elif subtotal > 1000:
            shipping = 0
        else:
            shipping = 40
        total = subtotal + shipping
        log=True
        return render(request,'checkout.html',{'log':log,'user':user_obj,'cart_obj':cart_obj,'subtotal':subtotal,'ship':shipping,'total':total,'address':address})
    return render(request,'login.html')

@login_required
def chenge(request,id):
    if request.user.is_authenticated:
        user_obj=Customer.objects.get(id=id)
        address = user_address.objects.filter(user_id=user_obj.id)
        test=False
        if not address.exists():  
            test = True
        print(test)
        if request.method == 'POST':
            address=request.POST.get('address')
            add=user_address.objects.get(id=address)
            user_id=Customer.objects.get(id=id)
            user_id.current_address=add
            user_id.save()
            return redirect('checkout')
        print(address)
        return render(request,'chenge.html',{'user':user_obj, 'address':address,"test":test ,'check':True})
    return render(request,'login.html')

@login_required
def add_address_order(request):

    username = request.user
    user_obj=Customer.objects.get(username=username)
        
    if request.method == 'POST':
        name=request.POST.get('name')
        call_number=request.POST.get('call_number')
        house_name=request.POST.get('housename')
        lanmark=request.POST.get('lanmark')
        post=request.POST.get('post')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        print('before')
        if  ''!= name.strip() and ''!= call_number.strip() and ''!= house_name.strip() and ''!= lanmark.strip() and ''!= post.strip() and ''!= city.strip() and ''!= state.strip() and''!= pincode.strip() :
            address=user_address(user_id=user_obj,name=name,call_number=call_number,house_name=house_name,lanmark=lanmark,post=post,city=city,state=state,pincode=pincode)
            print('after')
            print(address.user_id,address.name,address.call_number,type(address.call_number),address.house_name,address.lanmark,address.post,address.city,address.pincode,address.state)
            address.save()
            return redirect('checkout')
                
        else:
            messages.error(request, "address field id null")
            return redirect('add_address_order')
    return render(request,'checkout_add_address.html',{'user':user_obj})

@login_required
def cod_order(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj =Customer.objects.filter(username=username).prefetch_related('current_address').first()
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related("product_id")
        subtotal = cart.objects.filter(user_id=user_obj.id).aggregate(subtotal=Sum('cart_total'))
        subtotal = subtotal['subtotal'] if subtotal['subtotal'] is not None else subtotal['subtotal']
        shipping= 0 if subtotal>1000 else 40
        total=subtotal+shipping
        temp='fruitkha'+str(random.randint(111111,999999))
        while order.objects.filter(order_id=temp) is None:
            temp='fruitkha'+str(random.randint(111111,999999))
        address_text = f"{user_obj.current_address.name},{user_obj.current_address.call_number},{user_obj.current_address.house_name},{user_obj.current_address.lanmark},{user_obj.current_address.post},{user_obj.current_address.city},{user_obj.current_address.state},{user_obj.current_address.pincode}"
        ord=order(user=user_obj,total_price=total,payment_method='COD',order_id=temp,address=address_text)
        ord.save()

        for i in cart_obj:
            ord_it=order_items(order_item=ord,product=i.product_id,price_now=i.product_id.price,quantity_now=i.book_quantity)
            prod=myprodect.objects.get(id=i.product_id.id)
            print(i.product_id.id)
            prod.quantity-=i.book_quantity
            prod.save()
            ord_it.save()
        cart_obj.delete()
        log=True
        return render(request,'order_succes.html',{'log':log,'order_id':temp,'total':total})
    return render ('shop.html')


@login_required
def razorpaychek(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj =Customer.objects.filter(username=username).prefetch_related('current_address').first()
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related("product_id")
        subtotal = cart.objects.filter(user_id=user_obj.id).aggregate(subtotal=Sum('cart_total'))
        subtotal = subtotal['subtotal'] if subtotal['subtotal'] is not None else subtotal['subtotal']
        shipping= 0 if subtotal>1000 else 40
        total=subtotal+shipping
        print(subtotal  )
        temp='fruitkha'+str(random.randint(111111,999999))
        while order.objects.filter(order_id=temp) is None:
            temp='fruitkha'+str(random.randint(111111,999999))
        # ord=order(user=user_obj,total_price=total,payment_method='COD',order_id=temp)
        # ord.save()

        # for i in cart_obj:
        #     ord_it=order_items(order_item=ord,product=i.product_id,price_now=i.product_id.price,quantity_now=i.book_quantity)
        #     ord_it.save()
        # cart_obj.delete()
        print('hello razor pay here')
        return JsonResponse({
            'total_price':total,
            'order_id':temp
        })
    return render ('login')


@login_required
def online_order(request):
    if request.user.is_authenticated:
        username = request.user
        user_obj =Customer.objects.filter(username=username).prefetch_related('current_address').first()
        cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related("product_id")
        payment_id=request.POST.get('payment_id')
        order_id=request.POST.get('order_id')
        total=request.POST.get('total')
        address_text = f"{user_obj.current_address.name},{user_obj.current_address.call_number},{user_obj.current_address.house_name},{user_obj.current_address.lanmark},{user_obj.current_address.post},{user_obj.current_address.city},{user_obj.current_address.state},{user_obj.current_address.pincode}"
        ord=order(user=user_obj,total_price=total,payment_method='Online',order_id=order_id,payment_id=payment_id,address=address_text)
        ord.save()

        for i in cart_obj:
            ord_it=order_items(order_item=ord,product=i.product_id,price_now=i.product_id.price,quantity_now=i.book_quantity)
            prod=myprodect.objects.get(id=i.product_id.id)
            print(i.product_id.id)
            prod.quantity-=i.book_quantity
            prod.save()
            ord_it.save()
            cart_obj.delete()
        return JsonResponse({'status':"Your Order Placed Succesfully"})
    return redirect ('login')


@login_required
def online_sucess(request):
    return HttpResponse("MyOrder is succesfuly placed")

@login_required
def address_check(request,id,a_id):
    if request.user.is_authenticated:
        user_obj=Customer.objects.get(id=id)
        address=user_address.objects.get(id=a_id)
        if request.method == 'POST':
            address.name=request.POST.get('name')
            address.call_number=request.POST.get('call_number')
            address.house_name=request.POST.get('housename')
            address.lanmark=request.POST.get('lanmark')
            address.post=request.POST.get('post')
            address.city=request.POST.get('city')
            address.state=request.POST.get('state')
            address.pincode=request.POST.get('pincode')
            address.user_id=Customer.objects.get(id=id)
            print('before')
            # address=user_address(user_id=user_id,name=name,call_number=call_number,house_name=house_name,lanmark=lanmark,post=post,city=city,state=state,pincode=pincode)
            print('after')
            print(address.user_id,address.name,address.call_number,type(address.call_number),address.house_name,address.lanmark,address.post,address.city,address.pincode,address.state)
            address.save()
            return redirect('checkout')
        return render(request,'check_edit_address.html',{'user':user_obj,'address':address})
    return render(request,'login.html')



@login_required
def succes(request):
    
    return render(request,'order_succes.html')