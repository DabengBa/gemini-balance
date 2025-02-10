# 🚀 FastAPI OpenAI (Gemini) 代理服务

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📝 项目简介

本项目是一个基于 FastAPI 框架开发的高性能、易于部署的 OpenAI 和 Gemini API 代理服务。它不仅兼容 OpenAI 的 API 接口，还支持 Google 的 Gemini 模型，为用户提供灵活的模型选择。该代理服务内置了多 API Key 轮询、负载均衡、自动重试、访问控制（Bearer Token 认证）、流式响应等功能，旨在简化 AI 应用的开发和部署流程。

**核心功能与优势:**

- **多模型支持**: 无缝切换 OpenAI 和 Gemini 模型。
- **智能 API Key 管理**: 自动轮询多个 API Key，实现负载均衡和故障转移。
- **安全访问控制**: 使用 Bearer Token 进行身份验证，保护 API 访问。
- **流式响应支持**: 提供实时的流式数据传输，提升用户体验。
- **内置工具支持**: 支持代码执行和 Google 搜索等工具, 丰富模型功能 (可选)。
- **灵活配置**: 通过环境变量或 `.env` 文件轻松配置。
- **易于部署**: 提供 Docker 一键部署，也支持手动部署。
- **健康检查**: 提供健康检查接口，方便监控服务状态。
- **图片生成支持**: 支持使用OpenAI的DALL-E模型生成图片

## 🛠️ 技术栈

- **FastAPI**: 高性能 Web 框架。
- **Python 3.9+**: 编程语言。
- **Pydantic**: 数据验证和设置管理。
- **httpx**: 异步 HTTP 客户端。
- **uvicorn**: ASGI 服务器。
- **Docker**: 容器化部署 (可选)。

## 🚀 快速开始

### 环境要求

- Python 3.9 或更高版本
- Docker (可选，推荐用于生产环境)

### 📦 安装与配置

1. **克隆项目**:

    ```bash
    git clone https://github.com/snailyp/gemini-balance.git
    cd gemini-balance
    ```

2. **安装依赖**:

    ```bash
    pip install -r requirements.txt
    ```

3. **配置**:

    创建 `.env` 文件，并按以下分类配置环境变量：

    ```env
    # 基础配置
    BASE_URL="https://generativelanguage.googleapis.com/v1beta"  # Gemini API 基础 URL，默认无需修改
    MAX_FAILURES=3  # 允许单个key失败的次数，默认3次

    # 认证与安全配置
    API_KEYS=["your-gemini-api-key-1", "your-gemini-api-key-2"]  # Gemini API 密钥列表，用于负载均衡
    ALLOWED_TOKENS=["your-access-token-1", "your-access-token-2"]  # 允许访问的 Token 列表
    AUTH_TOKEN=""  # 超级管理员token，具有所有权限，默认使用 ALLOWED_TOKENS 的第一个

    # 模型功能配置
    MODEL_SEARCH=["gemini-2.0-flash-exp"]  # 支持搜索功能的模型列表
    TOOLS_CODE_EXECUTION_ENABLED=false  # 是否启用代码执行工具，默认false
    SHOW_SEARCH_LINK=true  # 是否在响应中显示搜索结果链接，默认true
    SHOW_THINKING_PROCESS=true  # 是否显示模型思考过程，默认true

    # 图片生成配置
    PAID_KEY="your-paid-api-key"  # 付费版API Key，用于图片生成等高级功能
    CREATE_IMAGE_MODEL="imagen-3.0-generate-002"  # 图片生成模型，默认使用imagen-3.0
    
    # 图片上传配置
    UPLOAD_PROVIDER="smms"  # 图片上传提供商，目前支持smms
    SMMS_SECRET_TOKEN="your-smms-token"  # SM.MS图床的API Token
    ```

   ### 配置说明

   #### 基础配置

    - `BASE_URL`: Gemini API 的基础 URL
      - 默认值: `https://generativelanguage.googleapis.com/v1beta`
      - 说明: 通常无需修改，除非 API 地址发生变化
    - `MAX_FAILURES`: API Key 允许的最大失败次数
      - 默认值: `3`
      - 说明: 超过此次数后，Key 将被暂时标记为无效

   #### 认证与安全配置

    - `API_KEYS`: Gemini API 密钥列表
      - 格式: JSON 数组字符串
      - 用途: 支持多个 Key 轮询，实现负载均衡
      - 建议: 至少配置 2 个 Key 以保证服务可用性
    - `ALLOWED_TOKENS`: 访问令牌列表
      - 格式: JSON 数组字符串
      - 用途: 用于客户端认证
      - 安全提示: 请使用足够复杂的令牌
    - `AUTH_TOKEN`: 超级管理员令牌
      - 可选配置，留空则使用 ALLOWED_TOKENS 的第一个
      - 具有查看 API Key 状态等特权操作权限

   #### 模型功能配置

    - `MODEL_SEARCH`: 搜索功能支持的模型
      - 默认值: `["gemini-2.0-flash-exp"]`
      - 说明: 仅列表中的模型可使用搜索功能
    - `TOOLS_CODE_EXECUTION_ENABLED`: 代码执行功能
      - 默认值: `false`
      - 安全提示: 生产环境建议禁用
    - `SHOW_SEARCH_LINK`: 搜索结果链接显示
      - 默认值: `true`
      - 用途: 控制搜索结果中是否包含原始链接
    - `SHOW_THINKING_PROCESS`: 思考过程显示
      - 默认值: `true`
      - 用途: 显示模型的推理过程，便于调试

   #### 图片生成配置

    - `PAID_KEY`: 付费版 API Key
      - 用途: 用于图片生成等高级功能
      - 说明: 需要单独申请的付费版 Key
    - `CREATE_IMAGE_MODEL`: 图片生成模型
      - 默认值: `imagen-3.0-generate-002`
      - 说明: 当前支持的最新图片生成模型

   #### 图片上传配置

    - `UPLOAD_PROVIDER`: 图片上传服务提供商
      - 默认值: `smms`
      - 说明: 目前支持 SM.MS 图床
    - `SMMS_SECRET_TOKEN`: SM.MS API Token
      - 用途: 用于图片上传到 SM.MS 图床
      - 获取方式: 需要在 SM.MS 官网注册并获取

