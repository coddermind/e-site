from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Product,Order,OTP
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# Create your views here.

def index(request):
    all_products = Product.objects.all()
    product_ids_list = []

    # Get the order for the current user that hasn't been placed yet
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        order_ids=order_items.product_id.split(",")
        for i in order_ids:
            product_ids_list.append(int(i))
    except:
        pass
    
    # code for searching
    item_name=request.GET.get("item_name")
    if item_name!='' and item_name is not None:
        all_products=all_products.filter(name__icontains=item_name)

    # code for pagination
    paginator=Paginator(all_products,4) # 4 products per page
    page=request.GET.get("page")
    all_products=paginator.get_page(page)

    context = {
        "all_products": all_products,
        "product_ids_list": product_ids_list,
        "count_products":len(product_ids_list),
    }

    return render(request, "index.html", context)


def shop(request):
    all_products = Product.objects.all()
    category_list=[]
    product_ids_list = []

    for i in all_products:
        if i.category not in category_list:
            category_list.append(i.category)

    # Get the order for the current user that hasn't been placed yet
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        order_ids=order_items.product_id.split(",")
        for i in order_ids:
            product_ids_list.append(int(i))
    except:
        pass
    
    # code for searching
    search_var=None
    item_name=request.GET.get("item_name")
    if item_name!='' and item_name is not None:
        all_products=all_products.filter(name__icontains=item_name)
        search_var=item_name

    category=request.GET.get("category")
    if category!="all" and category is not None:
        all_products=all_products.filter(category__icontains=category)
            
        

    # code for pagination
    paginator=Paginator(all_products,40) # 40 products per page
    page=request.GET.get("page")
    all_products=paginator.get_page(page)

    context = {
        "all_products": all_products,
        "product_ids_list": product_ids_list,
        "count_products":len(product_ids_list),
        "category_list":category_list,
        "search_var":search_var,
    }

    return render(request, "shop.html", context)

def details(request, id):
    product = get_object_or_404(Product, id=id)
    product_ids_list = []

    
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        order_ids=order_items.product_id.split(",")
        for i in order_ids:
            product_ids_list.append(int(i))
    except:
        pass

    context = {
        "product": product,
        "product_ids_list": product_ids_list,
    }
    return render(request, "details.html", context)


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        str_ids.append(str(product.id))
        str_name.append(product.name)
        str_price.append(str(product.price))
        str_quantity.append("1")

        order_items.product_id=",".join(str_ids)
        order_items.product_name=",".join(str_name)
        order_items.product_price=",".join(str_price)
        order_items.product_quantity=",".join(str_quantity)
        order_items.save()

    except:
        order_items=Order.objects.create(
            user=request.user,
            product_name=product.name,
            product_id=str(product.id),
            product_price=product.price,
            product_quantity="1"
        )
        order_items.save()

    return redirect("index")

@login_required
def remove_from_cart(request, id):
    product = get_object_or_404(Product, id=id)

    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        index_id=str_ids.index(str(product.id))

        str_ids.pop(index_id)
        str_name.pop(index_id)
        str_price.pop(index_id)
        str_quantity.pop(index_id)

        if len(str_ids)>0:
            order_items.product_id=",".join(str_ids)
            order_items.product_name=",".join(str_name)
            order_items.product_price=",".join(str_price)
            order_items.product_quantity=",".join(str_quantity)
            order_items.save()
        else:
            order_items.delete()

    except:
        pass

    return redirect("index")




@login_required
def cart(request):
    all_products=Product.objects.all()
    try:

        if request.method=="POST":
            for key,value in request.POST.items():
                if key.startswith("quantity_"):
                    product_id=key.split("_")[1]

                    update_quantity=str(value)

                    order_items=get_object_or_404(Order,user=request.user,order_placed=False)
                    str_ids=order_items.product_id.split(",")
                    str_quantity=order_items.product_quantity.split(",")

                    ind=str_ids.index(str(product_id))
                    str_quantity[ind]=update_quantity

                    order_items.product_quantity=",".join(str_quantity)
                    order_items.save()



        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        int_ids=[]
        int_price=[]
        int_quantity=[]
        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))

        d={
            "ids":int_ids,
            "quantity":int_quantity
        }

        zipped_data=zip(d["ids"],d["quantity"])

    except:
        order_items=None
        all_products=None
        zipped_data=None

    context={
        "all_products":all_products,
        "cart_products":zipped_data if zipped_data else None
    }

    
    return render(request, 'cart.html', context)

@login_required
def delivery_details(request):
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        if request.method=="POST":
            phone=request.POST.get("phone")
            address=request.POST.get("address")
            order_items.phone=phone
            order_items.address=address
            order_items.email=request.user.email
            order_items.order_date=timezone.now()
            order_items.save()

            return redirect("order_summary")
    except:
        order_items=None
    return render(request,"delivery_details.html")


