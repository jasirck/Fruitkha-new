from django.shortcuts import render, redirect
from my_admin.models import myprodect
from login.models import Customer
from cart.models import cart, Wishlist
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from offer.models import Product_Offer, Category_Offer
# Create your views here.


@login_required
def Cart(request):
    username = request.user
    user_obj = Customer.objects.get(username=username)
    cart_obj = (
        cart.objects.filter(user_id=user_obj.id)
        .prefetch_related("product_id")
        .order_by("id")
    )
    # pro_offer =
    subtotal_query = cart.objects.filter(Q(user_id=user_obj.id)).aggregate(
        subtotal=Sum("cart_total")
    )
    subtotal = (
        subtotal_query["subtotal"] if subtotal_query["subtotal"] is not None else 0
    )

    shipping = 0 if int(subtotal) > 1000 else 0 if int(subtotal) == 0 else 40
    total = subtotal + shipping
    log = True
    return render(
        request,
        "cart.html",
        {
            "log": log,
            "cart_obj": cart_obj,
            "subtotal": subtotal,
            "ship": shipping,
            "total": total,
        },
    )


@login_required
def add_cart(request, id):
    print("add  cart   here  **88888**888*88*88")
    if request.method == "POST":
        username = request.user
        user_id = Customer.objects.get(username=username)
        quantity = request.POST.get("quantity")
        product_id = myprodect.objects.get(id=id)
        print("dddd", user_id.id, "aaaaa", quantity, "quantity")
        offer = False
        amount = product_id.price
        if quantity.strip() is not None:
            try:
                if cart.objects.filter(product_id=product_id).exists():
                    add = cart.objects.get(product_id=product_id)
                    add.book_quantity += int(quantity)
                    if (
                        add.book_quantity > product_id.quantity
                        or add.book_quantity > 10
                        or add.book_quantity < 1
                    ):
                        print("2", product_id)
                        messages.success(request, "We did't have that much quantity")
                        return redirect("single_prodect", id)

                    # offer  check
                    category = product_id.category

                    if Product_Offer.objects.filter(
                        produc_id=product_id, is_active=True
                    ).exists():
                        offer = True
                        product = Product_Offer.objects.get(
                            produc_id=product_id, is_active=True
                        )
                        percentage = product.percentage
                        category = product_id.category
                        print(category)
                        if Category_Offer.objects.filter(
                            category_id=category, is_active=True
                        ).exists():
                            category_instence = Category_Offer.objects.get(
                                category_id=category, is_active=True
                            )
                            category_percentage = category_instence.percentage
                            if percentage < category_percentage:
                                percentage = category_percentage
                    elif Category_Offer.objects.filter(
                        category_id=category, is_active=True
                    ).exists():
                        offer = True
                        print(category)
                        category_instence = Category_Offer.objects.get(
                            category_id=category, is_active=True
                        )
                        percentage = category_instence.percentage
                    if offer:
                        minus = amount * (percentage / 100)
                        amount -= minus

                    # offeer end

                    add.current_price = amount
                    add.save()
                    messages.success(request, "added to cart")
                    return redirect("single_prodect", id)
                if (
                    product_id.quantity < int(quantity)
                    or int(quantity) > 10
                    or int(quantity) < 1
                ):
                    print("1", product_id)
                    messages.success(request, "We did't have that much quantity")
                    return redirect("single_prodect", id)

                else:
                    # offer  check
                    category = product_id.category

                    if Product_Offer.objects.filter(
                        produc_id=product_id, is_active=True
                    ).exists():
                        offer = True
                        product = Product_Offer.objects.get(
                            produc_id=product_id, is_active=True
                        )
                        percentage = product.percentage
                        category = product_id.category
                        print(category)
                        if Category_Offer.objects.filter(
                            category_id=category, is_active=True
                        ).exists():
                            category_instence = Category_Offer.objects.get(
                                category_id=category, is_active=True
                            )
                            category_percentage = category_instence.percentage
                            if percentage < category_percentage:
                                percentage = category_percentage
                    elif Category_Offer.objects.filter(
                        category_id=category, is_active=True
                    ).exists():
                        offer = True
                        print(category)
                        category_instence = Category_Offer.objects.get(
                            category_id=category, is_active=True
                        )
                        percentage = category_instence.percentage
                    if offer:
                        minus = amount * (percentage / 100)
                        amount -= minus

                    # offeer end

                    cart_obj = cart(
                        user_id=user_id,
                        product_id=product_id,
                        book_quantity=int(quantity),
                        cart_total=int(quantity) * amount,
                        current_price=amount,
                    )
                    cart_obj.save()
                    print("1.1", product_id)
                    messages.success(request, "added to cart")
                    return redirect("single_prodect", id)  # ,'success.html'
            except ValueError:
                print("3", product_id)
                messages.success(request, "can not add without quantity")
                return redirect("single_prodect", id)  # {'message': 'Invalid quantity'}
        else:
            messages.success(request, "can not add without quantity")
            return redirect(
                "single_prodect", id
            )  # , {'message': 'Quantity cannot be empty'}
    return redirect("single_prodect", id)


