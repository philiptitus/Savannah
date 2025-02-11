from django.urls import path
from .views import *
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name="main.html")),
    path('r-admin/', TemplateView.as_view(template_name="register_admin.html"), name='make-admin'),
    path('create-product/', TemplateView.as_view(template_name="create_product.html"), name='make-product'),
    path('create-order/', TemplateView.as_view(template_name="create_order.html"), name='make-order'),
    path('average-price/', TemplateView.as_view(template_name="average_product_price.html"),  name='make-average'),
    path('auth-view/', AuthView.as_view(), name='auth-view'),  # Add this line
    path('create-category/', TemplateView.as_view(template_name="create_category.html"), name='make-category'),
    path('register-admin/', RegisterAdmin.as_view(), name='register-admin'),
    path('products/', CreateProduct.as_view(), name='create-product'),
    path('orders/', CreateOrder.as_view(), name='create-order'),
    path('categories/', CreateCategory.as_view(), name='create-category'),
    path('product-list/', ProductList.as_view(), name='product-list'),  # Add this line
    path('category-list/', CategoryList.as_view(), name='category-list'),  # Add this line
    path('average-product-price/', AverageProductPrice.as_view(), name='average-product-price'),  # Update this line
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-page/', TemplateView.as_view(template_name="login.html"), name='login-page'),  # Add this line
    path('register-page/', TemplateView.as_view(template_name="register.html"), name='register-page'),  # Add this line

]