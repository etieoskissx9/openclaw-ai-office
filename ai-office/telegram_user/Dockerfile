FROM python:3.11

WORKDIR /app

COPY telegram_ai.py .
COPY session.session .
RUN pip install telethon python-dotenv openai

CMD ["python", "telegram_ai.py"]
