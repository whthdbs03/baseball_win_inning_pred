FROM python:3.11-slim

# 크롬 및 드라이버 설치
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    curl \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정 (Selenium이 찾을 수 있도록)
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 작업 디렉토리
WORKDIR /app

# 소스 복사
COPY . .

# 종속성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 실행 커맨드
CMD ["python", "app.py"]
