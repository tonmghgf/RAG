from fastapi import FastAPI, Body
from openai import AsyncOpenAI
from typing import List
from fastapi.responses import StreamingResponse

app = FastAPI(title="Ollama API")

aclient = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

@app.post("/chat")
async def chat(
    query: str = Body(...),
    sys_prompt: str = Body("你是一个有用的助手"),
    history: List = Body([]),
    history_len: int = Body(1),
    temperature: float = Body(0.7),
    top_p: float = Body(0.8),
    max_tokens: int = Body(1024)
):
    messages = [{"role": "system", "content": sys_prompt}]
    if history_len > 0:
        messages.extend(history[-2 * history_len:])
    messages.append({"role": "user", "content": query})

    response = await aclient.chat.completions.create(
        model="qwen2.5:0.5b",
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stream=True
    )

    async def generate():
        async for chunk in response:
            c = chunk.choices[0].delta.content
            if c:
                yield c
    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6066)