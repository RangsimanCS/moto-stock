import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Motorcycle, Inventory, Profile

# 1. ฟอร์มจัดการข้อมูลรถมอเตอร์ไซค์
class MotorcycleForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        fields = ['brand', 'model_name', 'engine_cc', 'price', 'image', 'description']
        labels = {
            'brand': 'แบรนด์',
            'model_name': 'ชื่อรุ่น',
            'engine_cc': 'พิกัด (CC)',
            'price': 'ราคา (บาท)',
            'image': 'รูปรถ',
            'description': 'รายละเอียด'
        }
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น Wave 110i'}),
            'engine_cc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'เช่น 110'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'เช่น 45000'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# 2. ฟอร์มจัดการสต็อกรถ
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['motorcycle', 'color', 'quantity', 'status']
        labels = {
            'motorcycle': 'รถมอเตอร์ไซค์',
            'color': 'สี',
            'quantity': 'จำนวน (คัน)',
            'status': 'สถานะ'
        }
        widgets = {
            'motorcycle': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น แดง, ดำ'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

# 3. ฟอร์มสมัครสมาชิก (รหัสผ่านอย่างน้อย 8 ตัว มีทั้งตัวอักษรและตัวเลข)
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 8:
                raise ValidationError("รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร")
            if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
                raise ValidationError("รหัสผ่านต้องประกอบด้วยตัวอักษรและตัวเลข")
        return password

# 4. ฟอร์มแก้ไขข้อมูลผู้ใช้ (ชื่อ-นามสกุล, อีเมล)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'ชื่อจริง',
            'last_name': 'นามสกุล',
            'email': 'อีเมล'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# 5. ฟอร์มโปรไฟล์ส่วนตัว (เบอร์โทร, ที่อยู่, รูปโปรไฟล์)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_pic']
        labels = {
            'phone': 'เบอร์โทรศัพท์',
            'address': 'ที่อยู่จัดส่ง / ติดต่อ',
            'profile_pic': 'รูปโปรไฟล์'
        }
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น 0812345678'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'บ้านเลขที่ ถนน ตำบล อำเภอ จังหวัด'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'})
        }

# ใส่เผื่อไว้สำหรับชื่อเดิมที่ views.py เคยเรียกหา
class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'})
        }