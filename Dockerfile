# Python 3.10-slim 이미지를 기반으로 설정
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . .

RUN python manage.py collectstatic --noinput

# 컨테이너 포트 8000 노출
EXPOSE 8000

# gunicorn으로 Django 앱 실행
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
