FROM python:3.12-slim

WORKDIR /app

COPY . .

# 必要ライブラリを全部入れる
RUN pip install --no-cache-dir telethon openai python-dotenv

ENV PYTHONPATH=/app

# Telegramのゆなを起動
CMD ["python", "telegram/telegram_bot.py"]
