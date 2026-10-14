from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ตั้งค่า DefaultRouter สำหรับ REST API
router = DefaultRouter()
router.register(r'bikes', views.MotorcycleViewSet, basename='api_bikes')
router.register(r'inventory', views.InventoryViewSet, basename='api_inventory')

urlpatterns = [
    # 1. หน้าร้านค้าหลัก (Home)
    path('', views.home_view, name='home'),

    # 2. REST API Endpoints (ขึ้นต้นด้วย /api/)
    path('api/', include(router.urls)),

    # 3. จัดการข้อมูลรถ (Bike CRUD)
    path('bikes/', views.bike_list, name='bike_list'),
    path('bikes/add/', views.bike_create, name='bike_create'),
    path('bikes/<int:pk>/edit/', views.bike_update, name='bike_update'),
    path('bikes/<int:pk>/delete/', views.bike_delete, name='bike_delete'),

    # 4. จัดการสต็อกหน้าร้าน (Inventory CRUD)
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/edit/', views.inventory_update, name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),

    # 5. ระบบสมาชิกและคำสั่งซื้อ
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('checkout/<int:inventory_id>/', views.checkout_view, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
]