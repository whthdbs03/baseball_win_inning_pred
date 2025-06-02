FROM python:3.11-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    wget unzip curl gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 크롬 환경변수 설정 (Selenium이 찾을 수 있도록)
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/lib/chromium/

# 작업 디렉토리 설정
WORKDIR /app

# 코드 복사
COPY . .

# 의존성 설치
RUN pip install --upgrade pip && pip install -r requirements.txt

# 실행 커맨드
CMD ["python", "app.py"]