@login_required
def delete_cart(request, id):
    delete = cart.objects.get(id=id)
    delete.delete()
    return redirect("Cart")


@login_required
def quantity_cart(request):
    if request.method == "POST":
        products_id = int(request.POST.get("products_id"))
        action = request.POST.get("action")
        item = cart.objects.get(id=products_id)
        print("cart quantity")
        if action == "plus":
            item.book_quantity += 1
            if item.product_id.quantity < int(
                item.book_quantity or int(item.book_quantity) > 10
            ):
                messages.success(request, "We did't have that much quantity")
                # return redirect('Cart')
                return JsonResponse({"status": "updated suucessfully"})
        elif action == "minus":
            item.book_quantity -= 1
            if item.product_id.quantity < int(
                item.book_quantity or int(item.book_quantity) > 10
            ):
                messages.success(request, "We did't have that much quantity")
                # return redirect('Cart')
                return JsonResponse({"status": "updated suucessfully"})

        item.cart_total = item.current_price * item.book_quantity
        item.save()

        return JsonResponse({"status": "updated suucessfully"})


@login_required
def wishlist_page(request):
    username = request.user
    user = Customer.objects.get(username=username)
    log = True
    wish = Wishlist.objects.filter(user_id=user)
    # pri=
    # print(wish)
    return render(request, "wishlist.html", {"log": log, "wishlist": wish})


@login_required
def wishlist_new(request, id):
    username = request.user
    username = Customer.objects.get(username=username)
    product = myprodect.objects.get(id=id)
    if Wishlist.objects.filter(user_id=username, product_id=product).exists():
        Wishlist.objects.filter(user_id=username, product_id=product).delete()
        return redirect("single_prodect", id)
    else:
        Wishlist.objects.create(user_id=username, product_id=product)
        return redirect("single_prodect", id)


@login_required
def add_to_cart(request):
    print("hello_wisddhfghxt")
    if request.method == "POST" and request.is_ajax():
        user = request.user
        user_id = Customer.objects.get(username=user)
        product_id = request.POST.get("product_id")
        product = myprodect.objects.get(id=product_id)
        offer = False
        amount = product.price
        print(product_id)
        if cart.objects.filter(product_id=product).exists():
            add = cart.objects.get(product_id=product_id)
            add.book_quantity += 1
            print("add to cart first one")
            messages.success(request, "added to cart")
            return JsonResponse({"success": True, "message": "Product added to cart."})
        else:
            # offer  check
            category = product.category

            if Product_Offer.objects.filter(
                produc_id=product_id, is_active=True
            ).exists():
                offer = True
                product = Product_Offer.objects.get(
                    produc_id=product_id, is_active=True
                )
                percentage = product.percentage
                category = product_id.category
                print(category)
                if Category_Offer.objects.filter(
                    category_id=category, is_active=True
                ).exists():
                    category_instence = Category_Offer.objects.get(
                        category_id=category, is_active=True
                    )
                    category_percentage = category_instence.percentage
                    if percentage < category_percentage:
                        percentage = category_percentage
            elif Category_Offer.objects.filter(
                category_id=category, is_active=True
            ).exists():
                offer = True
                print(category)
                category_instence = Category_Offer.objects.get(
                    category_id=category, is_active=True
                )
                percentage = category_instence.percentage
            if offer:
                minus = amount * (percentage / 100)
                amount -= minus

                # offeer end
            cart_obj = cart(
                user_id=user_id,
                product_id=product,
                book_quantity=1,
                cart_total=1 * amount,
                current_price=amount,
            )
            print("add to cart first one")
            cart_obj.save()
        print("1.1", product_id)
        # messages.success(request, 'added to cart')
        # return redirect("single_prodect",id)#,'success.html'
        print("hello wish")
        return JsonResponse({"success": True, "message": "Product added to cart."})
    else:
        print("hello wish else")
        return JsonResponse({"success": False, "message": "Invalid request"})


def wishlist_remove(request):
    if request.method == "POST" and request.is_ajax():
        user = request.user
        username = Customer.objects.get(username=user)
        product_id = request.POST.get("product_id")
        product = myprodect.objects.get(id=product_id)
        print(product_id)
        remove = Wishlist.objects.filter(user_id=username, product_id=product)
        remove.delete()
        return JsonResponse({"success": True, "message": "Product Removed."})
    else:
        print("hello wish else")
        return JsonResponse({"success": False, "message": "Invalid request"})
