from django.db import models
from django.contrib.auth.models import User

class Motorcycle(models.Model):
    BRAND_CHOICES = [
        ('Honda', 'Honda'), 
        ('Kawasaki', 'Kawasaki'), 
        ('Yamaha', 'Yamaha'), 
        ('KTM', 'KTM'), 
        ('Other', 'Other')
    ]
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name='แบรนด์')
    model_name = models.CharField(max_length=200, verbose_name='ชื่อรุ่น')
    engine_cc = models.IntegerField(verbose_name='พิกัด (CC)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ราคา (บาท)')
    image = models.ImageField(upload_to='bikes/', blank=True, null=True, verbose_name='รูปรถ')
    description = models.TextField(blank=True, verbose_name='รายละเอียด')
    
    def __str__(self):
        return f"{self.brand} {self.model_name}"

class Inventory(models.Model):
    STATUS_CHOICES = [
        ('Available', 'พร้อมขาย'), 
        ('Reserved', 'จองแล้ว'), 
        ('Out of Stock', 'สินค้าหมด')
    ]
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, verbose_name='รถมอเตอร์ไซค์')
    color = models.CharField(max_length=50, verbose_name='สี')
    quantity = models.IntegerField(default=0, verbose_name='จำนวน (คัน)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available', verbose_name='สถานะ')

    def __str__(self):
        return f"{self.motorcycle.brand} {self.motorcycle.model_name} (สี {self.color}) - เหลือ {self.quantity} คัน"

# ตารางประวัติการสั่งซื้อ
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ผู้สั่งซื้อ')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name='รายการสต็อก')
    quantity = models.PositiveIntegerField(default=1, verbose_name='จำนวนที่ซื้อ')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='ราคารวม')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='วันที่สั่งซื้อ')

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ซื้อ {self.inventory.motorcycle.model_name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="เบอร์โทรศัพท์")
    address = models.TextField(blank=True, null=True, verbose_name="ที่อยู่")
    profile_pic = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True, null=True, verbose_name="รูปโปรไฟล์")

    def __str__(self):
        return f"โปรไฟล์ของ {self.user.username}"

    def __str__(self):
        return f"Profile ของ {self.user.username}"