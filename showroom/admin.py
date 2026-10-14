from django.contrib import admin
from .models import Motorcycle, Inventory

# ปรับแต่งหน้าตา Admin ให้ดูข้อมูลรถง่ายขึ้น
class MotorcycleAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model_name', 'engine_cc', 'price']
    search_fields = ['model_name', 'brand']
    list_filter = ['brand']

# ปรับแต่งหน้าตา Admin ให้ดูสต็อกง่ายขึ้น
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['motorcycle', 'color', 'quantity', 'status']
    list_filter = ['status']
    search_fields = ['motorcycle__model_name']

admin.site.register(Motorcycle, MotorcycleAdmin)
admin.site.register(Inventory, InventoryAdmin)