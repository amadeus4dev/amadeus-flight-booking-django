# 베이스 이미지로 Python 3.10 사용
FROM python:3.10

# 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# requirements.txt를 컨테이너에 복사
COPY requirements.txt .

# FastAPI 애플리케이션 실행에 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# FastAPI 애플리케이션 실행 (uvicorn 사용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
