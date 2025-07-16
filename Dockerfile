# ใช้ Python แบบบางเบา
FROM python:3.11-slim

# ห้าม cache pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# โฟลเดอร์ใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt แล้วติดตั้ง
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# คัดลอกไฟล์โปรเจกต์ทั้งหมด
COPY . /app/

# ✅ รวบรวม static files
RUN python manage.py collectstatic --noinput

# ✅ เปิด port
EXPOSE 8000

# ✅ ใช้ gunicorn รัน Django
CMD ["gunicorn", "training_project.wsgi:application", "--bind", "0.0.0.0:8000"]
