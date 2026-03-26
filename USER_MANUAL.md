# 八爪鱼（Octopus）用户使用手册

## 目录

1. [项目介绍](#项目介绍)
2. [系统要求](#系统要求)
3. [安装指南](#安装指南)
4. [快速开始](#快速开始)
5. [Web界面使用](#web界面使用)
6. [功能说明](#功能说明)
7. [API文档](#api文档)
8. [配置说明](#配置说明)
9. [测试指南](#测试指南)
10. [故障排除](#故障排除)

---

## 项目介绍

八爪鱼（Octopus）是一个开源的AI智能体执行框架，致力于实现从"思考"到"行动"的跨越，为大模型装上"手脚"，实现端到端的任务自动化执行。

### 核心特性

- **执行能力**：真正能做事的AI，自主操控电脑，自动打开软件、处理文件、生成成果
- **多模型支持**：集成多种主流大模型，支持本地Ollama模型
- **本地优先**：所有操作在本地运行，数据隐私可控
- **开源免费**：完全开源，社区驱动发展
- **实时输出**：支持大模型实时输出和中间阶段信息展示

### 当前版本

**v0.4.0 RC** - 已完成功能：
- ✅ 接入服务（Access Service）
- ✅ 控制服务（Control Service）
- ✅ 实时输出服务（Realtime Service）
- ✅ 执行服务（Execution Service）
- ✅ 能力服务（Capability Service）
- ✅ 用户认证和会话管理
- ✅ WebSocket实时通信
- ✅ 流式API输出
- ✅ ReAct循环引擎
- ✅ 意图理解和任务拆解
- ✅ 工具选择和调用
- ✅ 上下文管理
- ✅ 技能管理系统
- ✅ 工具执行引擎
- ✅ 沙箱环境
- ✅ 资源管理
- ✅ **Web界面交互（新增）**
  - 智能对话界面
  - 服务状态监控
  - 技能管理界面
  - 历史记录查看
  - WebSocket实时通信
  - 本地资源加载

---

## Web界面使用

### 概述

八爪鱼提供了现代化的Web界面，让您可以通过浏览器轻松与AI智能体进行交互。Web界面包含以下功能模块：

- **智能对话**：与八爪鱼AI进行实时聊天
- **服务状态**：监控各微服务的运行状态
- **技能管理**：查看和管理系统可用技能
- **历史记录**：查看历史会话记录

### 启动Web界面

#### 方法一：使用专门的启动脚本（推荐）

**Windows系统：**
```bash
start_web_ui.bat
```

#### 方法二：直接启动接入服务

```bash
# 设置Python路径
$env:PYTHONPATH="d:/learnning/2603_03;d:/learnning/2603_03/src"

# 启动接入服务
python src/services/access/app.py
```

### 访问Web界面

服务启动后，在浏览器中打开：
```
http://localhost:8000
```

### 功能说明

#### 1. 智能对话界面

- **消息发送**：在输入框中输入消息，按Enter键发送
- **实时响应**：通过WebSocket实时接收AI响应
- **消息历史**：显示完整的对话历史
- **输入状态**：显示AI正在输入的状态

#### 2. 服务状态监控

- **服务列表**：显示所有微服务的状态
- **健康检查**：自动检测服务健康状态
- **端口信息**：显示各服务的监听端口
- **状态指示器**：绿色表示运行中，红色表示离线

#### 3. 技能管理界面

- **技能卡片**：以卡片形式展示所有技能
- **技能分类**：按类别组织技能（内置/插件）
- **技能详情**：点击卡片查看技能详细信息
- **技能描述**：显示技能的功能说明

#### 4. 历史记录界面

- **会话列表**：显示历史会话记录
- **会话预览**：显示会话的简短预览
- **时间戳**：记录会话的创建时间
- **快速加载**：点击历史会话快速加载

### 技术特性

- **Vue 3**：现代化的前端框架
- **Element Plus**：美观的UI组件库
- **WebSocket**：实时双向通信
- **本地资源**：所有资源本地加载，无外部依赖
- **响应式设计**：支持多种屏幕尺寸

### 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 系统要求

### 操作系统
- Windows 10/11
- Linux (Ubuntu 18.04+)
- macOS 10.14+

### 软件依赖
- Python 3.8+
- pip (Python包管理器)

### 硬件要求
- CPU: 双核及以上
- 内存: 4GB及以上
- 磁盘: 1GB可用空间

---

## 安装指南

### 方法一：使用启动脚本（推荐）

#### Windows系统

1. 双击运行 `start.bat` 文件
2. 脚本会自动完成以下操作：
   - 检查Python安装
   - 创建虚拟环境
   - 安装依赖包
   - 启动程序

#### Linux/macOS系统

1. 打开终端，进入项目目录
2. 运行启动脚本：
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

### 方法二：手动安装

1. **创建虚拟环境**
   ```bash
   python -m venv venv
   ```

2. **激活虚拟环境**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Linux/macOS:
   ```bash
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```bash
   python src/main.py
   ```

---

## 快速开始

### 启动Web界面（推荐）

这是最简单的方式，启动后即可通过浏览器访问Web界面：

```bash
# Windows系统
start_web_ui.bat

# 或直接运行
python src/services/access/app.py
```

服务启动后，在浏览器中打开：**http://localhost:8000**

### 启动所有服务

```bash
python src/main.py
```

### 单独启动服务

**启动接入服务（端口8000）：**
```bash
python src/services/access/app.py
```

**启动控制服务（端口8001）：**
```bash
python src/services/control/app.py
```

**启动执行服务（端口8002）：**
```bash
python src/services/execution/app.py
```

**启动能力服务（端口8003）：**
```bash
python src/services/capability/app.py
```

**启动实时输出服务（端口8004）：**
```bash
python src/services/realtime/app.py
```

### 验证服务

访问以下URL验证服务是否正常运行：

- 接入服务健康检查: http://localhost:8000/health
- 控制服务健康检查: http://localhost:8001/health
- 执行服务健康检查: http://localhost:8002/health
- 能力服务健康检查: http://localhost:8003/health
- 实时输出服务健康检查: http://localhost:8004/health

---

## 功能说明

### 1. 接入服务（Access Service）

接入服务负责处理用户请求，支持HTTP和WebSocket两种通信方式。

#### HTTP接口

**发送消息**
```http
POST http://localhost:8000/api/access/message
Content-Type: application/json

{
  "message": "你好",
  "user_id": "user123"
}
```

**流式API**
```http
POST http://localhost:8000/api/access/stream
Content-Type: application/json

{
  "message": "请帮我写一段代码",
  "user_id": "user123"
}
```

#### WebSocket接口

**连接地址：**
```
ws://localhost:8000/ws
```

**发送消息示例：**
```json
{
  "type": "message",
  "content": "你好",
  "user_id": "user123"
}
```

### 2. 控制服务（Control Service）

控制服务负责用户认证、会话管理和消息路由。

#### 用户认证

**用户注册**
```http
POST http://localhost:8001/api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123",
  "email": "test@example.com"
}
```

**用户登录**
```http
POST http://localhost:8001/api/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**用户登出**
```http
POST http://localhost:8001/api/auth/logout?token=YOUR_TOKEN
```

#### 会话管理

**创建会话**
```http
POST http://localhost:8001/api/session/create
Content-Type: application/json

{
  "user_id": "user123"
}
```

**获取会话**
```http
GET http://localhost:8001/api/session/{session_id}
```

**更新会话**
```http
POST http://localhost:8001/api/session/update
Content-Type: application/json

{
  "session_id": "session123",
  "data": {
    "context": "new context"
  }
}
```

### 3. 实时输出服务（Realtime Service）

实时输出服务提供流式输出和WebSocket实时通信功能。

#### 流式API

**流式输出**
```http
GET http://localhost:8002/api/realtime/stream/{session_id}
```

**发送消息**
```http
POST http://localhost:8002/api/realtime/send
Content-Type: application/json

{
  "session_id": "session123",
  "message": "实时消息内容"
}
```

**广播消息**
```http
POST http://localhost:8002/api/realtime/broadcast
Content-Type: application/json

{
  "message": "广播消息内容"
}
```

#### WebSocket接口

**连接地址：**
```
ws://localhost:8002/ws/realtime
```

### 4. 执行服务（Execution Service）

执行服务是v0.3.0 Beta版本新增的核心服务，实现了ReAct循环引擎，负责任务的智能执行。

#### 任务执行

**执行任务**
```http
POST http://localhost:8003/api/execution/execute
Content-Type: application/json

{
  "task_id": "task_001",
  "user_input": "创建一个新文件",
  "session_id": "session_001"
}
```

**响应示例：**
```json
{
  "status": "success",
  "task_id": "task_001",
  "result": {
    "status": "success",
    "results": [...]
  },
  "intent": {
    "intent": "action",
    "confidence": 0.8
  },
  "tasks": [...]
}
```

#### 流式执行

**流式执行任务**
```http
POST http://localhost:8003/api/execution/stream
Content-Type: application/json

{
  "task_id": "task_002",
  "user_input": "分析数据",
  "session_id": "session_001"
}
```

**流式响应：**
```
data: {"type": "task_start", "task_id": "task_002"}
data: {"type": "thought", "iteration": 0, "content": "..."}
data: {"type": "action", "iteration": 0, "content": {...}}
data: {"type": "observation", "iteration": 0, "content": "..."}
data: {"type": "task_complete", "task_id": "task_002"}
```

#### WebSocket实时执行

**连接地址：**
```
ws://localhost:8003/ws/execution
```

**发送执行请求：**
```json
{
  "type": "execute",
  "data": {
    "task_id": "task_003",
    "user_input": "搜索文件",
    "session_id": "session_001"
  }
}
```

**接收实时更新：**
```json
{
  "type": "update",
  "data": {
    "phase": "thought",
    "content": "正在思考..."
  }
}
```

#### ReAct循环引擎

执行服务实现了完整的ReAct（Reasoning + Acting）循环：

1. **Thought（思考）**：分析任务，决定下一步行动
2. **Action（行动）**：选择并执行工具
3. **Observation（观察）**：观察执行结果
4. **循环**：根据观察结果继续思考，直到任务完成

#### 意图理解

执行服务能够自动识别用户意图：

- **查询（query）**：搜索、查询信息
- **操作（action）**：创建、生成、构建
- **分析（analysis）**：分析、评估、比较
- **修改（modification）**：修改、更新、编辑
- **删除（deletion）**：删除、移除
- **搜索（search）**：查找、定位

#### 任务拆解

根据意图自动拆解复杂任务：

- **查询任务**：搜索 → 分析 → 总结
- **操作任务**：验证 → 准备 → 执行 → 验证
- **分析任务**：收集 → 处理 → 报告
- **修改任务**：定位 → 备份 → 修改 → 验证

#### 工具系统

执行服务提供8种基础工具：

1. **file_reader**：读取文件内容
2. **file_writer**：写入文件内容
3. **file_searcher**：搜索文件
4. **code_executor**：执行Python代码
5. **web_searcher**：Web搜索
6. **data_analyzer**：数据分析
7. **text_processor**：文本处理
8. **api_caller**：API调用

### 5. 能力服务（Capability Service）

能力服务是v0.4.0 RC版本新增的核心服务，提供技能管理、工具执行和沙箱环境。

#### 技能管理

**注册技能**
```http
POST http://localhost:8004/api/capability/skill/register
Content-Type: application/json

{
  "name": "custom_skill",
  "description": "Custom skill description",
  "category": "custom",
  "tags": ["custom", "demo"],
  "parameters": {
    "input": {"type": "string", "required": true}
  }
}
```

**列出所有技能**
```http
GET http://localhost:8004/api/capability/skill/list
```

**获取技能信息**
```http
GET http://localhost:8004/api/capability/skill/{skill_id}
```

**注销技能**
```http
DELETE http://localhost:8004/api/capability/skill/{skill_id}
```

#### 工具执行

**执行单个工具**
```http
POST http://localhost:8004/api/capability/execute
Content-Type: application/json

{
  "tool_name": "file_write",
  "parameters": {
    "file_path": "test.txt",
    "content": "Hello, World!"
  },
  "session_id": "session_001",
  "use_sandbox": true
}
```

**批量执行工具**
```http
POST http://localhost:8004/api/capability/execute/batch
Content-Type: application/json

{
  "tools": [
    {
      "tool_name": "file_write",
      "parameters": {"file_path": "file1.txt", "content": "Content 1"}
    },
    {
      "tool_name": "file_write",
      "parameters": {"file_path": "file2.txt", "content": "Content 2"}
    }
  ],
  "session_id": "session_001"
}
```

#### 沙箱环境

**创建沙箱**
```http
POST http://localhost:8004/api/capability/sandbox/create
Content-Type: application/json

{
  "session_id": "session_001",
  "config": {
    "max_memory": 268435456,
    "max_cpu_time": 30,
    "max_file_size": 10485760
  }
}
```

**销毁沙箱**
```http
DELETE http://localhost:8004/api/capability/sandbox/{sandbox_id}
```

#### 资源管理

**获取资源状态**
```http
GET http://localhost:8004/api/capability/resource/status
```

**响应示例：**
```json
{
  "status": "success",
  "resources": {
    "cpu": {
      "percent": 25.5,
      "count": 8
    },
    "memory": {
      "total": 17179869184,
      "available": 8589934592,
      "percent": 50.0
    },
    "disk": {
      "total": 512110190592,
      "used": 256055095296,
      "percent": 50.0
    }
  }
}
```

#### 结果收集

**获取执行结果**
```http
GET http://localhost:8004/api/capability/result/{session_id}
```

#### WebSocket实时执行

**连接地址：**
```
ws://localhost:8004/ws/capability
```

**发送执行请求：**
```json
{
  "type": "execute",
  "tool_name": "file_read",
  "parameters": {
    "file_path": "test.txt"
  },
  "session_id": "session_001"
}
```

**接收实时更新：**
```json
{
  "type": "status",
  "message": "Executing file_read..."
}
```

#### 内置技能

能力服务提供10种内置技能：

**文件操作类：**
1. **file_read**：读取文件内容
2. **file_write**：写入文件内容
3. **file_delete**：删除文件
4. **file_search**：搜索文件

**浏览器操作类：**
5. **browser_open**：打开URL
6. **browser_click**：点击元素
7. **browser_input**：输入文本

**API调用类：**
8. **api_get**：GET请求
9. **api_post**：POST请求

**代码执行类：**
10. **code_execute**：执行Python代码

---

## API文档

### 接入服务API

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/access/message` | POST | 发送消息 |
| `/api/access/stream` | POST | 流式消息处理 |
| `/ws` | WebSocket | WebSocket连接 |

### 控制服务API

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/logout` | POST | 用户登出 |
| `/api/auth/check_permission` | POST | 检查权限 |
| `/api/session/create` | POST | 创建会话 |
| `/api/session/{session_id}` | GET | 获取会话 |
| `/api/session/update` | POST | 更新会话 |
| `/api/router/route` | POST | 路由消息 |
| `/api/realtime/output` | POST | 实时输出 |

### 实时输出服务API

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/realtime/stream/{session_id}` | GET | 流式输出 |
| `/api/realtime/send` | POST | 发送消息 |
| `/api/realtime/broadcast` | POST | 广播消息 |
| `/ws/realtime` | WebSocket | WebSocket连接 |

### 执行服务API

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/execution/execute` | POST | 执行任务 |
| `/api/execution/stream` | POST | 流式执行任务 |
| `/ws/execution` | WebSocket | WebSocket实时执行 |

### 能力服务API

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/capability/skill/register` | POST | 注册技能 |
| `/api/capability/skill/list` | GET | 列出所有技能 |
| `/api/capability/skill/{skill_id}` | GET | 获取技能信息 |
| `/api/capability/skill/{skill_id}` | DELETE | 注销技能 |
| `/api/capability/execute` | POST | 执行工具 |
| `/api/capability/execute/batch` | POST | 批量执行工具 |
| `/api/capability/sandbox/create` | POST | 创建沙箱 |
| `/api/capability/sandbox/{sandbox_id}` | DELETE | 销毁沙箱 |
| `/api/capability/resource/status` | GET | 获取资源状态 |
| `/api/capability/result/{session_id}` | GET | 获取执行结果 |
| `/ws/capability` | WebSocket | WebSocket实时执行 |

---

## 配置说明

### 环境变量配置

创建 `.env` 文件配置环境变量：

```env
# 模型配置
MODEL_NAME=Qwen/Qwen3-8B
API_KEY=your_api_key_here
API_URL=https://api.siliconflow.cn/v1

# 服务配置
ACCESS_SERVICE_PORT=8000
CONTROL_SERVICE_PORT=8001
REALTIME_SERVICE_PORT=8002

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/octopus.log
```

### 服务配置文件

配置文件位于 `src/config.py`，可以修改以下配置：

```python
class Config:
    # 服务配置
    ACCESS_SERVICE_HOST = "0.0.0.0"
    ACCESS_SERVICE_PORT = 8000
    
    CONTROL_SERVICE_HOST = "0.0.0.0"
    CONTROL_SERVICE_PORT = 8001
    
    REALTIME_SERVICE_HOST = "0.0.0.0"
    REALTIME_SERVICE_PORT = 8002
    
    # 模型配置
    MODEL_NAME = os.environ.get('MODEL_NAME', 'Qwen/Qwen3-8B')
    API_KEY = os.environ.get('API_KEY', 'your_api_key')
    API_URL = os.environ.get('API_URL', 'https://api.siliconflow.cn/v1')
```

---

## 测试指南

### 运行所有测试

```bash
python tests/run_all_tests.py
```

### 运行单个服务测试

**接入服务测试：**
```bash
python tests/test_access_service.py
```

**控制服务测试：**
```bash
python tests/test_control_service.py
```

**实时输出服务测试：**
```bash
python tests/test_realtime_service.py
```

### 测试报告

测试报告会自动生成在 `test_reports/` 目录下：
- `test_report.html` - 单个服务测试报告
- `comprehensive_test_report.html` - 综合测试报告

---

## 故障排除

### 常见问题

#### 1. 端口被占用

**错误信息：**
```
OSError: [Errno 98] Address already in use
```

**解决方法：**

Windows:
```bash
# 查找占用端口的进程
netstat -ano | findstr :8000

# 终止进程
taskkill /PID <进程ID> /F
```

Linux/macOS:
```bash
# 查找占用端口的进程
lsof -i :8000

# 终止进程
kill -9 <进程ID>
```

#### 2. 模块导入错误

**错误信息：**
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方法：**
```bash
# 确保已激活虚拟环境
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

#### 3. WebSocket连接失败

**错误信息：**
```
server rejected WebSocket connection: HTTP 404
```

**解决方法：**
1. 确认服务已启动
2. 检查WebSocket端点是否正确
3. 重启服务

#### 4. 编码错误

**错误信息：**
```
UnicodeEncodeError: 'gbk' codec can't encode character
```

**解决方法：**
- Windows系统使用PowerShell或CMD运行程序
- 确保文件编码为UTF-8

### 日志查看

日志文件位于 `logs/` 目录下，可以通过日志排查问题：

```bash
# 查看最新日志
tail -f logs/octopus.log

# 搜索错误日志
grep "ERROR" logs/octopus.log
```

### 获取帮助

如果遇到无法解决的问题，可以通过以下方式获取帮助：

1. 查看项目文档：`doc/` 目录
2. 查看测试用例：`tests/` 目录
3. 提交Issue：GitHub Issues

---

## 附录

### 项目结构

```
2603_03/
├── doc/                    # 文档目录
│   └── 01/
│       └── charter/        # 产品规划文档
├── src/                    # 源代码目录
│   ├── common/             # 公共模块
│   ├── services/           # 微服务目录
│   │   ├── access/         # 接入服务
│   │   ├── control/        # 控制服务
│   │   └── realtime/       # 实时输出服务
│   ├── cli.py              # 命令行接口
│   ├── config.py           # 配置文件
│   ├── main.py             # 主程序入口
│   └── model_client.py     # 模型客户端
├── tests/                  # 测试目录
│   ├── config.py           # 测试配置
│   ├── utils.py            # 测试工具
│   ├── test_access_service.py      # 接入服务测试
│   ├── test_control_service.py     # 控制服务测试
│   ├── test_realtime_service.py    # 实时输出服务测试
│   └── run_all_tests.py    # 主测试脚本
├── test_reports/           # 测试报告目录
├── requirements.txt        # 依赖列表
├── start.bat               # Windows启动脚本
└── README.md               # 项目说明
```

### 依赖列表

主要依赖包：

```
fastapi>=0.104.0
uvicorn>=0.24.0
websockets>=12.0
aiohttp>=3.9.0
python-jose>=3.3.0
python-multipart>=0.0.6
```

### 版本历史

- **v0.4.0 RC** (2026-03-27)
  - 完成能力服务开发
  - 实现技能管理系统
  - 实现工具执行引擎
  - 实现沙箱环境
  - 实现资源管理
  - 完成10种内置技能
  - 完成能力服务测试（10个测试用例全部通过）
  - **新增Web界面交互能力**
    - 实现Vue 3 + Element Plus前端框架
    - 创建智能对话界面
    - 创建服务状态监控界面
    - 创建技能管理界面
    - 创建历史记录界面
    - 集成WebSocket实时通信
    - 实现本地资源加载（无外部CDN依赖）
    - 创建专门的Web界面启动脚本

- **v0.3.0 Beta** (2026-03-27)
  - 完成执行服务开发
  - 实现ReAct循环引擎
  - 实现意图理解和任务拆解
  - 实现工具选择和调用
  - 实现上下文管理
  - 完成执行服务测试（10个测试用例全部通过）

- **v0.2.0 Alpha** (2026-03-27)
  - 完成接入服务、控制服务、实时输出服务
  - 实现用户认证和会话管理
  - 支持WebSocket实时通信
  - 完成全部测试用例

- **v0.1.0 MVP** (2026-03-26)
  - 项目初始化
  - 基础架构搭建
  - 核心功能验证

---

**文档版本：** v1.2  
**创建日期：** 2026-03-27  
**最后更新：** 2026-03-27  
**维护者：** 八爪鱼开发团队
