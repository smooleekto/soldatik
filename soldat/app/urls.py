from django.urls import path
from .views import order_bid, home, profile, RegisterView, productsadd, productupdate, product_details, order_page, order_status
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='app-home'),
    path('register/', RegisterView.as_view(), name='app-register'),
    path('profile/', profile, name='app-profile'),
    path('sell/', productsadd, name='app-sell'),
    path('order/', order_page, name='app-order_page'),
    path('order_bid/<int:order_bid_id>', order_bid, name='app-order_bid'),
    path('order_status/<int:order_id>/', order_status, name='app-order_status'),
    path('update_product/<product_id>', productupdate, name='app-productupdate'),
    path('product_details/<int:product_id>/', product_details, name='app-productdetails'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
