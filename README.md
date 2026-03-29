# 🤖 Ollama 本地 AI 应用集合

一个完整的本地 AI 模型应用套件，使用 [Ollama](https://ollama.ai) 和 [Qwen](https://qwenlm.github.io/) 模型，支持多种前后端框架。

## ✨ 功能特性

- **多种 UI 框架**：支持 Gradio、Streamlit 等前端
- **FastAPI 后端**：提供可扩展的 REST API 接口
- **流式聊天**：实时流式输出，提升用户体验
- **成语接龙游戏**：基于 LangChain 的交互式游戏
- **本地运行**：完全离线，隐私优先
- **参数可调**：支持温度、Top-P 等参数调整

## 📂 项目结构

```
ollama/
├── api.py                    # FastAPI 后端服务
├── gradio_app.py             # Gradio Web UI
├── web.py                    # Streamlit Web UI
├── 成语接龙.py                # 成语接龙游戏
├── 模型下载.py                # 模型下载脚本
├── OpenAI访问ollama.py       # OpenAI API 适配层演示
├── modles/                   # 模型存储目录
│   └── Qwen/                # Qwen2.5 模型
└── 图片/                     # 应用截图目录
```

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Ollama 已安装并运行
- 已下载 Qwen2.5 模型

### 安装依赖

```bash
pip install fastapi uvicorn openai langchain langchain-openai gradio streamlit requests
```

### 启动 Ollama

```bash
ollama serve
# 或在另一个终端运行
ollama pull qwen2.5:0.5b
```

### 启动后端 API

```bash
python api.py
# API 将在 http://localhost:6066 上运行
```

### 选择一个前端

#### 方式1：使用 Gradio 界面

```bash
python gradio_app.py
# 访问 http://localhost:7860
```

#### 方式2：使用 Streamlit 界面

```bash
streamlit run web.py
# 访问 http://localhost:8501
```

#### 方式3：成语接龙游戏

```bash
python 成语接龙.py
```

## 📝 功能说明

### 1. **api.py** - FastAPI 后端

提供聊天 API 接口，支持流式响应。

**端点**: `POST /chat`

**请求参数**:
- `query` (str): 用户输入
- `sys_prompt` (str): 系统提示词
- `history` (list): 聊天历史
- `history_len` (int): 保留历史轮数
- `temperature` (float): 生成多样性 (0.01-2.0)
- `top_p` (float): 核采样参数 (0.01-1.0)
- `max_tokens` (int): 最大生成长度

**使用示例**:
```bash
curl -X POST "http://localhost:6066/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "你好",
    "sys_prompt": "你是一个有用的助手",
    "history": [],
    "history_len": 1,
    "temperature": 0.7,
    "top_p": 0.8,
    "max_tokens": 1024
  }'
```

### 2. **gradio_app.py** - Gradio 前端

基于 Gradio 的 Web UI，提供美观的聊天界面。

**特性**:
- 可调节的系统提示词
- 历史轮数切片
- 实时参数调整
- 流式输出

![Gradio 应用截图](图片/屏幕截图%202026-03-29%20093140.png)
![Gradio 界面2](图片/屏幕截图%202026-03-29%20101131.png)

### 3. **web.py** - Streamlit 前端

基于 Streamlit 的轻量级聊天应用。

**特性**:
- 实时聊天界面
- 侧栏参数配置
- 清空历史记录功能
- 会话管理

![Streamlit 应用截图](图片/屏幕截图%202026-03-29%20101531.png)
![Streamlit 界面2](图片/屏幕截图%202026-03-29%20102903.png)

### 4. **成语接龙.py** - 交互式游戏

使用 LangChain 实现的成语接龙游戏。

**玩法**:
```
输入第一个成语，AI 会用该成语的最后一个字接下一个成语
例如：输入"龙虎相争" -> AI 可能回复"争分夺秒"
```

## ⚙️ 参数详解

本项目的所有可调节参数及其作用：

### 模型与连接参数

| 参数名 | 类型 | 默认值 | 取值范围 | 说明 |
|------|------|--------|---------|------|
| `model` | str | `qwen2.5:0.5b` | 任何已下载的Ollama模型 | 指定要使用的LLM模型 |
| `base_url` | str | `http://localhost:11434/v1` | 任何有效的URL | Ollama 服务器地址 |
| `api_key` | str | `ollama` | 任何字符串 | OpenAI兼容API的密钥 |

### 聊天生成参数

| 参数名 | 类型 | 默认值 | 取值范围 | 说明 |
|------|------|--------|---------|------|
| `temperature` | float | `0.7` | 0.01 - 2.0 | **生成多样性**。值越大输出越随机创意，值越小越稳定一致。推荐0.5-1.0 |
| `top_p` | float | `0.8` | 0.01 - 1.0 | **核采样参数**。控制词汇多样性，值越小越集中在高概率词汇 |
| `max_tokens` | int | `1024` | 1 - 32000 | **最大生成长度**。单位为token，越大响应越长但速度越慢 |

### 对话管理参数

| 参数名 | 类型 | 默认值 | 取值范围 | 说明 |
|------|------|--------|---------|------|
| `query` | str | 无 | 任何文本 | **用户输入**的问题或指令 |
| `sys_prompt` | str | `你是一个有用的助手` | 任何文本 | **系统提示词**，定义AI的角色和行为 |
| `history` | list | `[]` | 消息对象列表 | **对话历史**，包含之前的user和assistant消息 |
| `history_len` | int | `1` | 1 - 10 | **保留历史轮数**。1表示只看最近1轮对话 |

### 服务端口参数

| 参数名 | 服务 | 默认值 | 说明 |
|------|------|--------|------|
| `port` | FastAPI | `6066` | API服务监听端口 |
| `port` | Gradio | `7860` | Gradio Web界面端口 |
| `port` | Streamlit | `8501` | Streamlit Web界面端口 |

### 参数调整建议

**速度优化**（提升响应速度）：
```python
max_tokens=512          # 减少生成长度
temperature=0.5        # 降低多样性
history_len=1          # 减少历史上下文
```

**质量优化**（提升回复质量）：
```python
max_tokens=2048        # 增加生成长度
temperature=0.8        # 适度提高创意度
top_p=0.9             # 保留更多词汇选择
history_len=5         # 增加历史上下文
```

**创意优化**（获得多样化回复）：
```python
temperature=1.5       # 提高随机性
top_p=0.95           # 增加词汇多样性
max_tokens=1024       # 给予充分空间
```

**稳定优化**（获得一致性回复）：
```python
temperature=0.3       # 降低随机性
top_p=0.6            # 集中在高概率词汇
```

## 🔧 配置说明

### 模型配置

所有应用默认使用 `qwen2.5:0.5b` 模型。可在代码中修改：

```python
model="qwen2.5:0.5b"  # 改为其他可用模型
```

### Ollama 连接

默认连接地址：`http://localhost:11434/v1`

如需修改，在各文件中修改 `base_url` 参数。

### API 端口

- FastAPI: `6066`
- Gradio: `7860`
- Streamlit: `8501`

## 📊 性能优化建议

1. **选择合适的模型**：
   - 轻量级：`qwen2.5:0.5b`（推荐，快速响应）
   - 标准：`qwen2.5:1.5b`
   - 高性能：`qwen2.5:7b`

2. **调整参数**：
   - 降低 `max_tokens` 以加快响应
   - 增加 `temperature` 得到更多样的回复

3. **硬件要求**：
   - 推荐 GPU（CUDA/ROCm）
   - 最小内存：4GB（0.5B 模型）

## 🔌 与 OpenAI 兼容

本项目使用 OpenAI Python 客户端连接到本地 Ollama 服务，实现 OpenAI API 兼容模式。

参考文件：`OpenAI访问ollama.py`

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)
```

## 📦 依赖说明

| 包名 | 用途 |
|-----|------|
| fastapi | REST API 框架 |
| uvicorn | ASGI 服务器 |
| openai | OpenAI 客户端（兼容 Ollama） |
| gradio | Web UI 框架 |
| streamlit | 轻量级 Web 框架 |
| langchain | AI 应用框架 |
| langchain-openai | LangChain OpenAI 集成 |

## 🐛 常见问题

**Q: 如何连接到远程 Ollama 服务器？**
A: 修改 `base_url`，例如：`http://192.168.1.100:11434/v1`

**Q: 为什么响应很慢？**
A: 检查是否使用 GPU 加速，修改 `max_tokens` 减少生成长度

**Q: 如何切换模型？**
A: 修改代码中的 `model` 参数为其他已下载的模型名称

**Q: 如何调整生成质量？**
A: 调整 `temperature`（创意度）和 `top_p`（多样性）参数

## 📝 开发建议

- 建议在虚拟环境中运行
- 使用 `pip freeze > requirements.txt` 保存依赖
- 参考官方文档：[Ollama Docs](https://github.com/ollama/ollama)、[LangChain Docs](https://python.langchain.com/)

## 📄 许可证

根据您的项目选择合适的开源许可证

## 🙏 致谢

感谢以下项目的支持：
- [Ollama](https://ollama.ai)
- [Qwen LLM](https://qwenlm.github.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Gradio](https://www.gradio.app/)
