from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-book/', views.upload_book, name='upload_book'),
    path('upload-notes/', views.upload_notes, name='upload_notes'),
    path('search/', views.search_resources, name='search_resources'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('users/', views.user_list, name='user_list'),
    path('inbox/', views.chat_inbox, name='chat_inbox'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/order/<int:book_id>/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path('request-book/', views.request_book, name='request_book'),
    path('book-requests/', views.list_book_requests, name='list_book_requests'),
    path('', views.home_view, name='home'),
]
