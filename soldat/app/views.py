from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required
from .forms import UpdateProductForm, RegisterForm, RepliesForm, LoginForm, UpdateUserForm, UpdateProfileForm, AddProduct, CommentForm, BidForm, OrderForm
from .models import Products, Profile, Comments, Replies, ProductsBid, Orders, ProductsOrders
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from cart.forms import CartAddProductForm
from cart.cart import Cart


def home(request):
    products = Products.objects.all()
    user_group = Group.objects.all()
    users = Profile.objects.all()
    product_form = CartAddProductForm
    cart = Cart(request)
    return render(request, 'app/home.html', {'cart':cart,   'products':products, 'user_group':user_group, 'product_form': product_form, 'users':users})



class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'app/register.html'
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(username=username, password=password)
            vendors = Group.objects.get(name='vendors')
            customers = Group.objects.get(name='customers')  
            if user_type == '1':
                user.groups.add(customers)
                messages.success(request, f'Account created for customer {username}')
            elif user_type == '2':
                user.groups.add(vendors)
                messages.success(request, f'Account created for vendor {username}')
            profile = Profile()
            profile.bio = ''
            profile.user_id = User.objects.last().id
            profile.save()
            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app/password_reset.html'
    email_template_name = 'app/password_reset_email.html'
    subject_template_name = 'app/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('app-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'app/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('app-home')


@login_required
def profile(request):
    bids = ProductsBid.objects.all()
    prupdateform = UpdateProductForm()
    users = User.objects.all()
    orders = Orders.objects.all()
    productsorders = ProductsOrders.objects.all()
    user_group = Group.objects.all()
    products = Products.objects.all()
    totals = []
    for item in Orders.objects.all():
        count = 0
        foo = ProductsOrders.objects.filter(order_id_id=item.order_id)
        for x in foo:
            count += int(x.price)
        totals.append([item.order_id, count])
        
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='app-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'app/profile.html', 
    {'user_form': user_form, 
    'users': users,
    'bids': bids,
    'profile_form': profile_form, 
    'products': products, 
    'user_group': user_group,
    'orders': orders,
    'productsorders': productsorders,
    'totals': totals,
    'prupdateform':prupdateform})



def productsadd(request):
    error = ''
    if request.method == 'POST':
        productform = AddProduct(request.POST, request.FILES)
        if productform.is_valid():
            to_db = Products()
            to_db.price = productform.cleaned_data['price']
            to_db.name = productform.cleaned_data['name']
            to_db.photo = productform.cleaned_data['photo']
            to_db.quantity = productform.cleaned_data['quantity']
            if to_db.quantity or to_db.price < 0 :
                messages.error(request, f'Amount must be positive')
                return redirect(to='/sell')
            to_db.description = productform.cleaned_data['description']
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            to_db.vendor_id = user
            to_db.save()
            return redirect(to='/')
        else:
            messages.success(request, f'{productform}')
            
    
    productform = AddProduct()

    data = {
        'productform': productform,
        'error': error,
    }
    return render(request, 'app/sell.html', data)


def productupdate(request, product_id):
    product = Products.objects.get(pk=product_id)
    productform = UpdateProductForm(request.POST)
    if request.method == 'POST' and 'btn-prupd' in request.POST:
        productform = UpdateProductForm(request.POST)
        if productform.is_valid():
            updname = productform.cleaned_data['name']
            updquantity = productform.cleaned_data['quantity']
            updprice = productform.cleaned_data['price']

            Products.objects.filter(product_bid_id=product_id).update(name=updname)
            Products.objects.filter(product_bid_id=product_id).update(quantity=updquantity)
            Products.objects.filter(product_bid_id=product_id).update(price=updprice)
            return redirect('app-profile')
    return render(request, 'app/profile.html', {'productform':productform})


def productdelete(request, product_id):
    product = Products.objects.get(pk=product_id)
    product.delete()
    messages.success(request, ("Product Deleted!!"))
    return redirect('app-profile')


