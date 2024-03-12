from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from my_admin.models import myprodect,myvariant,AdminCategory
from login.models import Customer
from django.db.models import Count
from order.models import order,order_items
from cart.models import Wishlist
from django.http import JsonResponse
from offer.models import Product_Offer,Category_Offer

# Create your views here.
# @login_required(login_url="/accounts/login/")
# def shop(request):
#     # if 'username'in request.session:
#         if request.user.is_authenticated:
#             log=True
#         else:
#             log=False
#         top_3_products = order_items.objects.values('product__prodect_name', 'product__prodect_image1', 'product__price', 'product__quantity').annotate(total_orders=Count('product')).order_by('-total_orders')[:3]

#         print(top_3_products)
#         # new = myprodect.objects.filter(category__status='list', quantity__gt=0).order_by('-' + filter)[:3]
#         main_prodect=myprodect.objects.filter(category__status='list',status="list",quantity__gt=0).order_by('prodect_name')
#         main_category = AdminCategory.objects.filter(status="list").order_by('name')
#         return render(request,'shop.html',{'main_prodect':main_prodect,'main_category': main_category,'log':log,'top_3':top_3_products})
    # return render(request,'login.html')
    
    
def shop(request):
    if request.user.is_authenticated:
        log = True
    else:
        log = False
        
    top_3_products = myprodect.objects.annotate(order_count=Count('order_items')).order_by('-order_count')[:3]
    print(top_3_products)
    main_prodect = myprodect.objects.filter(category__status='list', status="list", quantity__gt=0).order_by('prodect_name')
    
    print(main_prodect)
    main_category = AdminCategory.objects.filter(status="list").order_by('name')
    return render(request, 'shop.html', {'main_prodect': main_prodect, 'main_category': main_category, 'log': log, 'top_3': top_3_products})


def shop_cat(request, id):
    if request.user.is_authenticated:
        log=True
    else:
        log=False
    prodects =myprodect.objects.filter(category=id,quantity__gt=0,status="list",category__status='list')
    main_category = AdminCategory.objects.filter(status="list").order_by('name')
    hover=id
    return render(request, 'shop.html', {'main_prodect': prodects, 'main_category': main_category,'hover':hover,'log':log})
    
def shop_search(request):
    # if 'username'in request.session:
        if request.user.is_authenticated:
            log=True
        else:
            log=False
        if request.method == 'POST':
            category = request.POST.get('category')
            print(category)
            search = request.POST.get('search')
            main_prodect=myprodect.objects.filter(category__status='list',status="list",quantity__gt=0,prodect_name__icontains=search).order_by('prodect_name')
            main_category = AdminCategory.objects.filter(status="list").order_by('name')
            return render(request,'shop.html',{'main_prodect':main_prodect,'main_category': main_category,'log':log})
        main_prodect=myprodect.objects.filter(category__status='list',status="list",quantity__gt=0).order_by('prodect_name')
        main_category = AdminCategory.objects.filter(status="list").order_by('name')
        return render(request,'shop.html',{'main_prodect':main_prodect,'main_category': main_category,'log':log})
    # return render(request,'login.html')

