from modelscope.hub.snapshot_download import snapshot_download

# 直接下载到 D:\ollama 下面
llm_model_dir = snapshot_download(
    'Qwen/Qwen2.5-0.5B-Instruct',
    cache_dir=r'D:\ollama'
)

print("模型下载完成，路径：", llm_model_dir)