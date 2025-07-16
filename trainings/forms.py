from django import forms
from .models import Training

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
