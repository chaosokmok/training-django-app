from django import forms
from .models import Training
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'
        labels = {
            'course_name': '📘 ชื่อหลักสูตรอบรม',
            'course_type': '🏷️ ประเภทการอบรม',
            'hours': '⏱️ จำนวนชั่วโมง',
            'date': '📅 วันที่อบรม',
            'certificate': '📁 ไฟล์วุฒิบัตร (PDF/JPG/PNG)',
        }
        help_texts = {
            'certificate': 'รองรับไฟล์ PDF, JPG หรือ PNG เท่านั้น',
        }
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control shadow-sm',
                'type': 'date',
                'autocomplete': 'off'
            }, format='%Y-%m-%d'),

            'course_name': forms.Textarea(attrs={
                'class': 'form-control-modern textarea-auto-resize w-100',
                'rows': 1,
                'style': 'width: 100%;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']

class RegistrationForm(forms.Form):
    name = forms.CharField(
        label='ชื่อ-นามสกุล', 
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'กรอกชื่อของคุณ',
            'autocomplete': 'name'
        }),
        error_messages={
            'required': 'กรุณากรอกชื่อ-นามสกุล',
            'max_length': 'ชื่อ-นามสกุลยาวเกินไป (ไม่เกิน 100 ตัวอักษร)'
        }
    )
    
    email = forms.EmailField(
        label='อีเมล', 
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'example@email.com',
            'autocomplete': 'email'
        }),
        error_messages={
            'required': 'กรุณากรอกอีเมล',
            'invalid': 'รูปแบบอีเมลไม่ถูกต้อง'
        }
    )
    
    password = forms.CharField(
        label='รหัสผ่าน', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'รหัสผ่าน',
            'autocomplete': 'new-password'
        }), 
        min_length=6, 
        required=True,
        help_text='รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร',
        error_messages={
            'required': 'กรุณากรอกรหัสผ่าน',
            'min_length': 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
        }
    )
    
    confirm_password = forms.CharField(
        label='ยืนยันรหัสผ่าน', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'ยืนยันรหัสผ่าน',
            'autocomplete': 'new-password'
        }), 
        required=True,
        error_messages={
            'required': 'กรุณายืนยันรหัสผ่าน'
        }
    )
    
    # Phone validator for Thai phone numbers
    phone_validator = RegexValidator(
        regex=r'^(\+66|0)[0-9]{8,9}$',
        message='รูปแบบเบอร์โทรไม่ถูกต้อง (เช่น 081234567หรือ +6681234567)'
    )
    
    tel = forms.CharField(
        label='เบอร์โทรศัพท์', 
        max_length=20, 
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '08xxxxxxxx',
            'autocomplete': 'tel'
        }),
        help_text='(ไม่บังคับ) รูปแบบ: 08xxxxxxxx หรือ +66xxxxxxxx'
    )
    
    bio = forms.CharField(
        label='เกี่ยวกับฉัน', 
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3,
            'placeholder': 'แนะนำตัวคุณให้เราได้รู้จัก...',
            'style': 'resize: vertical;'
        }), 
        required=False,
        max_length=500,
        help_text='แนะนำตัวคุณให้เราได้รู้จัก (ไม่บังคับ, ไม่เกิน 500 ตัวอักษร)'
    )

    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 2:
                raise forms.ValidationError("ชื่อ-นามสกุลต้องมีอย่างน้อย 2 ตัวอักษร")
            
            # Check for valid characters (allow Thai, English, spaces, and common punctuation)
            if not re.match(r'^[a-zA-Zก-๙\s\.\-]+$', name):
                raise forms.ValidationError("ชื่อ-นามสกุลมีตัวอักษรที่ไม่อนุญาต")
        
        return name

    def clean_email(self):
        """Validate email field and check for duplicates"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            
            # Check if email already exists (case-insensitive)
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("อีเมลนี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")
            
            # Additional email validation
            if email.count('@') != 1:
                raise forms.ValidationError("รูปแบบอีเมลไม่ถูกต้อง")
                
        return email

    def clean_password(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password')
        if password:
            # Check password strength
            if len(password) < 6:
                raise forms.ValidationError("รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร")
            
            # Optional: Add more password strength requirements
            strength_score = 0
            feedback = []
            
            if len(password) >= 8:
                strength_score += 1
            else:
                feedback.append("อย่างน้อย 8 ตัวอักษร")
                
            if re.search(r'[a-z]', password):
                strength_score += 1
            else:
                feedback.append("ตัวอักษรเล็ก")
                
            if re.search(r'[A-Z]', password):
                strength_score += 1
            else:
                feedback.append("ตัวอักษรใหญ่")
                
            if re.search(r'\d', password):
                strength_score += 1
            else:
                feedback.append("ตัวเลข")
                
            if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
                strength_score += 1
            else:
                feedback.append("อักขระพิเศษ")
            
            # Require at least medium strength (3/5)
            if strength_score < 3:
                raise forms.ValidationError(
                    f"รหัสผ่านไม่แข็งแกร่งพอ ต้องการ: {', '.join(feedback)}"
                )
        
        return password

    def clean_tel(self):
        """Validate phone number"""
        tel = self.cleaned_data.get('tel')
        if tel:
            tel = tel.strip()
            # Remove spaces and dashes
            tel = re.sub(r'[\s\-]', '', tel)
            
            # Convert Thai format to international format
            if tel.startswith('0'):
                tel = '+66' + tel[1:]
            elif not tel.startswith('+66'):
                if len(tel) == 9:  # Assuming 9 digits without country code
                    tel = '+66' + tel
                    
        return tel

    def clean_bio(self):
        """Clean and validate bio field"""
        bio = self.cleaned_data.get('bio')
        if bio:
            bio = bio.strip()
            if len(bio) > 500:
                raise forms.ValidationError("เกี่ยวกับฉันยาวเกินไป (ไม่เกิน 500 ตัวอักษร)")
        return bio

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")

        # Check password confirmation
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน")
        
        # Check if password contains name or email
        if password and name:
            if name.lower() in password.lower():
                self.add_error('password', "รหัสผ่านไม่ควรมีชื่อของคุณ")
                
        if password and email:
            email_name = email.split('@')[0].lower()
            if email_name in password.lower():
                self.add_error('password', "รหัสผ่านไม่ควรมีส่วนของอีเมล")
        
        return cleaned_data

    def save(self):
        """Create user from form data"""
        cleaned_data = self.cleaned_data
        
        # Create user
        user = User.objects.create_user(
            username=cleaned_data['email'],  # Use email as username
            email=cleaned_data['email'],
            password=cleaned_data['password'],
            first_name=cleaned_data['name']
        )
        
        # You can extend this to save additional fields to a UserProfile model
        # if you have one set up
        
        return user