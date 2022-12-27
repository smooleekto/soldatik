"""soldat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from app.views import reply_add, CustomLoginView, ResetPasswordView, ChangePasswordView, productsadd, productdelete, productupdate, comment_delete, decline_offer, accept_offer, delete_offer
from app.forms import LoginForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('app.urls')),

    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='app/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('sell/', productsadd, name='app-sell'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path(r'delete_product/<int:product_id>', productdelete, name='app-delete'),
    path(r'delete_comment/<int:comment_id>', comment_delete, name='app-delete_comment'),
    path(r'reply_add/<int:comment_id>', reply_add, name='app-reply_add'),
    path(r'decline_offer/<int:product_bid_id>', decline_offer, name='app-decline_offer'),
    path(r'delete_offer/<int:product_bid_id>', delete_offer, name='app-delete_offer'),
    path(r'accept_offer/<int:product_bid_id>', accept_offer, name='app-accept_offer'),
    path('update_product/<int:product_id>', productupdate, name='app-productupdate'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
