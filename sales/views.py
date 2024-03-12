from django.shortcuts import render,redirect
from my_admin.views import admin_required
from my_admin.models import myprodect,AdminCategory
from login.models import Customer
from coupon.models import Coupon
from order.models import order
from django.contrib import messages
from offer.models import Product_Offer,Category_Offer
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa
from order.models import order,order_items
from django.db.models import Q
from datetime import datetime, timedelta
import xlsxwriter
from io import BytesIO
from django.utils.html import strip_tags
import pandas as pd




# Create your views here.

# @admin_required
# def sales_report(request):
    # sales = order_items.objects.filter(
    #     order_item__status__in=['Deliverd', 'Return Requested']
    # )
    # if request.method == 'get':
    #     filter = request.POST.get('filter')
    #     if filter = "fixed":
    #          interval = request.POST.get('interval')
    
    # template_path = 'report.html'
    # for sale in sales:
    #     print(sale.product)
    #     dis = sale.product.price - sale.price_now
    #     setattr(sale, 'dis', dis)
    # print(sales)
    # context = {'sales': sales}
    # html_content = render(request, template_path, context).content.decode('utf-8')
    # return render(request, 'report.html', {'html_content': html_content,'sales':sales,"pdf":True})

@admin_required
def sales_report(request):
    print("hello sales report")
    if request.method == 'POST':
        print("hello sales report inside")
        # Get the selected time interval from the request
        filter = request.POST.get('filter')
        if filter == "fixed":
            interval = request.POST.get('interval')
            print(interval,filter)
        
        # Define the date range based on the selected interval
            if interval == 'day':
                start_date = datetime.now().date() - timedelta(days=1)
                end_date = datetime.now().date()
                print(start_date,end_date)
            elif interval == 'week':
                start_date = datetime.now().date() - timedelta(weeks=1)
                end_date = datetime.now().date()
            elif interval == 'month':
                start_date = datetime.now().date() - timedelta(days=30)
                end_date = datetime.now().date()
            elif interval == 'year':
                start_date = datetime.now().date() - timedelta(days=365)
                end_date = datetime.now().date()

# Filter the order items based on the selected interval and status
            sales = order_items.objects.filter(
                order_item__status__in=['Deliverd', 'Return Requested'],
                order_item__created__range=[start_date, end_date]
            )
        if filter == "custom":
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            
            # Convert date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # Filter the order items based on the custom date range and status
            sales = order_items.objects.filter(
                order_item__status__in=['Deliverd', 'Return Requested'],
                order_item__created__range=[start_date, end_date]
            )
            
            
        # Calculate the discount for each sale
        for sale in sales:
            dis = sale.product.price - sale.price_now
            setattr(sale, 'dis', dis)

        # Render the template with the filtered sales data
        context = {'sales': sales}
        html_content = render(request, 'report.html', context).content.decode('utf-8')
        return render(request, 'report.html', {'html_content': html_content, 'sales': sales,'pdf': True})
    else:
        # Handle other HTTP methods if needed
        return redirect('dashboard')

@admin_required
def generate_pdf(request):
    html_content = request.POST.get('html_content')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')
    return response

@admin_required
def generate_excel(request):
    html_content = request.POST.get('html_content')
    
    # Parse the HTML content into a DataFrame using pandas
    tables = pd.read_html(html_content)
    if not tables:
        return HttpResponse("No tables found in HTML content.")
    
    # Select the first table (you may need to adjust this depending on your HTML structure)
    df = tables[0]

    # Create an in-memory stream for storing the Excel file
    output = BytesIO()

    # Write the DataFrame to an Excel file in the in-memory stream
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    # Set the appropriate headers for the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'
    
    # Write the Excel file content to the response
    output.seek(0)
    response.write(output.getvalue())

    return response