FROM python:3.11-slim

# 필요한 패키지 설치 (크롬 + 드라이버 포함)
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 \
    libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 \
    libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 xdg-utils \
    chromium-driver chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 환경변수 설정
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="${PATH}:/usr/lib/chromium/"

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사
COPY . .

# 의존성 설치
RUN pip install --upgrade pip && pip install -r requirements.txt

# 실행
CMD ["python", "app.py"]