### ▶️ 运行

#### 使用 Docker (推荐)

1. **构建镜像**:

    ```bash
    docker build -t gemini-balance .
    ```

2. **运行容器**:

    ```bash
    docker run -d -p 8000:8000 --env-file .env gemini-balance
    ```

    - `-d`: 后台运行。
    - `-p 8000:8000`: 将容器的 8000 端口映射到主机的 8000 端口。
    - `--env-file .env`: 使用 `.env` 文件设置环境变量。

#### 手动运行

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- `--reload`: 开启热重载，方便开发调试 (生产环境不建议开启)。

## 🔌 API 接口

### 认证

所有 API 请求都需要在 Header 中添加 `Authorization` 字段，值为 `Bearer <your-token>`，其中 `<your-token>` 需要替换为你在 `.env` 文件中配置的 `ALLOWED_TOKENS` 中的一个或者 `AUTH_TOKEN`。

### 获取模型列表

- **URL**: `/v1/models`
- **Method**: `GET`
- **Header**: `Authorization: Bearer <your-token>`

### 聊天补全 (Chat Completions)

- **URL**: `/v1/chat/completions`
- **Method**: `POST`
- **Header**: `Authorization: Bearer <your-token>`
- **Body** (JSON):

    ```json
    {
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ],
        "model": "gemini-1.5-flash-002",
        "temperature": 0.7,
        "stream": false,
        "tools": [],
        "max_tokens": 8192,
        "stop": [],
        "top_p": 0.9,
        "top_k": 40
    }
    ```

  - `messages`: 消息列表，格式与 OpenAI API 相同。
  - `model`: 模型名称，例如 `gemini-1.5-flash-002`。
  - `stream`: 是否开启流式响应，`true` 或 `false`。
  - `tools`: 使用的工具列表。
  - 其他参数：与 OpenAI API 兼容的参数，如 `temperature`, `max_tokens` 等。

### 获取词向量 (Embeddings)

- **URL**: `/v1/embeddings`
- **Method**: `POST`
- **Header**: `Authorization: Bearer <your-token>`
- **Body** (JSON):

    ```json
    {
        "input": "你的文本",
        "model": "text-embedding-004"
    }
    ```

  - `input`: 输入文本。
  - `model`: 模型名称。

