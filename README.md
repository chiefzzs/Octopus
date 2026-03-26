# 八爪鱼（Octopus）- AI智能体执行框架

## 项目简介

八爪鱼（Octopus）是一个开源的AI智能体执行框架，致力于实现从"思考"到"行动"的跨越，为大模型装上"手脚"，实现端到端的任务自动化执行。

## 当前版本

**v0.4.0 RC** - Release Candidate版本

### 已实现功能

- ✅ 微服务架构（接入、控制、执行、能力、实时输出）
- ✅ Web界面（Vue 3 + Element Plus）
  - 智能对话界面
  - 服务状态监控
  - 技能管理界面
  - 历史记录查看
- ✅ ReAct循环引擎
- ✅ 意图理解和任务拆解
- ✅ 工具选择和调用
- ✅ 上下文管理
- ✅ 技能管理系统
- ✅ 工具执行引擎
- ✅ 沙箱环境
- ✅ 资源管理
- ✅ 10种内置技能
- ✅ WebSocket实时通信
- ✅ 命令行接入
- ✅ 大模型集成（支持OpenAI兼容API）

### 即将推出

- 🔄 多渠道接入（飞书、钉钉、微信）
- 🔄 多模型支持
- 🔄 行业适配系统
- 🔄 插件机制

## 快速开始

### 环境要求

- Python 3.9+
- pip

### 安装步骤

1. 克隆项目
```bash
git clone git@github.com:chiefzzs/Octopus.git
cd Octopus
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 启动服务

**方式一：启动Web界面（推荐）**
```bash
# Windows
start_web_ui.bat

# 或直接运行
python src/services/access/app.py
```

**方式二：启动所有微服务**
```bash
python src/main.py
```

### 访问Web界面

服务启动后，在浏览器中打开：**http://localhost:8000**

### 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 接入服务 | 8000 | Web界面入口 |
| 控制服务 | 8001 | 请求路由控制 |
| 执行服务 | 8002 | ReAct执行引擎 |
| 能力服务 | 8003 | 技能管理执行 |
| 实时输出服务 | 8004 | 实时数据推送 |

## 项目结构

```
Octopus/
├── doc/                           # 文档目录
│   └── 01/
│       └── charter/
│           ├── 信息收集/           # 信息收集文档
│           ├── 产品规划.md         # 产品规划文档
│           └── 架构设计.md         # 架构设计文档
├── src/                           # 源代码目录
│   ├── main.py                   # 主程序入口
│   ├── config.py                 # 配置文件
│   ├── common/                   # 公共模块
│   │   └── utils/
│   │       └── logger.py         # 日志工具
│   └── services/                 # 微服务目录
│       ├── access/               # 接入服务
│       │   ├── app.py            # 服务入口
│       │   ├── gateway/          # 网关模块
│       │   ├── streaming/        # 流式处理
│       │   ├── format/           # 消息格式化
│       │   └── web/              # Web界面
│       ├── control/              # 控制服务
│       │   ├── app.py            # 服务入口
│       │   ├── auth/             # 认证模块
│       │   ├── router/           # 路由模块
│       │   ├── session/          # 会话管理
│       │   └── realtime/         # 实时输出
│       ├── execution/            # 执行服务
│       │   ├── app.py            # 服务入口
│       │   ├── react/            # ReAct引擎
│       │   ├── intent/           # 意图分析
│       │   ├── planning/         # 任务规划
│       │   ├── context/          # 上下文管理
│       │   └── tools/            # 工具选择
│       ├── capability/           # 能力服务
│       │   ├── app.py            # 服务入口
│       │   ├── skill/            # 技能管理
│       │   ├── executor/         # 工具执行
│       │   ├── sandbox/          # 沙箱环境
│       │   ├── result/           # 结果收集
│       │   └── resource/         # 资源管理
│       └── realtime/             # 实时输出服务
│           ├── app.py            # 服务入口
│           ├── websocket/        # WebSocket管理
│           ├── streaming/        # 流式输出
│           └── broker/           # 消息代理
├── tests/                        # 测试目录
│   ├── test_access_service.py
│   ├── test_control_service.py
│   ├── test_execution_service.py
│   ├── test_capability_service.py
│   └── test_realtime_service.py
├── logs/                         # 日志目录
├── requirements.txt              # Python依赖
├── start.bat                     # Windows启动脚本
├── start_services.bat            # 服务启动脚本
├── start_web_ui.bat              # Web界面启动脚本
├── USER_MANUAL.md                # 用户手册
├── QUICK_START.md                # 快速开始指南
└── README.md                     # 本文件
```

## 配置说明

### 环境变量配置

在运行项目前，请确保设置以下环境变量：

#### 必填配置

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| API_KEY | 大模型API密钥 | sk-xxxxxxxxxxxxxxxx |
| JWT_SECRET_KEY | JWT认证密钥（生产环境必须修改） | your_secure_random_key |

#### 可选配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| MODEL_NAME | 模型名称 | Qwen/Qwen3-8B |
| API_URL | API地址 | https://api.siliconflow.cn/v1 |
| DEBUG | 调试模式 | False |

### 配置方式

**Windows (PowerShell):**
```powershell
# 必填配置
$env:API_KEY="your_api_key_here"
$env:JWT_SECRET_KEY="your_secure_random_key_here"

# 可选配置
$env:MODEL_NAME="Qwen/Qwen3-8B"
$env:API_URL="https://api.siliconflow.cn/v1"
```

**Windows (命令提示符):**
```cmd
set API_KEY=your_api_key_here
set JWT_SECRET_KEY=your_secure_random_key_here
```

**Linux/macOS:**
```bash
# 必填配置
export API_KEY="your_api_key_here"
export JWT_SECRET_KEY="your_secure_random_key_here"

# 可选配置
export MODEL_NAME="Qwen/Qwen3-8B"
export API_URL="https://api.siliconflow.cn/v1"
```

**或创建 `.env` 文件（推荐）：**
```bash
# .env 文件内容
API_KEY=your_api_key_here
JWT_SECRET_KEY=your_secure_random_key_here
MODEL_NAME=Qwen/Qwen3-8B
API_URL=https://api.siliconflow.cn/v1
```

> ⚠️ **安全提示**: 
> - 请勿将 `.env` 文件提交到版本控制系统
> - 生产环境请务必修改 `JWT_SECRET_KEY` 为安全的随机字符串
> - API密钥请妥善保管，不要泄露

## 技术栈

- **语言**：Python 3.9+
- **Web框架**：FastAPI
- **异步框架**：asyncio
- **HTTP客户端**：aiohttp
- **前端框架**：Vue 3 + Element Plus
- **实时通信**：WebSocket
- **模型**：支持OpenAI兼容API的模型

## 参考文档

- [用户手册](USER_MANUAL.md)
- [快速开始指南](QUICK_START.md)
- [产品规划](doc/01/charter/产品规划.md)
- [架构设计](doc/01/charter/架构设计.md)

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

## 许可证

本项目采用开源许可证，具体许可证类型待定。

## 联系方式

- 项目团队：八爪鱼产品团队
- GitHub：https://github.com/chiefzzs/Octopus
- 创建日期：2026-03-26

---

**注意**：当前版本为RC（Release Candidate），功能正在持续完善中。欢迎体验和反馈！
