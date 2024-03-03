from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from my_admin.models import myprodect,myvariant,AdminCategory

# Create your views here.
# @login_required(login_url="/accounts/login/")
def shop(request):
    # if 'username'in request.session:
        if request.user.is_authenticated:
            log=True
        else:
            log=False
        # new = myprodect.objects.filter(category__status='list', quantity__gt=0).order_by('-' + filter)[:3]
        main_prodect=myprodect.objects.filter(category__status='list',status="list",quantity__gt=0).order_by('prodect_name')
        main_category = AdminCategory.objects.filter(status="list").order_by('name')
        return render(request,'shop.html',{'main_prodect':main_prodect,'main_category': main_category,'log':log})
    # return render(request,'login.html')
    

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

def single_prodect(request,id):
    if request.user.is_authenticated:
        log=True
        single=myprodect.objects.get(id=id)
        left:True
        if single.quantity > 6:
            left=False
            # single.quantity=5
            # single.save()
        cate=single.category
        var=single.variant
        return render(request,'single_product.html',{'single_product':single,'cate':cate,'var':var,'log':log,'left':left})
    return render(request,'login.html')
  

def single_prodect_img(request,id,img):
    if request.user.is_authenticated:
        log=True
        single=myprodect.objects.get(id=id)
        if single.quantity <= 6:
            left=True
        cate=single.category
        var=single.variant
        return render(request,'single_product.html',{'log':log,'single_product':single,'cate':cate,'var':var,'img':img})
    return render(request,'login.html')
    