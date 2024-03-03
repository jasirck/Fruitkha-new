from django.shortcuts import render,redirect
from my_admin.models import myprodect
from login.models import Customer
from cart.models import cart
from django.contrib import messages
from django.db.models import Sum,Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def Cart(request):
    username = request.user
    user_obj = Customer.objects.get(username=username)
    cart_obj = cart.objects.filter(user_id=user_obj.id).prefetch_related("product_id").order_by('id')
    subtotal_query = cart.objects.filter(Q(user_id=user_obj.id)).aggregate(subtotal=Sum('cart_total'))
    subtotal = subtotal_query['subtotal'] if subtotal_query['subtotal'] is not None else 0

    shipping= 0 if int(subtotal) >1000 else 0 if int(subtotal) == 0 else 40
    total=subtotal+shipping
    log=True
    return render(request,'cart.html',{'log':log,'cart_obj':cart_obj,'subtotal':subtotal,'ship':shipping,'total':total})

@login_required
def add_cart(request,id):
    print('add  cart   here  **88888**888*88*88')
    if request.method == 'POST':
        username = request.user
        user_id = Customer.objects.get(username=username)
        quantity=request.POST.get('quantity')
        product_id =  myprodect.objects.get(id=id)
        print('dddd',user_id.id,'aaaaa',quantity,"quantity")
        if quantity.strip() is not None:
            try:
                if cart.objects.filter(product_id=product_id).exists():
                    add=cart.objects.get(product_id=product_id)
                    add.book_quantity+=int(quantity)
                    if add.book_quantity > product_id.quantity or add.book_quantity > 10:
                        print('2',product_id)
                        messages.success(request, "We did't have that much quantity")
                        return redirect("single_prodect",id)
                    add.save()
                    messages.success(request, 'added to cart')
                    return redirect("single_prodect",id)
                if product_id.quantity < int(quantity) or int(quantity) > 10:
                    print('1',product_id)
                    messages.success(request, "We did't have that much quantity")
                    return redirect("single_prodect",id)
                    
                else:
                    cart_obj =cart(user_id=user_id,product_id=product_id,book_quantity=int(quantity),cart_total=int(quantity)*product_id.price)
                    cart_obj.save()
                    print('1.1',product_id)
                    messages.success(request, 'added to cart')
                    return redirect("single_prodect",id)#,'success.html'
            except ValueError:
                print('3',product_id)
                messages.success(request, 'can not add without quantity')
                return redirect("single_prodect",id)# {'message': 'Invalid quantity'}
        else:
            messages.success(request, 'can not add without quantity')
            return redirect("single_prodect",id)#, {'message': 'Quantity cannot be empty'}            
    return redirect("single_prodect",id)

@login_required
def delete_cart(request,id):
    delete=cart.objects.get(id=id)
    delete.delete()
    return redirect('Cart')

# @login_required
# def plus_cart(request,id,price):
#     plus=cart.objects.get(id=id)
#     print(plus.product_id)
#     plus.book_quantity+=1
#     if plus.product_id.quantity < int(plus.book_quantity or  int(plus.book_quantity ) < 10 ):
#         messages.success(request, "We did't have that much quantity")
#         return redirect('Cart')
#     plus.cart_total=price * plus.book_quantity
#     plus.save()
#     messages.success(request, "quantity ingrees")
#     return redirect('Cart')
    
# @login_required
# def minus_cart(request,id,price):
#     plus=cart.objects.get(id=id)
#     print(plus.product_id)
#     plus.book_quantity-=1

#     plus.cart_total=price * plus.book_quantity
#     plus.save()
#     return redirect('Cart')

@login_required
def quantity_cart(request):
    if request.method == "POST":
        products_id = int(request.POST.get("products_id"))
        action = request.POST.get("action")
        item = cart.objects.get(id=products_id)
        print('cart quantity')
        if action == "plus":
            item.book_quantity+=1
            if item.product_id.quantity < int(item.book_quantity or  int(item.book_quantity ) > 10 ):
                messages.success(request, "We did't have that much quantity")
                # return redirect('Cart')
                return JsonResponse({"status": "updated suucessfully"})
        elif action == "minus":
            item.book_quantity-=1
            if item.product_id.quantity < int(item.book_quantity or  int(item.book_quantity ) > 10 ):
                messages.success(request, "We did't have that much quantity")
                # return redirect('Cart')
                return JsonResponse({"status": "updated suucessfully"})

            
        item.cart_total=item.product_id.price * item.book_quantity
        item.save()

        return JsonResponse({"status": "updated suucessfully"})

# @login_required
# def plus_cart(request, id, price):
#     cart_item = Cart.objects.get(id=id)
#     cart_item.book_quantity += 1
#     cart_item.cart_total = price * cart_item.book_quantity
#     cart_item.save()
#     return JsonResponse({'book_quantity': cart_item.book_quantity})

# @login_required
# def minus_cart(request, id, price):
#     plus = cart.objects.get(id=id)
#     print(plus.product_id)
#     plus.book_quantity -= 1
#     plus.cart_total = price * plus.book_quantity
#     plus.save()
#     return JsonResponse({'book_quantity': plus.book_quantity})
