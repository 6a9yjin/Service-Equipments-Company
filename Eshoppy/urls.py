from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('productlist/', views.productlist, name='productlist'),
    path('logout/', views.logout, name='logout'),
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('edit/',views.edit,name='edit'),
    path('home/',views.home,name='home'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:id>/', views.deleteproduct, name='deleteproduct'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_users/', views.manage_users_view, name='manage_users'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('product_list/', views.product_list, name='product_list'),
    path('register/', views.register_view, name='register'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),

    path('add_cart/<int:pid>/',views.add_cart,name='add_cart'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('initiate-payment/<cid>/',views.initiate_payment,name='initiate_payment'),
    path('confirm-payment/<order_id>/<payment_id>/<crti_id>/',views.confirm_payment,name='confirm-payment'),

]