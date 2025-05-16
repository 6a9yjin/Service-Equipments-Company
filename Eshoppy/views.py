from django.shortcuts import render,redirect,HttpResponse
from .import models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')
def admin_dashboard(request):
    pro = models.Product.objects.all()
    feedbacks = models.Feedback.objects.select_related('product', 'user').all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {'pro': pro, 'feedbacks': feedbacks})

def logout(request):
    request.session.flush()
    return redirect('index')

def register(request):
    if request.method=='POST':
        try:
            name=request.POST.get('Name')
            email=request.POST.get('Email')
            phone=request.POST.get('Phone')
            password=request.POST.get('Password')
            age=request.POST.get('Age')
            gender=request.POST.get('Gender')
            address=request.POST.get('Address')
            if models.Register.objects.filter(email=email).exists():
                alert = "<script>alert('Email already exists'); window.location.href='/register/'; </script>"
                return HttpResponse(alert)
            models.Register.objects.create(name=name,email=email,phone=phone,password=password,age=age,gender=gender,address=address)
            alert = "<script>alert('Registration succesfull'); window.location.href='/login/'; </script>"
            return HttpResponse(alert)
        except models.Register.DoesNotExist:
            alert = "<script>alert('User not found'); window.location.href='/register/'; </script>"
            return HttpResponse(alert)
    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'hehe@gmail.com' and password == 'Hehe@1234!':
            request.session['email'] = email
            request.session['is_admin'] = True
            alert = "<script> alert('Admin login successful'); window.location.href='/admin_dashboard/'; </script>"
            return HttpResponse(alert)
        elif models.Register.objects.filter(email=email, password=password).exists():
            request.session['email'] = email
            request.session['is_admin'] = False
            alert = "<script> alert('Login successful'); window.location.href='/home/'; </script>"
            return HttpResponse(alert)
        else:
            alert = "<script> alert('Invalid credentials'); window.location.href='/login/'; </script>"
            return HttpResponse(alert)
    else:
        return render(request, 'login.html')


def profile(request):
    email = request.session['email']
    user = models.Register.objects.get(email=email)
    return render(request,'profile.html',{'user':user})

def edit(request):
    email = request.session['email']
    user = models.Register.objects.get(email=email)
    if request.method=='POST':
        name=request.POST.get('Name')
        user.name = name
        phone=request.POST.get('Phone')
        user.phone = phone
        age=request.POST.get('Age')
        user.age = age
        gender=request.POST.get('Gender')
        user.gender = gender
        address=request.POST.get('Address')
        user.address = address
        user.save()
        return redirect('profile')
    return render(request,'edit.html',{'user':user})

def addproduct(request):
    if request.method=='POST':
        name=request.POST.get('Name')
        category=request.POST.get('Category')
        photo=request.FILES.get('Photo')
        price=request.POST.get('Price')
        quantity=request.POST.get('Quantity')
        availability=request.POST.get('Availability')
        models.Product.objects.create(name=name,category=category,photo=photo,price=price, quantity=quantity, availability=availability)
        alert = "<script>alert('Product added successfully'); window.location.href='/productlist/'; </script>"
        return HttpResponse(alert)
    return render(request,'addproduct.html')

def productlist(request):
    pro=models.Product.objects.all()
    return render(request,'productlist.html',{'pro':pro})

def editproduct(request,id):
    user = models.Product.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get('Name')
        user.name = name
        category=request.POST.get('Category')
        user.category = category
        photo=request.FILES.get('Photo')
        if photo:  # Only update if a new image is uploaded
            user.photo = photo
        price=request.POST.get('Price')
        user.price = price
        quantity=request.POST.get('Quantity')
        user.quantity = quantity
        availability=request.POST.get('Availability')
        user.availability = availability
        user.save()
        return redirect('productlist')
    else:
        return render(request,'editproduct.html',{'user':user})
    
def deleteproduct(request,id):
    product = models.Product.objects.get(id=id).delete()
    return redirect('productlist')

# In your views.py
from django.shortcuts import render

def manage_users_view(request):
    users = models.Register.objects.all()  # Fetch all users
    return render(request, 'manage_users.html', {'users': users})

def editusers(request):
    user = models.Register.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get('Name')
        user.name = name
        email=request.POST.get('Email')
        user.email = email
    user.save()
    return redirect('manage_users')


def delete_user(request, id):
    try:
        user = models.Register.objects.get(id=id)
        user.delete()
        return redirect('manage_users')
    except models.Register.DoesNotExist:
        return HttpResponse("<script>alert('User not found'); window.location.href='/manage_users/';</script>")

def adminproduct(request):
    pro=models.Product.objects.all()
    return render(request,'adminproduct.html',{'pro':pro})

