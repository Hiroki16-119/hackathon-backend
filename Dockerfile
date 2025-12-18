FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# タイムアウトを1000秒に延長、リトライ回数を5回に設定
RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]
