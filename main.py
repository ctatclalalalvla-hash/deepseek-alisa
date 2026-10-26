import os
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

# Инициализируем клиент OpenAI для работы через Ofox
# Ofox использует этот протокол, поэтому мы указываем их базовый URL
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), # Сюда мы вставили ключ ofox в Render
    base_url="https://api.ofox.ai/v1"
)

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    # Отправляем запрос в DeepSeek через прокси Ofox
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat", # Модель DeepSeek через Ofox
            messages=[{"role": "user", "content": user_text}]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        # Если произойдет ошибка, Алиса скажет об этом, а мы увидим лог
        print(f"Error: {e}")
        answer = "Произошла ошибка при обращении к нейросети."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
