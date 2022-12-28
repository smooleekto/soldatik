from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile, Products, Comments, Replies, ProductsBid, Orders

USER_TYPES = (
    ("1", "Customer"),
    ("2", "Vendor"),
)

class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    user_type = forms.ChoiceField(choices=USER_TYPES)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class UpdateProductForm(forms.ModelForm):
    name = forms.CharField(max_length=40,
                               required=True,)
    quantity = forms.IntegerField(required=True)
    price = forms.FloatField(required=True)

    class Meta:
        model = Products
        fields = ['name', 'quantity', 'price']


class AddProduct(forms.ModelForm):
    price = forms.FloatField()
    name = forms.CharField(max_length=20)
    quantity = forms.IntegerField()
    description = forms.TextInput()
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'photo']

class CommentForm(forms.ModelForm):
    MARKS = [('1','1'), ('2', '2'),  ('3', '3'),  ('4', '4') , ('5', '5')]
    comment = forms.CharField(required=False,
    widget=forms.Textarea(attrs={'rows': 2, 'cols':20, 'style':'resize:none;', 'maxlength':'140'}))
    mark = forms.CharField(label='Mark', widget=forms.RadioSelect(choices=MARKS))
    class Meta:
        model = Comments
        fields = ['mark', 'comment']


class BidForm(forms.ModelForm):
    new_price = forms.FloatField()
    quantity = forms.IntegerField()
    class Meta:
        model = ProductsBid
        fields = ['new_price', 'quantity']


class OrderForm(forms.ModelForm):
    post_office = forms.CharField(max_length=40)
    customer_first_name = forms.CharField(max_length=40)
    customer_last_name = forms.CharField(max_length=40)
    customer_phone = forms.CharField(max_length=40)
    class Meta:
        model = Orders
        fields = ['post_office', 'customer_first_name', 'customer_last_name', 'customer_phone']

class RepliesForm(forms.ModelForm):
    comment = comment = forms.CharField(required=True,
    widget=forms.Textarea(attrs={'rows': 2, 'cols':20, 'style':'resize:none;', 'maxlength':'140'}))
    class Meta:
        model = Replies
        fields = ['comment']