### 健康检查

- **URL**: `/health`
- **Method**: `GET`

### 获取 API Key 列表

- **URL**: `/v1/keys/list`
- **Method**: `GET`
- **Header**: `Authorization: Bearer <your-auth-token>`
- **说明**: 只有使用 `AUTH_TOKEN` 才能访问此接口, 用于获取有效和无效的 API Key 列表。

### 图片生成 (Image Generation)

- **URL**: `/v1/images/generations`
- **Method**: `POST`
- **Header**: `Authorization: Bearer <your-auth-token>`
- **说明**: Body示例和参数说明

    ```json
    {
    "model": "dall-e-3",
    "prompt": "汉服美女",
    "n": 1,
    "size": "1024x1024"
    }
    ```

## 📚 代码结构

```plaintext
.
├── app/
│   ├── api/                # API 路由
│   │   ├── gemini_routes.py   # Gemini 模型路由
│   │   └── openai_routes.py   # OpenAI 兼容路由
│   ├── core/               # 核心组件
│   │   ├── config.py         # 配置管理
│   │   ├── logger.py         # 日志配置
│   │   └── security.py       # 安全认证
│   ├── middleware/         # 中间件
│   │   └── request_logging_middleware.py  # 请求日志中间件
│   ├── schemas/            # 数据模型
│   │   ├── gemini_models.py  # Gemini 原始请求/响应模型
│   │   └── openai_models.py  # OpenAI 兼容请求/响应模型
│   ├── services/           # 服务层
│   │   ├── chat/           # 聊天相关服务
│   │   │   ├── api_client.py # API 客户端
│   │   │   ├── message_converter.py # 消息转换器
│   │   │   ├── response_handler.py # 响应处理器
│   │   │   └── retry_handler.py #重试处理器
│   │   ├── gemini_chat_service.py   # Gemini 原始聊天服务
│   │   ├── openai_chat_service.py   # OpenAI 兼容聊天服务
│   │   ├── embedding_service.py # 向量服务
│   │   ├── key_manager.py    # API Key 管理
│   │   └── model_service.py  # 模型服务
│   └── main.py              # 主程序入口
├── Dockerfile              # Dockerfile
├── requirements.txt       # 项目依赖
└── README.md               # 项目说明
```

## 🔒 安全性

- **API Key 轮询**: 自动轮换 API Key，提高可用性和负载均衡。
- **Bearer Token 认证**: 保护 API 端点，防止未经授权的访问。
- **请求日志记录**: 记录详细的请求信息，便于调试和审计 (可选，通过取消 `app.add_middleware(RequestLoggingMiddleware)` 的注释来启用)。
- **自动重试**: 在 API 请求失败时自动重试，提高服务的稳定性。

## 🤝 贡献

欢迎任何形式的贡献！如果你发现 bug、有新功能建议或者想改进代码，请随时提交 Issue 或 Pull Request。

1. Fork 本项目。
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到你的分支 (`git push origin feature/AmazingFeature`)。
5. 创建一个新的 Pull Request。

## ❓ 常见问题解答 (FAQ)

**Q: 如何获取 Gemini API Key？**

A: 请参考 Gemini API 的官方文档，申请 API Key。

**Q: 如何配置多个 API Key？**

A: 在 `.env` 文件的 `API_KEYS` 变量中，用列表的形式添加多个 Key，例如：`API_KEYS=["key1", "key2", "key3"]`。

**Q: 为什么我的 API Key 总是失败？**

A: 请检查以下几点：

- API Key 是否正确。
- API Key 是否已过期或被禁用。
- 是否超出了 API Key 的速率限制或配额。
- 网络连接是否正常。

**Q: 如何启用流式响应？**

A: 在请求的 Body 中，将 `stream` 参数设置为 `true` 即可。

**Q: 如何启用代码执行工具？**
A: 在 `.env` 文件的 `TOOLS_CODE_EXECUTION_ENABLED` 变量中, 设置为 `true` 即可。

## 📄 许可证

本项目采用 MIT 许可证。有关详细信息，请参阅 [LICENSE](LICENSE) 文件 (你需要创建一个 LICENSE 文件)。