def comment_delete(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    page_id = comment.product_id_id
    comment.delete()
    messages.success(request, ("Comment Deleted!!"))
    return redirect(f'/product_details/{page_id}')


def reply_add(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    page_id = comment.product_id_id
    reply_form = RepliesForm(request.POST)
    print('qweqweqwewqewqeqqqqqqqqqqqqq  ')
    if request.method == 'POST' and 'btn-reply' in request.POST:
        reply_form = RepliesForm(request.POST)
        if reply_form.is_valid():
            to_db = Replies()
            to_db.comment = reply_form.cleaned_data['comment']
            to_db.comment_id = comment_id
            to_db.user_id = User.objects.get(id=request.user.id)
            to_db.save()
            return redirect(f'/product_details/{page_id}')


def product_details(request, product_id):
    details_id = int(request.path.split('/')[-2])
    product = Products.objects.get(product_id=product_id)
    products = Products.objects.all()
    users = User.objects.all()
    comments = Comments.objects.all()
    replies = Replies.objects.all()
    comment_form = CommentForm()
    bid_form = BidForm()
    reply_form = RepliesForm(request.POST)
    comment_count = Comments.objects.filter(product_id_id=details_id).count()
    if request.method == 'POST' and 'btn-comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            to_db = Comments()
            to_db.mark = comment_form.cleaned_data['mark']
            to_db.comment = comment_form.cleaned_data['comment']
            to_db.product_id = Products.objects.get(product_id=details_id)
            to_db.customer_id = User.objects.get(id=request.user.id)
            to_db.save()
            return HttpResponseRedirect(request.path_info)
    if request.method == 'POST' and 'btn-offer' in request.POST:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            to_db = ProductsBid()
            to_db.new_price = bid_form.cleaned_data['new_price']
            to_db.quantity = bid_form.cleaned_data['quantity']
            if to_db.quantity or to_db.price < 0 :
                messages.error(request, f'Amount must be positive')
                return HttpResponseRedirect(request.path_info)
            to_db.product_id = Products.objects.get(product_id=details_id)
            to_db.customer_id = User.objects.get(id=request.user.id)
            to_db.vendor_id = product.vendor_id
            to_db.save()
            return HttpResponseRedirect(request.path_info)
    return render(request, 'app/product_details.html', 
    {'product': product,
    'products': products,
    'users': users,
    'comments': comments,
    'replies': replies,
    'comment_form': comment_form,
    'details_id': details_id, 
    'comment_count': comment_count,
    'bid_form': bid_form,
    'reply_form': reply_form})

def decline_offer(request, product_bid_id):
    ProductsBid.objects.filter(product_bid_id=product_bid_id).update(status='Declined')
    messages.success(request, ("Offer has been declined!"))
    return redirect('app-profile')


def delete_offer(request, product_bid_id):
    offer = ProductsBid.objects.filter(product_bid_id=product_bid_id)
    offer.delete()
    messages.success(request, ("Offer has been deleted!"))
    return redirect('app-profile')


def accept_offer(request, product_bid_id):
    ProductsBid.objects.filter(product_bid_id=product_bid_id).update(status='Accepted')
    messages.success(request, ("Offer has been accepted!"))
    return redirect('app-profile')


def order_page(request):
    cart = Cart(request)
    orderform = OrderForm(request.POST)
    print(request.user)
    if request.method == 'POST':
        if orderform.is_valid():
            to_db = Orders()
            to_db.post_office = orderform.cleaned_data['post_office']
            to_db.customer_first_name = orderform.cleaned_data['customer_first_name']
            to_db.customer_last_name = orderform.cleaned_data['customer_last_name']
            to_db.customer_phone = orderform.cleaned_data['customer_phone']
            if to_db.customer_phone[0:4] != '+380' or len(to_db.customer_phone) !=11:
                messages.error(request, f'Phone example: +3807771133')
                return HttpResponseRedirect(request.path_info)
            to_db.vendor_id = User.objects.get(id=list(cart)[0].get('product').vendor_id_id)
            to_db.status = 'Waiting for sending'
            if request.user.is_anonymous == False:
                user_id = request.user.id
                user = User.objects.get(id=user_id)
                to_db.customer_id = user
            else:
                user_id = User.objects.get(id=6).id
                user = User.objects.get(id=user_id)
                to_db.customer_id = user
            to_db.save()
            order_id = to_db.order_id
            for item in list(cart):
                to_db = ProductsOrders()
                to_db.product_id = Products.objects.get(product_id=item.get('product').product_id)
                to_db.quantity = item.get('quantity')
                to_db.price = item.get('total_price')
                to_db.order_id_id = order_id
                to_db.save()
                newquantity = Products.objects.get(product_id=item.get('product').product_id).quantity - item.get('quantity')
                Products.objects.filter(product_id=item.get('product').product_id).update(quantity=newquantity)
            return redirect(to='app-profile')
    return render(request, 'app/order_page.html',
    {'cart': cart,
    'orderform': orderform})

def order_bid(request, order_bid_id):
    orderform = OrderForm(request.POST)
    bid = ProductsBid.objects.get(product_bid_id=order_bid_id)
    if request.method == 'POST':
        if orderform.is_valid():
            to_db = Orders()
            to_db.post_office = orderform.cleaned_data['post_office']
            to_db.customer_first_name = orderform.cleaned_data['customer_first_name']
            to_db.customer_last_name = orderform.cleaned_data['customer_last_name']
            to_db.customer_phone = orderform.cleaned_data['customer_phone']
            if to_db.customer_phone[0:4] != '+380' or len(to_db.customer_phone) !=11 :
                messages.error(request, f'Phone example: +3807771133')
                return redirect(to='/sell')
            to_db.vendor_id = User.objects.get(id=bid.vendor_id_id)
            to_db.status = 'Waiting for sending'
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            to_db.customer_id = user
            to_db.save()
            order_id = to_db.order_id
            to_db = ProductsOrders()
            to_db.product_id = Products.objects.get(product_id=bid.product_id_id)
            to_db.quantity = bid.quantity
            to_db.price = bid.new_price * bid.quantity
            to_db.order_id_id = order_id
            to_db.save()
            newquantity = Products.objects.get(product_id=bid.product_id_id).quantity - bid.quantity
            Products.objects.filter(product_id=bid.product_id_id).update(quantity=newquantity)
            return redirect(to='app-profile')
    total = bid.new_price*bid.quantity
    return render(request, 'app/order_bid_page.html',
    {'orderform': orderform,
    'bid':bid,
    'total':total})


def order_status(request, order_id):
    Orders.objects.filter(order_id=order_id).update(status='On the way')
    return redirect('app-profile')