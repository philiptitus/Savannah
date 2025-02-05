from django.urls import path
from .views import RegisterAdmin, CreateProduct, CreateOrder, AverageProductPrice, CreateCategory
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name="main.html")),
    path('register-admin/', RegisterAdmin.as_view(), name='register-admin'),
    path('products/', CreateProduct.as_view(), name='create-product'),
    path('orders/', CreateOrder.as_view(), name='create-order'),
    path('categories/', CreateCategory.as_view(), name='create-category'),
    path('categories/<int:category_id>/average-price/', AverageProductPrice.as_view(), name='average-product-price'),
]