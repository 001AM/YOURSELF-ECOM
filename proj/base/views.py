from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Avg
from .models import Collection,Store,Prodtype,CustomUser,CartItem,Cart,Order,UserReview
from .forms import SortForm,FilterForm,CustomUserCreationForm,CustomUserChangeForm,ContactForm,ChangeDetailForm,CustomerReviewForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

import razorpay

def home(request):
    template ='base/home.html'
    collections = Collection.objects.all() 
    newarrivals = Store.objects.order_by('-created')
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
        
    else:
        cart_count= '0'
    context = {
        'collections': collections,
        'newarrivals': newarrivals,
        'cart_count':cart_count,
    }
    return render(request,template,context)



def store(request,pk=None,pk1=None):
    template ='base/store.html'
    form1 = SortForm(request.GET or None)
    form2 = FilterForm(request.GET or None)
    if form1.is_valid():
        q= request.GET.get('q')
       
        sort_by = form1.cleaned_data.get('sort_by')
        
        if q :
            
            stores = Store.objects.filter(collection__category=q)
            stores = stores.order_by(sort_by)
            pk = q 
            title=pk
        else:
            pk  = ''
            title=pk
            stores = Store.objects.all()
            stores = stores.order_by(sort_by)
    elif form2.is_valid():
        q= request.GET.get('q')
       
        choice_by = form2.cleaned_data.get('choice_by')
        
        if q :
            
            stores = Store.objects.filter(collection__category=q)
            stores = stores.filter(prodtype__product=choice_by)
            
            pk = q 
            title=pk
        else:
            pk  = ''
            title=pk
            stores = Store.objects.all()
            stores = stores.filter(prodtype__product=choice_by)
    else:
        if 'newarrival' == pk and not pk1:
            stores = Store.objects.order_by('-created')
            pk = ''
            title= pk
        elif pk and not pk1:
            stores = Store.objects.filter(collection__category=pk)
            title = pk
        elif pk1 and not pk:
            stores = Store.objects.filter(prodtype__product=pk1)
        elif pk and pk1:
            stores = Store.objects.filter(collection__category=pk, prodtype__product=pk1)
            title=pk+' '+pk1
        else:
            stores = Store.objects.order_by('?')
            pk = ''
            title=pk

        
    form1 = SortForm()
    form2 = FilterForm()
    collections = Collection.objects.all() 
    # prodtypes = Prodtype.objects.all()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    context ={
        'stores': stores,
        'collections': collections,
        'title':title,
        'pk1' : pk1,
        'form1':form1,
        'form2':form2,
        'cart_count':cart_count,
    }
    return render(request,template,context)

@login_required(login_url='login')
def add_to_cart(request, prod_name):
    product = get_object_or_404(Store, prod_name=prod_name)
    try:
        cart = request.user.cart  # Assuming you have a one-to-one relationship between User and Cart models
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    # Check if the product already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the product already exists in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def product(request,pk):
    template ='base/product.html'
    prods = Store.objects.filter(prod_name__exact=pk)
    collections = Collection.objects.all() 
    stores = Store.objects.order_by('?')
    store_reviews = UserReview.objects.filter(prod_name__prod_name=pk)
    reviews = store_reviews.order_by('?')[:3]
    newarrivals = stores.exclude(prod_name=pk)
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    if request.method == 'POST':
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Create an instance of the form but don't save it yet
            review.username= request.user# Set the username using request.user
            review.prod_name = Store.objects.get(prod_name=pk)  # Set the product name (replace with appropriate logic)
            review.save()  # Save the form data to the database
            return redirect(product,pk)  # Redirect to a success page or any other URL after successful submission
    else:
        form = CustomerReviewForm()
    # Calculate the average rating
    average_rating = store_reviews.aggregate(Avg('rating'))['rating__avg']

    # Check if the average rating exists
    if average_rating is not None:
        # Convert the average rating to a scale of 5
        average_rating_out_of_5 = (average_rating / 5.0) * 5

        # Update the product's average rating
        for prod in prods:
            prod.rating = average_rating_out_of_5
            prod.save()
    
    # Create a list to store the ratings
    rate = []
    prods = Store.objects.filter(prod_name__exact=pk)
    # Iterate over each store object in the queryset
    for store in prods:
        # Access the rating attribute of each store object
        rate.append(store.rating)
    ratings= int(''.join(map(str,rate)))
    ratings= range(ratings)

    context ={
        'stores':stores,
        'prods': prods,
        'collections': collections,
        'newarrivals': newarrivals,
        'cart_count':cart_count,
        'ratings':ratings,
        'reviews':reviews,
        'review_form':form
        
    }
    return render(request,template,context)


def search(request):
    template ='base/search.html'
    s = request.GET.get('s') if request.GET.get('s') != None else ''
    stores = Store.objects.filter(Q(prod_name__icontains=s ) | Q(prod_price__icontains=s) | Q(collection__category__icontains=s) | Q(prodtype__product__icontains=s))
    sort_form = SortForm(request.GET or None)
    filter_form = FilterForm(request.GET or None)
    if sort_form.is_valid():
        sort_by = sort_form.cleaned_data.get('sort_by')
        stores = stores.order_by(sort_by)
    elif filter_form.is_valid():
        choice_by = filter_form.cleaned_data.get('choice_by')
        stores = stores.filter(prodtype__product=choice_by)
    else:
        stores=stores
    collections = Collection.objects.all()
    sort_form = SortForm()
    filter_form = FilterForm()
    context ={
        'stores': stores,
        'collections': collections,
        'sort_form':sort_form,
        'filter_form':filter_form,
        's':s,
    }
    return render(request,template,context)

