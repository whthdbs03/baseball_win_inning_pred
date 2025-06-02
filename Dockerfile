FROM python:3.11-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    chromium \
    chromium-driver \
    fonts-liberation \
    && apt-get clean

# 환경 변수 설정
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver
ENV PATH="${CHROMEDRIVER_PATH}:${PATH}"

# 작업 디렉토리
WORKDIR /app

# 소스 복사
COPY . .

# 종속성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 실행 커맨드
CMD ["python", "app.py"]
