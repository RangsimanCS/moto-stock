from django.shortcuts import render, redirect, get_object_or_404
from .models import Motorcycle, Inventory, Order, Profile
from .forms import (
    CustomUserCreationForm, UserProfileForm, ProfileForm,
    MotorcycleForm, InventoryForm
)
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import MotorcycleSerializer, InventorySerializer

# --- REST API ViewSets (DRF) พร้อมกำหนดสิทธิ์ความปลอดภัย ---
class MotorcycleViewSet(viewsets.ModelViewSet):
    queryset = Motorcycle.objects.all()
    serializer_class = MotorcycleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# --- หน้าแรก ยินดีต้อนรับ ---
def home_view(request):
    return render(request, 'showroom/home.html')

# --- ตรวจสอบสิทธิ์ Staff ---
def is_staff_user(user):
    return user.is_authenticated and user.is_staff

# --- ระบบสมัครสมาชิก เข้าสู่ระบบ และ ออกจากระบบ ---
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'ยินดีต้อนรับคุณ {user.username}! สมัครสมาชิกสำเร็จ')
            return redirect('bike_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'showroom/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('bike_list')
    else:
        form = AuthenticationForm()
    return render(request, 'showroom/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- ระบบจัดการข้อมูลรถ (CRUD) ---
def bike_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        bikes = Motorcycle.objects.filter(
            Q(brand__icontains=query) | Q(model_name__icontains=query)
        )
    else:
        bikes = Motorcycle.objects.all()

    paginator = Paginator(bikes, 5)
    page = request.GET.get('page')
    bikes_page = paginator.get_page(page)
    return render(request, 'showroom/bike_list.html', {'bikes': bikes_page, 'query': query})

@user_passes_test(is_staff_user, login_url='login')
def bike_create(request):
    form = MotorcycleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'เพิ่มข้อมูลรถสำเร็จ!')
        return redirect('bike_list')
    return render(request, 'showroom/bike_form.html', {'form': form})

@user_passes_test(is_staff_user, login_url='login')
def bike_update(request, pk):
    bike = get_object_or_404(Motorcycle, pk=pk)
    form = MotorcycleForm(request.POST or None, request.FILES or None, instance=bike)
    if form.is_valid():
        form.save()
        messages.success(request, 'แก้ไขข้อมูลรถสำเร็จ!')
        return redirect('bike_list')
    return render(request, 'showroom/bike_form.html', {'form': form})

@user_passes_test(is_staff_user, login_url='login')
def bike_delete(request, pk):
    bike = get_object_or_404(Motorcycle, pk=pk)
    if request.method == 'POST':
        bike.delete()
        messages.success(request, 'ลบข้อมูลรถเรียบร้อยแล้ว!')
        return redirect('bike_list')
    return render(request, 'showroom/bike_confirm_delete.html', {'bike': bike})

# --- ระบบจัดการสต็อกหน้าร้าน (CRUD) ---
def inventory_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        items = Inventory.objects.filter(
            Q(motorcycle__brand__icontains=query) | Q(motorcycle__model_name__icontains=query)
        )
    else:
        items = Inventory.objects.all()

    paginator = Paginator(items, 5)
    page = request.GET.get('page')
    items_page = paginator.get_page(page)
    return render(request, 'showroom/inventory_list.html', {'items': items_page, 'query': query})

@user_passes_test(is_staff_user, login_url='login')
def inventory_create(request):
    form = InventoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'เพิ่มสต็อกสินค้าสำเร็จ!')
        return redirect('inventory_list')
    return render(request, 'showroom/inventory_form.html', {'form': form})

@user_passes_test(is_staff_user, login_url='login')
def inventory_update(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    form = InventoryForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, 'แก้ไขสต็อกสินค้าสำเร็จ!')
        return redirect('inventory_list')
    return render(request, 'showroom/inventory_form.html', {'form': form})

@user_passes_test(is_staff_user, login_url='login')
def inventory_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'ลบสต็อกสินค้าเรียบร้อยแล้ว!')
        return redirect('inventory_list')
    return render(request, 'showroom/inventory_confirm_delete.html', {'item': item})

# --- ระบบชำระเงินผ่าน QR Code พร้อมเพย์ & บันทึกคำสั่งซื้อ ---
@login_required(login_url='login')
def checkout_view(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)
    if item.quantity <= 0 or item.status != 'Available':
        messages.error(request, 'ขออภัย สินค้ารายการนี้หมดแล้ว')
        return redirect('inventory_list')

    if request.method == 'POST':
        item.quantity -= 1
        if item.quantity == 0:
            item.status = 'Out of Stock'
        item.save()

        Order.objects.create(
            user=request.user,
            inventory=item,
            quantity=1,
            total_price=item.motorcycle.price
        )
        messages.success(request, f'ชำระเงินสำเร็จ! สั่งซื้อ {item.motorcycle.model_name} สี {item.color} เรียบร้อยแล้ว')
        return redirect('order_history')

    promptpay_number = "0812345679"
    return render(request, 'showroom/checkout.html', {
        'item': item,
        'promptpay_number': promptpay_number
    })

@login_required(login_url='login')
def order_history(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-order_date')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'showroom/order_history.html', {'orders': orders})

# --- ระบบดูและแก้ไขโปรไฟล์ผู้ใช้งาน ---
@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserProfileForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'อัปเดตข้อมูลโปรไฟล์และที่อยู่เรียบร้อยแล้ว!')
            return redirect('profile')
    else:
        u_form = UserProfileForm(instance=request.user)
        p_form = ProfileForm(instance=profile)

    return render(request, 'showroom/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    })