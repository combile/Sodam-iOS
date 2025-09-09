FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 데이터베이스 디렉토리 생성
RUN mkdir -p instance

# 포트 노출
EXPOSE 5000

# 환경 변수 설정
ENV FLASK_APP=run_server.py
ENV FLASK_ENV=production
ENV JWT_SECRET_KEY=your-production-secret-key
ENV DATABASE_URL=sqlite:///instance/app.db

# 데이터베이스 초기화 및 서버 실행
CMD ["sh", "-c", "flask db upgrade && python run_server.py"]
