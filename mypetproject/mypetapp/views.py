from typing import Any
from django.shortcuts import render,redirect
from .models import Pet, Customer, Cart, Order, Orderdetail, Payment
from django.http import HttpResponse
from django.views.generic import DeleteView,UpdateView,DetailView,ListView,CreateView
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from datetime import date
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class petview(ListView):
    model= Pet
    template_name = 'petview.html'
    context_object_name = 'petobj'

    def get_context_data(self, **kwargs):
        try:
            data = self.request.session['sessionvalue']
            context = super().get_context_data(**kwargs)
            context['sessionvalue'] = data
            return context
        except:
            context = super().get_context_data(**kwargs)


class petdetail(DetailView):
    model=Pet
    template_name='PetDetail.html'
    context_object_name = 'i'

class petviewcm(ListView):
    template_name= 'petview.html'
    context_object_name ='petobj'

def petviewcmfun(request):
    petdetails = Pet.cpetobj.getdata('dog')
    return render(request,'petview.html',{'petobj':petdetails})   


def search(request):
    if request.method == "POST":
        session = request.session['sessionvalue']
        searchdata = request.POST.get('searchquery')
        petobj = Pet.objects.filter(Q(name__icontains = searchdata) | Q(breeds__icontains = searchdata) | Q(species__icontains = searchdata))
        return render(request, 'petview.html',{'petobj': petobj, 'session':session})


def register(request):
    if request.method == "GET":
        return render(request, 'resigter.html')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        espassword = make_password(password)

        cutobj = Customer(name = name, password = espassword, email=email, phoneno=phoneno)
        cutobj.save()
        return redirect('../login/')
    


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('user')
        print(username)
        pass1 = request.POST.get('pass1')
        print(pass1)

        cust = Customer.objects.filter(email = username)
        if cust:
            custobj = Customer.objects.get(email=username)

            flag = check_password(pass1,custobj.password)

            if flag:
                request.session['sessionvalue'] = custobj.email
                return redirect('../petview/')
            else:
                return render(request,'login.html',{'msg':'Incorrect username and Password'})
            
        else:
            return render(request,'login.html',{'msg':'Incorrect username and Password'})
        

class petdetail(DetailView):
    model = Pet
    template_name = 'viewdetail.html'
    context_object_name = 'i'

def addtocart(request):
    productid = request.POST.get('productid')
    try:
        custsession = request.session['sessionvalue']
        custobj = Customer.objects.get(email = custsession)
        custid = custobj.id
        probj = Pet.objects.get(id = productid)

        flag = Cart.objects.filter(cid = custobj.id, pid = probj.id)
        if flag:
            cartobj = Cart.objects.get(cid = custobj.id, pid = probj.id)
            cartobj.quanity = cartobj.quanity +1
            cartobj.totalamount = probj.price * cartobj.quanity
            cartobj.save()
        else:
            cartobj = Cart(cid = custobj, pid = probj, quanity = 1, totalamount = probj.price*1)
            cartobj.save()
        
        return redirect('../petview/')
    except:
        return redirect('../login/')
    

def viewcart(request):
    custsession = request.session['sessionvalue'] #email of customer
    custobj = Customer.objects.get(email = custsession) 
    cartobj = Cart.objects.filter(cid = custobj.id)

    return render(request,'cart.html',{'cartobj':cartobj , 'session': custsession})

def cq(request):
    cemail = request.session["sessionvalue"]
    pid = request.POST.get('pid')
    print(pid)
    custobj = Customer.objects.get(email = cemail)
    pobj = Pet.objects.get(id = pid)
    cartobj = Cart.objects.get(cid = custobj.id, pid = pobj.id)
    print(cartobj)
    if request.POST.get('changequantitybtn') == "+":
        cartobj.quanity = cartobj.quanity + 1
        print(cartobj.quanity)
        cartobj.totalamount = cartobj.quanity * pobj.price
        cartobj.save()

    elif request.POST.get('changequantitybtn') == "-":
        if cartobj.quanity == 1:
            cartobj.delete()
        else:
            cartobj.quanity = cartobj.quanity - 1
            cartobj.totalamount = cartobj.quanity * pobj.price
            cartobj.save()

    return redirect('../viewcart/')


def summary(request):
    custsession = request.session["sessionvalue"]
    custobj = Customer.objects.get(email = custsession)
    cartobj = Cart.objects.filter(cid = custobj.id)
    totalbill = 0
    for i in cartobj:
        totalbill = i.totalamount + totalbill

    return render(request, "summary.html", {'session': custsession, 'cartobj': cartobj, 'totalbill': totalbill})


def placeorder(request):
    if request.method == "POST":
        fn = request.POST.get('fn')
        ln = request.POST.get('ln')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phoneno = request.POST.get('phoneno')

        datev = date.today()
        # print(datev.date)
        orderobj = Order(firstname = fn, lastname = ln, address = address, city = city, state = state, pincode = pincode, phoneno = phoneno, orderdate = datev, orderstatus = 'pending')
        orderobj.save()

        ono = str(orderobj.id) + str(datev).replace('-', '')
        orderobj.ordernumber = ono
        orderobj.save()

        custsession = request.session["sessionvalue"]
        custobj = Customer.objects.get(email = custsession)
        cartobj = Cart.objects.filter(cid = custobj.id)
        totalbill = 0
        for i in cartobj:
            totalbill = i.totalamount + totalbill

        from django.core.mail import EmailMessage

        sm = EmailMessage('order placed', 'order placed from pet store application. Total bill for your order is '+str(totalbill),to=['singhachintya43@gmail.com'])
        sm.send()
        
        
        
        
        # authorize razorpay client with API Keys.
        razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    

        currency = 'INR'
        amount = 20000  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '../PetView'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request,'payment.html',{'orderobj':orderobj,'session':custsession,'cartobj':cartobj,'totalbill':totalbill,'context':context})

def success(request):
    orderid = request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    request.session['sessionvalue'] = request.GET.get('session')
    usersession = request.session['sessionvalue']
    customerobj = Customer.objects.get(email=usersession)
    cartobj = Cart.objects.filter(cid = customerobj.id)

    orderobj = Order.objects.get(ordernumber = orderid)
    paymentobj = Payment(transactionid = tid, paymentstatus='paid',customerid=customerobj,oid = orderobj)
    paymentobj.save()
    for i in cartobj:
        orderdetailobj = Orderdetail(paymentid = paymentobj,ordernumber = orderid, productid = i.pid,customerid = i.cid,quantity = i.quanity,totalprice = i.totalamount)
        orderdetailobj.save()
        i.delete()
    
    return render(request,'success.html',{'session':usersession,'payobj':paymentobj})



def logout(request):
    del (request.session['sessionvalue'])
    return redirect('../login/')


   

