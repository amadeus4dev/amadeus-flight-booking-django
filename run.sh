#!/bin/bash

# 환경 변수 설정
set -a
source ./flight-booking.env
set +a

# Conda 환경 활성화
echo "[*] Conda 환경 활성화 전: $(which python)"
conda activate flight
conda init
echo "[*] Conda 환경 활성화 후: $(which python)"

pip install -r requirements.txt

# 경로 확인
echo "[*] 현재 경로: $(pwd)"

# Django 명령 실행
cd ./amadeus_demo_api
python manage.py migrate
cd ../
python amadeus_demo_api/manage.py runserver 0.0.0.0:8000
