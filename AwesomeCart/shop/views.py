from django.shortcuts import render
from django.http import HttpResponse
from .models import product,contactus_table,Order,OrderUpdate
from math import ceil
import json
from paytmfolder import Checksum
MERCHANT_KEY = '__I12u_i59uD5h37'
#eliminating csrf token for paytm post request
from django.views.decorators.csrf import csrf_exempt 

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

def searchMatch(searchquery,item):
    if searchquery in item.product_name.lower() or searchquery in item.category.lower() or searchquery in item.desc.lower():
        return True
    else:
        return False

def search(request):
    searchquery= request.GET.get('search')
    allprods=[] #blank list
    category_product=product.objects.values('category') #to fetch each category column and its values from database
    category_values={item['category'] for item in category_product} #creating a set of only values of category.

    for cat in category_values:
        product_datatemp=product.objects.filter(category=cat) #fetching those products having category stored in the category_values
        #we are adding items in the list that have matched with searched query.
        searchitem=[item for item in product_datatemp if searchMatch(searchquery,item)]
        no_of_products=len(searchitem) #length of each category's products.
        no_of_slides=no_of_products//4 + ceil((no_of_products/4)-(no_of_products//4))
        if no_of_products != 0:
            allprods.append([searchitem,range(1,no_of_slides),no_of_slides])

    param={'allprods':allprods,"msg": ""}
    if len(allprods) == 0 or len(searchquery)<2:
        param = {'msg': "Please make sure to enter relevant search query"}
    return render(request,'shop/search.html',param)

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
        #return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        # Request paytm to transfer the amount to your account after payment by user
        # CwWJeb23811036683351, WorldP64425807474247
        param_dict = {
                'MID': 'LrqHyG13540583068310',             
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'DIYtestingweb',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict':param_dict})
    return render(request,'shop/checkout.html')

def track(request):
    if request.method=="POST":
        order_id=request.POST.get('order_id','')
        email=request.POST.get('email','')
        try:
            ordercheck=Order.objects.filter(order_id=order_id,email=email) #fetching entered order id is available or not
        
            if len(ordercheck) > 0: #if we get order data from database
                fetchupdates=OrderUpdate.objects.filter(order_id=order_id) #fetching all updates of order id from orderupdate table
                #print(fetchupdates)
                updates_list=[] #a list where we will store description and timestamp of orders
                for item in fetchupdates: #storing values in updates_list from fetchupdates
                    updates_list.append({'text':item.update_desc,'time':item.timestamp}) #creating list of dictionaries
                    json_obj = json.dumps({"status":"success","updates":updates_list,"itemsJson":ordercheck[0].items_json},default=str) #converting python dictionary into json object
                return HttpResponse(json_obj) #sending json to html file.
            else:
                return HttpResponse('{"status":"noitem"}') #if no order is found, we will send blank 
        except Exception as e: #if there is any problem in transporting, this exception will generate
            return HttpResponse({"status":"error"})
        
    return render(request,'shop/track.html')

@csrf_exempt
def handlerequest(request):
    #paytm will send post request after transaction
    form=request.POST #storing data in form variable
    response_dict={} #dictionary for storing key, values 
    for i in form.keys(): 
        response_dict[i]=form[i] #storing data in response_dict
        if i=='CHECKSUMHASH': 
            checksumvar=form[i] #storing value of checksumhash in checksumvar

    #to check whether transaction was not attacked by hacker
    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksumvar)
    if verify:
        if response_dict['RESPCODE']=='01':
            print('order successful')
        else:
            #if order is unsuccess, printing with error
            print('order was not successful because '+ response_dict['RESPMSG']) 
    print(response_dict)
    return render(request, 'shop/paymentstatus.html',{'response':response_dict})        



def paytm(request):
    pass