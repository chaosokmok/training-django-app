import os
from urllib.request import pathname2url
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Training
from .forms import TrainingForm
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Profile 
from .forms import RegistrationForm
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login




@login_required
def training_list(request):
    trainings = Training.objects.all().order_by('-date')

    q = request.GET.get('q', '')
    course_type = request.GET.get('type', '')
    date_str = request.GET.get('date', '')

    if q:
        trainings = trainings.filter(course_name__icontains=q)

    if course_type:
        trainings = trainings.filter(course_type=course_type)

    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            trainings = trainings.filter(date=date_obj)
        except ValueError:
            pass

    # เดือนภาษาไทยแบบย่อ
    months_th = [
        "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
        "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]

    # แปลงวันที่เป็น "วัน เดือน(ย่อ) ปี พ.ศ." และผูกเป็น attribute ใหม่ชื่อ thai_date
    for t in trainings:
        if t.date:
            day = t.date.day
            month = months_th[t.date.month]
            year = t.date.year + 543  # แปลงปี ค.ศ. -> พ.ศ.
            t.thai_date = f"{day} {month} {year}"
        else:
            t.thai_date = ""

    types = [t[0] for t in Training.COURSE_TYPES]

    return render(request, 'trainings/training_list.html', {
        'trainings': trainings,
        'types': types,
    })



@login_required
def training_create(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('training_list')
    else:
        form = TrainingForm()
    return render(request, 'trainings/training_form.html', {'form': form})


@login_required
def training_dashboard(request):
    all_trainings = Training.objects.values('course_type').annotate(total=Sum('hours'))
    chart_data = {t['course_type']: t['total'] for t in all_trainings}

    def get_total_by_type(type_keyword):
        return Training.objects.filter(course_type__icontains=type_keyword).aggregate(total=Sum('hours'))['total'] or 0

    context = {
        'chart_data': chart_data,
        'digital_hours': get_total_by_type('ทักษะดิจิทัล'),
        'position_hours': get_total_by_type('สมรรถนะ'),
        'risk_hours': get_total_by_type('ความเสี่ยง'),
        'total_hours': sum(chart_data.values()),
    }
    return render(request, 'trainings/dashboard.html', context)


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    if uri.startswith('/static/'):
        path = os.path.join(settings.BASE_DIR, 'trainings', 'static', uri.replace('/static/', '').replace('/', os.sep))
        if not os.path.isfile(path):
            raise Exception(f'Media URI must exist: {path}')
        return path
    elif uri.startswith('/media/'):
        path = os.path.join(settings.BASE_DIR, 'media', uri.replace('/media/', '').replace('/', os.sep))
        if not os.path.isfile(path):
            raise Exception(f'Media URI must exist: {path}')
        return path
    return uri


@login_required
def preview_pdf(request):
    trainings = Training.objects.all()
    template_path = 'trainings/pdf_template.html'

    # path ฟอนต์ภาษาไทยจริง ๆ
    font_path = os.path.join(settings.BASE_DIR, 'trainings', 'static', 'trainings', 'fonts', 'THSarabunNew.ttf')
    if not os.path.isfile(font_path):
        raise Exception(f"Font file not found: {font_path}")

    font_uri = 'file:///' + pathname2url(font_path)

    context = {
        'trainings': trainings,
        'font_path': font_uri,  # ต้องตรงกับใน template pdf_template.html
    }

    html = get_template(template_path).render(context)
    response = HttpResponse(content_type='application/pdf')

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse(f'เกิดข้อผิดพลาดในการสร้าง PDF<br><pre>{html}</pre>')
    return response


@require_POST
def training_delete(request, pk):
    training = get_object_or_404(Training, pk=pk)
    training.delete()
    messages.success(request, f'ลบหลักสูตร "{training.course_name}" เรียบร้อยแล้ว')
    return redirect('training_list')

@login_required
def training_edit(request, pk):
    training = get_object_or_404(Training, pk=pk)

    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, 'อัปเดตข้อมูลเรียบร้อยแล้ว')
            return redirect('training_edit', pk=pk)  # กลับมาหน้าเดิม
    else:
        form = TrainingForm(instance=training)

    # เดือนภาษาไทยแบบย่อ
    months_th = [
        "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
        "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]

    # แปลงวันที่ของ training เพียงรายการเดียว
    if training.date:
        day = training.date.day
        month = months_th[training.date.month]
        year = training.date.year + 543
        thai_date = f"{day} {month} {year}"
    else:
        thai_date = ""

    return render(request, 'trainings/training_edit.html', {
        'form': form,
        'training': training,
        'thai_date': thai_date,
    })