@login_required(login_url='login')
def userprofile(request):
    template='base/userprofile.html'
    user = request.user
    if request.method == 'POST':
        updateform = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if updateform.is_valid():
            updateform.save()
            

            return redirect('home')
        else:
            print(updateform.errors)
            messages.error(request, 'An error occurred during registration')
    collections = Collection.objects.all()
    page = 'userprof'
    updateform = CustomUserChangeForm(instance=user)
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    context={
        'collections':collections,
        'page':page,
        'updateform':updateform,
        'cart_count':cart_count,
    }
    return render(request,template,context)

@login_required(login_url='login')
def proflogout(request):
    template='base/userprofile.html'
    collections = Collection.objects.all()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    page = 'logout'
    context={
        'collections':collections,
        'page':page,
        'cart_count':cart_count,
    }
    return render(request,template,context)

@login_required(login_url='login')
def contactus(request):
    template='base/userprofile.html'
    page = 'contactus'
    collections = Collection.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            subject = f'New Contact Form Submission from {name} on {subject} from {email}'
            email = EmailMessage(
                subject,
                message,
                email,
                [settings.EMAIL_HOST_USER]

            )
            email.fail_silently=False
            email.send()
            return redirect('.')
    else:
        form = ContactForm()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    context={
        'collections':collections,
        'page':page,
        'form':form,
        'cart_count':cart_count,
    }
    return render(request,template,context)

@login_required(login_url='login')
def order(request):
    template='base/userprofile.html'
    collections = Collection.objects.all()
    orders = Order.objects.filter(user= request.user).order_by('-created')
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    page = 'order'
    RAZORPAY_API_KEY = settings.RAZORPAY_API_KEY
    context={
        'collections':collections,
        'page':page,
        'orders':orders,
        'cart_count':cart_count,
        'RAZORPAY_API_KEY':RAZORPAY_API_KEY
    }
    return render(request,template,context)

def register(request):
    template = 'base/login-register.html'
    if request.method == 'POST':
        signupform = CustomUserCreationForm(request.POST)
        if signupform.is_valid():
            user =  signupform.save()
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            errors = signupform.errors
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f"{field}: {error}")
            messages.error(request, 'An error occurred during registration')
    signupform= CustomUserCreationForm()
    collections = Collection.objects.all()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    context ={
        'signupform':signupform,
        'collections':collections,
        'cart_count':cart_count,
    }

    return render(request,template,context)

def loginUser(request):
    template='base/login-register.html'
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username =  request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist') 

        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    collections = Collection.objects.all()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    context = {
        'page': page,
        'collections':collections,
        'cart_count':cart_count,
    }
    return render(request, template, context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def cart(request):
    template = 'base/cart.html'
    user = request.user
    collections = Collection.objects.all() 
    cart = Cart.objects.get(user=user)
    
    # Get all the cart items associated with the cart
    cartitems = CartItem.objects.filter(cart=cart)
    cart_count = cartitems.count()
    total_price = sum(item.product.prod_price for item in cartitems)
    
    if request.method == 'POST':
        if cart.user == user:
            update_form = ChangeDetailForm(request.POST, instance=user)
            if update_form.is_valid():
                update_form.save()
            else:
                print(update_form.errors)
    else:
        update_form = ChangeDetailForm(instance=user)
            
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY , settings.RAZORPAY_API_SECRET))
    payment = client.order.create({
        'amount': max(total_price, 1) * 100,  # Amount in paise (e.g., Rs. 10.50 should be 1050)
        'currency': 'INR',
        'payment_capture': 1})
    
    cart.razor_pay_order_id = payment['id']
    cart.save()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    else:
        cart_count="0"
    context = {
        'collections': collections,
        'cartitems': cartitems,  
        'cart_count': cart_count, 
        'total_price': total_price,
        'payment': payment,
        'update_form': update_form,
        'cart_count': cart_count,
    }
    return render(request, template, context)

def payment(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    ord_user = Order.objects.create(user=user)
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.prod_price for item in cart_items)
    # Store the cart items as order items
    for cart_item in cart_items:
        ord_user.ord_prod.add(cart_item.product)
    ord_user.razor_pay_order_id = cart.razor_pay_order_id
    
    ord_user.is_paid = True
    ord_user.save()
    # Delete the cart items
    cart_items.delete()
    ord = Order.objects.get(razor_pay_order_id=ord_user.razor_pay_order_id)
    context={
        'user':user,
        'ord':ord,
        'total_price':total_price,
    }
    template =render_to_string('pdfs/order.html',context)
    subject=f'Your Order Confirmation - Order ID: {ord_user.razor_pay_order_id}'
    useremail = user.email
    email = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,
        [useremail]

    )
    email.fail_silently=False
    email.send()
    return redirect('order')
    
def paymentfailure(request):
    template ='base/fail.html'
    collections = Collection.objects.all() 

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitems = CartItem.objects.filter(cart=cart)
            cart_count = cartitems.count()
        except Cart.DoesNotExist:
            cart_count= '0'
            pass
    context = {
        'collections': collections,
        'cart_count':cart_count,
    }
    return render(request,template,context)
@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if cart_item.cart.user == request.user:
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return JsonResponse({'success': False, 'message': 'Unauthorized'})

def invoice(request, q):
    template = "pdfs/invoice.html"
    ord_obj = Order.objects.get(razor_pay_order_id=q)
    total_price = sum(item.prod_price for item in ord_obj.ord_prod.all())
    context = {
        'ord': ord_obj,
        'total_price': total_price
    }
    return render(request, template, context)
