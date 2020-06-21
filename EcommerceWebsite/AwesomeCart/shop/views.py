from django.shortcuts import render
from django.http import HttpResponse
from .models import product,contactus_table,Order,OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    allprods=[]
    category_product=product.objects.values('category') #to fetch each category column and its values from database
    #this will create a list of dictionary
    #column name will be key and its value will be value
    # print(category_product)
    # print("\n")

    category_values={item['category'] for item in category_product} #creating a set of only values of category.
    #so that we dont get duplicate values.
    # print(category_values)
    # print("\n")

    for cat in category_values:
        product_data=product.objects.filter(category=cat) #fetching those products having category stored in the category_values
        # print(product_data)
        no_of_products=len(product_data) #length of each category's products.
        # print(no_of_products)
        no_of_slides=no_of_products//4 + ceil((no_of_products/4)-(no_of_products//4))
        allprods.append([product_data,range(1,no_of_slides),no_of_slides])

    param={'allprods':allprods}


    # param={'no_of_slides':no_of_slides,'range':range(1,no_of_slides),'data':product_data}
    return render(request,'shop/index.html',param)

def aboutus(request):
    return render(request,'shop/aboutus.html')

def contactus(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contactus_data=contactus_table(name=name,email=email,phone=phone,desc=desc) #to create a query
        contactus_data.save() #to store in database

        thank=True #flag for if data stored is succesful
        id = contactus_data.msg_id #order id of the order placed, fetching it from database
        return render(request,'shop/contactus.html',{'thank':thank,'id':id})
    return render(request,'shop/contactus.html')

def search(request):
    return render(request,'shop/search.html')

def productview(request,myid):
    #fetching product details using id
    product_data = product.objects.filter(id=myid)
    print(product_data)
    param={'products':product_data[0]}

    return render(request,'shop/productview.html',param)

def checkout(request):
    if request.method=="POST":
        items_json=request.POST.get('items_json','')
        amount=request.POST.get('amount','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','') + " " +  request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        pin_code=request.POST.get('pin_code','')
        phone=request.POST.get('phone','')

        order=Order(items_json=items_json,amount=amount,name=name,email=email,address=address,city=city,state=state,zip_code=pin_code, phone=phone) #to create a query
        order.save() #to store in database
        addOrderUpdate = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed.")
        #whenever an order will be placed, we will store its id in OrderUpdate table as well for tracking purpose.
        addOrderUpdate.save()
        thank=True #flag for order is placed
        id = order.order_id #order id of the order placed, fetching it from database
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')

def track(request):
    if request.method=="POST":
        order_id=request.POST.get('order_id','')
        email=request.POST.get('email','')
        try:
            ordercheck=Order.objects.filter(order_id=order_id,email=email) #fetching entered order id is available or not
            print('hello')
        
            if len(ordercheck) > 0: #if we get order data from database
                fetchupdates=OrderUpdate.objects.filter(order_id=order_id) #fetching all updates of order id
                print(fetchupdates)
                updates_list=[] #a list where we will store description and timestamp of orders
                for item in fetchupdates:
                    updates_list.append({'text':item.update_desc,'time':item.timestamp}) #creating dictionary
                    json_obj = json.dumps([updates_list,ordercheck[0].items_json],default=str) #converting python dictionary into json object
                return HttpResponse(json_obj)
            else:
                return HttpResponse('{}') #if no order is found, we will send blank 
        except Exception as e: #if there is any problem in transporting, this exception will generate
            return HttpResponse(f'{e}')
        
    return render(request,'shop/track.html')