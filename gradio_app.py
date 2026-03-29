import gradio as gr
import requests

# 后端FastAPI地址
backend_url = "http://127.0.0.1:6066/chat"


# 与后端交互
def chat_with_backend(prompt, history, sys_prompt, history_len, temperature, top_p, max_tokens, stream):
    if not history:
        history = []

    history_clean = []
    for h in history:
        history_clean.append({
            "role": h.get("role"),
            "content": h.get("content")
        })

    data = {
        "query": prompt,
        "sys_prompt": sys_prompt,
        "history": history_clean,
        "history_len": history_len,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }

    response = requests.post(backend_url, json=data, stream=True)

    if response.status_code != 200:
        yield f"请求失败：{response.status_code}"
        return

    chunks = ""
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        chunks += chunk
        yield chunks


# 界面
with gr.Blocks(fill_width=True, fill_height=True) as demo:
    gr.Markdown("# 🤖 本地聊天机器人（Gradio + FastAPI + Ollama）")

    with gr.Row():
        with gr.Column(scale=1, variant="panel"):
            sys_prompt = gr.Textbox(label="系统提示词", value="你是一个有用的助手")
            history_len = gr.Slider(minimum=1, maximum=10, value=1, label="历史轮数")
            temperature = gr.Slider(minimum=0.01, maximum=2.0, value=0.7, step=0.01, label="temperature")
            top_p = gr.Slider(minimum=0.01, maximum=1.0, value=0.8, step=0.01, label="top_p")
            max_tokens = gr.Slider(minimum=256, maximum=4096, value=1024, label="max_tokens")
            stream = gr.Checkbox(label="流式输出", value=True)

        with gr.Column(scale=10):
            chatbot = gr.Chatbot(type="messages", height=550)

    gr.ChatInterface(
        fn=chat_with_backend,
        type="messages",
        chatbot=chatbot,
        additional_inputs=[sys_prompt, history_len, temperature, top_p, max_tokens, stream]
    )

if __name__ == "__main__":
    demo.launch(server_port=7860)