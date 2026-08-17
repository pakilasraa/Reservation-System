from django.urls import path
from . import views

app_name = 'reservation_app'

urlpatterns = [
    # Customer routes
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    # Table Category routes
    path('table-categories/', views.table_category_list, name='table_category_list'),
    path('table-categories/add/', views.table_category_create, name='table_category_create'),
    path('table-categories/<int:pk>/', views.table_category_detail, name='table_category_detail'),
    path('table-categories/<int:pk>/edit/', views.table_category_update, name='table_category_update'),
    path('table-categories/<int:pk>/delete/', views.table_category_delete, name='table_category_delete'),

    # Table routes
    path('tables/', views.table_list, name='table_list'),
    path('tables/add/', views.table_create, name='table_create'),
    path('tables/<int:pk>/', views.table_detail, name='table_detail'),
    path('tables/<int:pk>/edit/', views.table_update, name='table_update'),
    path('tables/<int:pk>/delete/', views.table_delete, name='table_delete'),

    # Reservation Status routes
    path('reservation-statuses/', views.reservation_status_list, name='reservation_status_list'),
    path('reservation-statuses/add/', views.reservation_status_create, name='reservation_status_create'),
    path('reservation-statuses/<int:pk>/edit/', views.reservation_status_update, name='reservation_status_update'),
    path('reservation-statuses/<int:pk>/delete/', views.reservation_status_delete, name='reservation_status_delete'),

    # Reservation routes
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/add/', views.reservation_create, name='reservation_create'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:pk>/edit/', views.reservation_update, name='reservation_update'),
    path('reservations/<int:pk>/cancel/', views.reservation_cancel, name='reservation_cancel'),

    # Payment routes
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
    path('payments/<int:pk>/edit/', views.payment_update, name='payment_update'),

    # Audit Log routes
    path('audit-logs/', views.audit_log_list, name='audit_log_list'),
    path('audit-logs/<int:pk>/', views.audit_log_detail, name='audit_log_detail'),
]