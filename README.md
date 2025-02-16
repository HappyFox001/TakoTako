# TakoTako

TakoTako 是一个能生成犀利评论的 AI 系统，支持命令行和 API 两种使用方式。

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/HappyFox001/TakoTako.git
cd TakoTako
```

2. 创建虚拟环境并安装依赖：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
```
然后编辑 `.env` 文件，将 `your_openai_api_key_here` 替换为你的 OpenAI API Key。

## 使用方法

### 命令行模式
```bash
python chatbot.py
```

### API 模式
```bash
python api.py
```
API 服务器将在 http://localhost:8000 启动，你可以：
- 访问 http://localhost:8000/docs 查看交互式 API 文档
- 使用 POST 请求访问 http://localhost:8000/comment 生成评论