@login_required
def order_summary(request):
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))
            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        gross_total=sum(total_ind_price)

        

        d={
            "ids":int_ids,
            "name":str_name,
            "price":int_price,
            "total_price":total_ind_price,
            "quantity":int_quantity
        }

        zipped_data=zip(d["ids"],d["name"],d["price"],d["total_price"],d["quantity"])

        first_name=request.user.first_name
        last_name=request.user.last_name
        email=order_items.email
        phone=order_items.phone
        address=order_items.address
        order_id=f"ODRNO00{order_items.id}"
        date=order_items.order_date
    except:
        order_items=None
        zipped_data=None
        first_name=None
        last_name=None
        email=None
        phone=None
        address=None
        order_id=None
        date=None
        gross_total=None

    context={
        "zipped_data":zipped_data,
        "first_name":first_name,
        "last_name":last_name,
        "email":email,
        "phone":phone,
        "address":address,
        "order_id":order_id,
        "date":date,
        "gross_total":gross_total
    }

    if zipped_data:
        subject="Your Order Summary"
        html_content=render_to_string("order_summary_new.html",context)
        text_data=strip_tags(html_content)
        from_email=settings.EMAIL_HOST_USER
        to_email=email

        email = EmailMultiAlternatives(subject, text_data, from_email=from_email, to=[to_email])
        email.attach_alternative(html_content,"text/html")
        email.send()

    return redirect("order_summary_new")

@login_required
def order_summary_new(request):
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))
            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        gross_total=sum(total_ind_price)

        

        d={
            "ids":int_ids,
            "name":str_name,
            "price":int_price,
            "total_price":total_ind_price,
            "quantity":int_quantity
        }

        zipped_data=zip(d["ids"],d["name"],d["price"],d["total_price"],d["quantity"])

        first_name=request.user.first_name
        last_name=request.user.last_name
        email=order_items.email
        phone=order_items.phone
        address=order_items.address
        order_id=f"ORDNO00C{order_items.id}"
        date=order_items.order_date

        # set order_placed is True
        order_items.order_placed=True
        order_items.save()

        
    except:
        order_items=None
        zipped_data=None
        first_name=None
        last_name=None
        email=None
        phone=None
        address=None
        order_id=None
        date=None
        gross_total=None

    context={
        "zipped_data":zipped_data,
        "first_name":first_name,
        "last_name":last_name,
        "email":email,
        "phone":phone,
        "address":address,
        "order_id":order_id,
        "date":date,
        "gross_total":gross_total
    }

    return render(request,"order_summary_new.html",context)



# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string

# @login_required
# def order_summary(request):
#     # Your existing code to retrieve order details

#     subject = f"Order Summary - {user_products.id}"
#     from_email = EMAIL_HOST_USER
#     to_email = [request.user.email]

#     # Render email template with context data
#     html_content = render_to_string('order_confirmation_email.html', {'user': request.user})

#     # Create email message
#     msg = EmailMultiAlternatives(subject, '', from_email, to_email)
#     msg.attach_alternative(html_content, "text/html")

#     try:
#         # Send email
#         msg.send()
#         # Mark order as placed
#         user_products.order_placed = True
#         user_products.save()
#     except Exception as e:
#         print(e)

#     # Return your existing render statement
#     return render(request, "order_summary.html", context)









# def register_user(requst):
#     if requst.method=="POST":
#         form=CustomUserCreationForm(requst.POST)
#         if form.is_valid():
#             form.save()
#             # user=form.save(commit=False)
#             # user.save()
#             return redirect("index")
#     else:
#         form=CustomUserCreationForm()
#     context={"form":form}
#     return render(requst,"register_user.html",context)





# Other imports...

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Send email confirmation
            otp = random.randint(100000, 999999)

            user_obj = get_object_or_404(User, username=form.cleaned_data.get("email"))
            instance = OTP.objects.create(user=user_obj, otp=otp)
            instance.save()
            
            # Sending Mail with otp
            mail_subject = 'Activate your account'
            message = f"{otp}"
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[to_email])
            email.send()
            
            return redirect('registration_confirmation')
    else:
        form = CustomUserCreationForm()
    

    return render(request, 'register_user.html', {'form': form})

# First, delete expired OTPs and associated user accounts
expired_records = OTP.objects.filter(timestamp__lte=timezone.now() - timedelta(minutes=5))
for record in expired_records:
    user = record.user
    user.delete()

expired_records.delete()

def registration_confirmation(request):
    # First, delete expired OTPs and associated user accounts
    expired_records = OTP.objects.filter(timestamp__lte=timezone.now() - timedelta(minutes=5))
    for record in expired_records:
        user = record.user
        user.delete()

    expired_records.delete()

    user_obj = None
    if request.method == "POST":
        otp = request.POST.get("otp")
        
        try:
            otp_obj = get_object_or_404(OTP, otp=otp)
            user_id = otp_obj.user_id
            user_obj = get_object_or_404(User, id=user_id)
            
            
            user_obj.is_active = True
            user_obj.save()
            otp_obj.delete()
        except:
            return redirect("otp_failed")
    
    context = {"user_obj": user_obj}

    return render(request, 'registration_confirmation.html', context)

def otp_failed(request):
    return render(request,"otp_failed.html")

def login_user(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            next_url = request.POST.get('next', 'index')
            return redirect(next_url)
    else:
        form=AuthenticationForm()
    context={"form":form,'next':request.GET.get('next','')}
    return render(request,"login_user.html",context)

def logout_user(request):
    logout(request)
    return redirect("login_user")