def shop_filter(request):
    # if 'username'in request.session:
        if request.user.is_authenticated:
            log=True
        else:
            log=False
        if request.method == 'POST':
            filter = request.POST.get('filter')#filter(Q(name__icontains='John')
            category = request.POST.get('category')
            print(category)
            if category:
                
                if filter == 'prodect_name' or filter =='price' or filter =='rating'  or filter =='date_added':
                    print('inside filter',filter) 
                    main_prodect=myprodect.objects.filter(category=category,category__status='list',status="list",quantity__gt=0).order_by(filter)
                    main_category = AdminCategory.objects.filter(status="list").order_by('name')
                    return render(request,'shop.html',{'hover':category,'main_prodect':main_prodect,'main_category': main_category,'log':log})
                if filter == 'prodect_name_decs' or filter =='price_decs' or filter =='rating_decs'   or filter =='date_added_decs':
                    filter = filter[:-5] 
                    print('inside filter',filter)
                    main_prodect=myprodect.objects.filter(category=category,category__status='list',status="list",quantity__gt=0).order_by('-' + filter)
                    main_category = AdminCategory.objects.filter(status="list").order_by('name')
                    return render(request,'shop.html',{'hover':category,'main_prodect':main_prodect,'main_category': main_category,'log':log})
            if filter == 'prodect_name' or filter =='price' or filter =='rating'  or filter =='date_added':
                print('inside filter',filter) 
                main_prodect=myprodect.objects.filter(category__status='list',status="list",quantity__gt=0).order_by(filter)
                main_category = AdminCategory.objects.filter(status="list").order_by('name')
                return render(request,'shop.html',{'main_prodect':main_prodect,'main_category': main_category,'log':log})
            if filter == 'prodect_name_decs' or filter =='price_decs' or filter =='rating_decs'  or filter =='date_added_decs':
                filter = filter[:-5] 
                print('inside filter',filter)
                main_prodect=myprodect.objects.filter(category__status='list',status="list",quantity__gt=0).order_by('-' + filter)

                main_category = AdminCategory.objects.filter(status="list").order_by('name')
                return render(request,'shop.html',{'main_prodect':main_prodect,'main_category': main_category,'log':log})
        main_prodect=myprodect.objects.filter(category__status='list',quantity__gt=0).order_by('prodect_name')
        main_category = AdminCategory.objects.filter(status="list").order_by('name')
        return render(request,'shop.html',{'main_prodect':main_prodect,'main_category': main_category,'log':log})
    # return render(request,'login.html')

def single_prodect(request, id):
    if request.user.is_authenticated:
        user=request.user
        log = True
        single = myprodect.objects.get(id=id)
        offer = False
        category  = single.category
        
        # offer
        
        if Product_Offer.objects.filter(produc_id=single,is_active = True).exists():
            offer =True
            product = Product_Offer.objects.get(produc_id=single,is_active = True)
            percentage = product.percentage
            category  = single.category
            print(category)
            if Category_Offer.objects.filter(category_id=category,is_active = True).exists():
                category_instence = Category_Offer.objects.get(category_id=category,is_active = True)
                category_percentage = category_instence.percentage
                if percentage <category_percentage:
                    percentage = category_percentage
        elif Category_Offer.objects.filter(category_id=category,is_active = True).exists():
            print(category)
            offer =True
            category_instence = Category_Offer.objects.get(category_id=category,is_active = True)
            percentage = category_instence.percentage
        
        # offer
        
        left = True
        if single.quantity > 6:
            left = False
        amount = single.price
        if offer:
            minus = amount*(percentage/100)
            amount -=minus

        cate = single.category
        var = single.variant
        wish= True if Wishlist.objects.filter(user_id=user,product_id=id).exists() else False
        return render(request, 'single_product.html', {'amount':amount,'offer':offer,'single_product': single, 'cate': cate, 'var': var, 'log': log, 'left': left,'wish':wish})
    return render(request, 'login.html')

  

def single_prodect_img(request,id,img):
    if request.user.is_authenticated:
        user=request.user
        log=True
        left = True
        single=myprodect.objects.get(id=id)
        if single.quantity > 6:
            left = False
        offer = False
        # if single.offer > 0:
        #     offer =True
        cate=single.category
        var=single.variant
        wish= True if Wishlist.objects.filter(user_id=user,product_id=id).exists() else False
        return render(request,'single_product.html',{'offer':offer,'log':log,'single_product':single,'cate':cate,'var':var,'img':img, 'left': left,'wish':wish})
    return render(request,'login.html')
    
    
@login_required
def wishlist(request, id):
    username = request.user
    username = Customer.objects.get(username=username)
    product = myprodect.objects.get(id=id)
    if Wishlist.objects.filter(user_id=username, product_id=product).exists():
        Wishlist.objects.filter(user_id=username, product_id=product).delete()
        return JsonResponse({'wish':False,'message': 'Removed from wishlist'})
    else:
        Wishlist.objects.create(user_id=username, product_id=product)
        return JsonResponse({'wish':True,'message': 'Added to wishlist'})