def product_list(request):
    # Fetch all available products
    pro = models.Product.objects.all()
    return render(request, 'product_list.html', {'pro': pro})


def validate_registration(data):
    errors = []

    if not register.match(r'^[A-Za-z\s]+$', data.get('Name', '')):
        errors.append("Name must contain only letters and spaces.")

    email = data.get('Email', '')
    if not register.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net)$', email):
        errors.append("Invalid email format.")

    phone = data.get('Phone', '')
    if not register.match(r'^\d{10}$', phone):
        errors.append("Phone number must be exactly 10 digits.")

    if not data.get('PhoneCode'):
        errors.append("Country code is required.")

    if len(data.get('Password', '')) < 6:
        errors.append("Password must be at least 6 characters.")

    try:
        age = int(data.get('Age', 0))
        if age < 13 or age > 120:
            errors.append("Enter a valid age between 13 and 120.")
    except ValueError:
        errors.append("Age must be a number.")

    if data.get('Gender') not in ["Male", "Female"]:
        errors.append("Select a valid gender.")

    address = data.get('Address', '')
    if len(address) < 10 or len(address) > 70:
        errors.append("Address must be between 10 and 70 characters.")

    return errors

def register_view(request):
    if request.method == 'POST':
        errors = validate_registration(request.POST)
        if errors:
            return render(request, 'register.html', {'errors': errors})
        return HttpResponse("Registration successful!")
    return render(request, 'register.html')

from .models import Feedback, Product, Register

def submit_feedback(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        email = request.session.get('email')

        if not rating and not comment:
            messages.error(request, 'Please rate or write a comment before submitting feedback.')
            return redirect('product_list')

        if email and product_id:
            try:
                user = Register.objects.get(email=email)
                product = Product.objects.get(id=product_id)

                Feedback.objects.create(
                    user=user,
                    product=product,
                    rating=int(rating) if rating else 0,
                    comment=comment if comment else None
                )
                messages.success(request, 'Feedback submitted successfully.')
            except Exception as e:
                print("Error:", e)
                messages.error(request, 'Error saving feedback.')
        else:
            messages.error(request, 'Session expired or product not found.')

    return redirect('product_list')

def add_cart(request, pid):
    if 'email' in request.session:
        email = request.session.get('email')
        us = models.Register.objects.get(email=email)
        products = models.Product.objects.get(id=pid)

        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            if quantity is None or not quantity.isdigit():
                # handle invalid or missing quantity
                return render(request, 'cart.html', {'prd': products, 'error': 'Please enter a valid quantity.'})

            quantity = int(quantity)
            total_price = products.price * quantity

            cart_item, created = models.cart.objects.get_or_create(
                user=us,
                products=products,
                defaults={'quantity': quantity, 'total_price': total_price}
            )
            if not created:
                cart_item.quantity = quantity
                cart_item.total_price = total_price
                cart_item.save()

            return redirect('product_list')
        else:
            return render(request, 'cart.html', {'prd': products})
    else:
        return redirect('login')
    
def cart_view(request):
    if 'email' in request.session:
        email=request.session['email']
        user=models.Register.objects.get(email=email)
        cart = models.cart.objects.filter(user=user)
        return render(request, 'cart_view.html', {'cart': cart})
    return redirect('login')


import razorpay
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt

def initiate_payment(request,cid):
    email = request.session['email']
    if email:
        crt=models.cart.objects.get(id=cid)
        am=crt.total_price
        amount = int(am)*100 
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment_order['id']
        user = models.Register.objects.get(email=email)
        buyer_data = {
            'buyer': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'product_dtls': crt.id
                # Add other fields as needed
            }
        }
        response_data = {'order_id': order_id, 'amount': amount}
        response_data.update(buyer_data)
        return JsonResponse(response_data, encoder=DjangoJSONEncoder)
    else:
        return redirect('login')
    

from decimal import Decimal   
@csrf_exempt
def confirm_payment(request, order_id, payment_id,crti_id):
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    try:
        payment = client.payment.fetch(payment_id)
        print('payment', payment)
        if payment['order_id'] == order_id and payment['status'] == 'captured':
            pemail = payment.get('email')
            amount = payment.get('amount')
            crt_id= payment.get('crtid')
            print("cf",crt_id)
            amount_in_rupees = Decimal(amount) / Decimal(100)  

            if pemail:
                usr = models.Register.objects.get(email=pemail)
                crts=models.cart.objects.get(id=crti_id)
                prd=crts.products
                trns=models.Transaction(user=usr,products=prd,amount=amount_in_rupees,quantity=crts.quantity,order_id=order_id)
                trns.save()
                crts.delete()
                return redirect('product_list')

            else:
                return JsonResponse({'status': 'failure', 'error': 'User email not found'})
    except Exception as e:
        print('Error:', str(e))
        return redirect('home')