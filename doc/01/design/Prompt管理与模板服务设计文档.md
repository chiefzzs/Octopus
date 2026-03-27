# 八爪鱼（Octopus）Prompt管理与模板服务设计文档

## 文档信息

- **文档版本**: v1.0
- **创建日期**: 2026-03-27
- **作者**: 八爪鱼产品团队
- **文档类型**: 设计文档
- **适用范围**: 八爪鱼AI智能体Prompt统一管理

---

## 1. 文档概述

本文档定义了八爪鱼AI智能体的大模型Prompt统一管理和模板服务方案，实现所有内部使用大模型的Prompt的集中管理、版本控制和动态加载。

**设计目标**：
- 统一管理所有Prompt模板，避免散落在代码中
- 支持按模块和名称组织Prompt，便于查找和维护
- 支持Prompt版本管理，方便回滚和A/B测试
- 支持动态加载和热更新，无需重启服务
- 提供Prompt模板变量替换功能
- 支持多语言和多模型适配

---

## 2. 设计原则

### 2.1 核心原则

| 原则 | 说明 | 实现方式 |
|------|------|----------|
| **集中管理** | 所有Prompt集中存储和管理 | 文件系统 + 数据库 |
| **模块化组织** | 按模块和名称组织Prompt | 目录结构 + 命名规范 |
| **版本控制** | 支持Prompt版本管理 | Git + 数据库版本表 |
| **动态加载** | 支持运行时动态加载和更新 | 文件监听 + 缓存失效 |
| **变量替换** | 支持Prompt模板变量替换 | Jinja2模板引擎 |
| **多模型适配** | 支持不同模型的Prompt格式 | 模型适配器 |

### 2.2 Prompt命名规范

```
{模块名}/{功能名}/{Prompt名称}.yaml

示例：
- execution/intent/analyze_intent.yaml
- execution/planning/decompose_task.yaml
- model/function_calling/generate_parameters.yaml
- capability/tool/execute_tool.yaml
```

---

## 3. 架构设计

### 3.1 服务架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      Prompt管理服务                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Prompt加载器   │  │  Prompt解析器   │  │  Prompt缓存     │  │
│  │  (Loader)       │  │  (Parser)       │  │  (Cache)        │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           └────────────────────┴────────────────────┘           │
│                                │                                │
└────────────────────────────────┼────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐    ┌──────────▼──────────┐  ┌─────────▼─────────┐
│  Prompt存储     │    │   Prompt版本管理    │  │  Prompt模板引擎   │
│  (Storage)      │    │   (Version Control) │  │  (Template Engine)│
│  - 文件系统     │    │   - Git集成         │  │  - Jinja2         │
│  - 数据库       │    │   - 版本回滚       │  │  - 变量替换       │
└─────────────────┘    └─────────────────────┘  └───────────────────┘
```

### 3.2 目录结构

```
prompts/
├── templates/                  # Prompt模板目录
│   ├── execution/             # 执行服务Prompt
│   │   ├── intent/            # 意图识别
│   │   │   ├── analyze_intent.yaml
│   │   │   └── extract_entities.yaml
│   │   ├── planning/          # 任务规划
│   │   │   ├── decompose_task.yaml
│   │   │   └── generate_plan.yaml
│   │   └── react/             # ReAct循环
│   │       ├── generate_thought.yaml
│   │       └── observe_result.yaml
│   ├── model/                 # 模型服务Prompt
│   │   ├── function_calling/  # Function Calling
│   │   │   ├── select_tool.yaml
│   │   │   └── generate_parameters.yaml
│   │   └── chat/              # 聊天
│   │       └── system_prompt.yaml
│   ├── capability/            # 能力服务Prompt
│   │   └── tool/              # 工具执行
│   │       ├── validate_parameters.yaml
│   │       └── format_result.yaml
│   └── common/                # 通用Prompt
│       ├── error_handling.yaml
│       └── retry_strategy.yaml
├── versions/                  # 版本历史
│   └── .git/                  # Git仓库
├── config/                    # 配置文件
│   ├── prompt_config.yaml     # Prompt配置
│   └── model_config.yaml      # 模型配置
└── tests/                     # 测试用例
    ├── test_intent.yaml
    └── test_planning.yaml
```

---

## 4. Prompt模板定义

### 4.1 Prompt模板格式

```yaml
# prompts/execution/intent/analyze_intent.yaml
metadata:
  name: analyze_intent
  module: execution
  sub_module: intent
  version: 1.0.0
  description: 分析用户意图，识别主要意图和所需工具
  author: octopus-team
  created_at: 2026-03-27
  updated_at: 2026-03-27
  tags:
    - intent-recognition
    - tool-selection
  models:
    - gpt-4
    - gpt-3.5-turbo
    - claude-3-opus

template: |
  你是一个任务分析专家，能够准确分析用户输入的意图和所需的工具。
  
  ## 你的能力
  1. 理解用户的真实意图，而非简单的关键字匹配
  2. 识别完成任务所需的工具
  3. 评估任务的复杂度
  4. 提取关键实体信息
  
  ## 可用工具
  {% for tool in tools %}
  - **{{ tool.name }}**: {{ tool.description }}
  {% endfor %}
  
  ## 任务复杂度评估标准
  - **simple**: 单一工具调用，参数简单
  - **medium**: 多个工具调用，或有复杂参数
  - **complex**: 需要多步骤执行，或需要任务分解
  
  ## 用户输入
  {{ user_input }}
  
  ## 上下文信息
  {% if context %}
  - 会话历史: {{ context.history }}
  - 用户偏好: {{ context.preferences }}
  {% endif %}
  
  请分析用户意图，并返回以下信息：
  1. 主要意图
  2. 所需工具列表
  3. 任务复杂度
  4. 关键实体信息
  5. 置信度评分

variables:
  - name: user_input
    type: string
    required: true
    description: 用户输入内容
  - name: tools
    type: array
    required: true
    description: 可用工具列表
  - name: context
    type: object
    required: false
    description: 上下文信息
    properties:
      history:
        type: array
        description: 会话历史
      preferences:
        type: object
        description: 用户偏好

output_format:
  type: function_call
  function_name: analyze_intent
  parameters:
    intent:
      type: string
      description: 主要意图
    required_tools:
      type: array
      items:
        type: string
      description: 所需工具列表
    complexity:
      type: string
      enum: [simple, medium, complex]
      description: 任务复杂度
    entities:
      type: object
      description: 关键实体信息
    confidence:
      type: float
      minimum: 0
      maximum: 1
      description: 置信度评分

examples:
  - input:
      user_input: "请生成python排序代码"
      tools:
        - name: code_generator
          description: 生成代码
      context: null
    output:
      intent: code_generation
      required_tools: ["code_generator"]
      complexity: simple
      entities:
        language: python
        task: sorting
      confidence: 0.95
```

### 4.2 Prompt模板类型

| 类型 | 用途 | 示例 |
|------|------|------|
| **系统Prompt** | 定义AI的角色和能力 | system_prompt.yaml |
| **任务Prompt** | 描述具体任务要求 | analyze_intent.yaml |
| **Few-shot Prompt** | 提供示例引导模型 | code_generation.yaml |
| **Function Calling Prompt** | 定义工具调用规范 | select_tool.yaml |
| **ReAct Prompt** | 引导推理和行动循环 | generate_thought.yaml |

---

## 5. Prompt管理服务设计

### 5.1 服务架构

```python
# services/prompt/
prompt/
├── __init__.py
├── app.py                      # FastAPI应用入口
├── config.py                   # 配置管理
├── modules/                    # 核心模块
│   ├── __init__.py
│   ├── loader/                 # Prompt加载器
│   │   ├── __init__.py
│   │   ├── file_loader.py      # 文件加载器
│   │   ├── db_loader.py        # 数据库加载器
│   │   └── cache_loader.py     # 缓存加载器
│   ├── parser/                 # Prompt解析器
│   │   ├── __init__.py
│   │   ├── yaml_parser.py      # YAML解析器
│   │   └── validator.py        # 验证器
│   ├── template/               # 模板引擎
│   │   ├── __init__.py
│   │   ├── jinja2_engine.py    # Jinja2引擎
│   │   └── variable_replacer.py # 变量替换器
│   ├── version/                # 版本管理
│   │   ├── __init__.py
│   │   ├── git_manager.py      # Git管理器
│   │   └── version_manager.py  # 版本管理器
│   └── cache/                  # 缓存管理
│       ├── __init__.py
│       ├── memory_cache.py     # 内存缓存
│       └── redis_cache.py      # Redis缓存
├── models/                     # 数据模型
│   ├── __init__.py
│   ├── prompt.py               # Prompt模型
│   ├── template.py             # 模板模型
│   └── version.py              # 版本模型
└── storage/                    # 存储层
    ├── __init__.py
    ├── file_storage.py         # 文件存储
    └── db_storage.py           # 数据库存储
```

### 5.2 核心实现

#### 5.2.1 Prompt管理器

```python
# services/prompt/modules/manager.py
from typing import Dict, List, Optional
from pathlib import Path
import yaml
from jinja2 import Template
from pydantic import BaseModel

class PromptTemplate(BaseModel):
    """Prompt模板"""
    name: str
    module: str
    sub_module: str
    version: str
    description: str
    template: str
    variables: List[dict]
    output_format: dict
    examples: List[dict]

class PromptManager:
    """
    Prompt管理器
    
    职责：
    1. 加载和解析Prompt模板
    2. 管理Prompt版本
    3. 提供Prompt渲染接口
    4. 缓存管理
    """
    
    def __init__(
        self,
        template_dir: str = "prompts/templates",
        cache_enabled: bool = True
    ):
        self.template_dir = Path(template_dir)
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, PromptTemplate] = {}
        self._template_cache: Dict[str, Template] = {}
    
    def get_prompt(
        self,
        module: str,
        sub_module: str,
        name: str,
        version: Optional[str] = None
    ) -> PromptTemplate:
        """
        获取Prompt模板
        
        Args:
            module: 模块名
            sub_module: 子模块名
            name: Prompt名称
            version: 版本号（可选，默认最新版本）
            
        Returns:
            PromptTemplate: Prompt模板
        """
        # 生成缓存键
        cache_key = f"{module}/{sub_module}/{name}"
        if version:
            cache_key += f":{version}"
        
        # 检查缓存
        if self.cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]
        
        # 加载Prompt文件
        prompt_file = self._find_prompt_file(module, sub_module, name)
        if not prompt_file:
            raise PromptNotFoundError(f"Prompt not found: {cache_key}")
        
        # 解析Prompt
        with open(prompt_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 验证版本
        if version and data['metadata']['version'] != version:
            # 加载指定版本
            data = self._load_version(prompt_file, version)
        
        # 创建Prompt模板对象
        prompt_template = PromptTemplate(
            name=data['metadata']['name'],
            module=data['metadata']['module'],
            sub_module=data['metadata']['sub_module'],
            version=data['metadata']['version'],
            description=data['metadata']['description'],
            template=data['template'],
            variables=data['variables'],
            output_format=data['output_format'],
            examples=data.get('examples', [])
        )
        
        # 缓存
        if self.cache_enabled:
            self._cache[cache_key] = prompt_template
        
        return prompt_template
    
    def render_prompt(
        self,
        module: str,
        sub_module: str,
        name: str,
        variables: dict,
        version: Optional[str] = None
    ) -> str:
        """
        渲染Prompt
        
        Args:
            module: 模块名
            sub_module: 子模块名
            name: Prompt名称
            variables: 变量值
            version: 版本号（可选）
            
        Returns:
            str: 渲染后的Prompt
        """
        # 获取Prompt模板
        prompt_template = self.get_prompt(module, sub_module, name, version)
        
        # 检查缓存
        cache_key = f"{module}/{sub_module}/{name}:{prompt_template.version}"
        if cache_key in self._template_cache:
            template = self._template_cache[cache_key]
        else:
            # 创建Jinja2模板
            template = Template(prompt_template.template)
            if self.cache_enabled:
                self._template_cache[cache_key] = template
        
        # 渲染模板
        return template.render(**variables)
    
    def _find_prompt_file(
        self,
        module: str,
        sub_module: str,
        name: str
    ) -> Optional[Path]:
        """查找Prompt文件"""
        prompt_file = self.template_dir / module / sub_module / f"{name}.yaml"
        if prompt_file.exists():
            return prompt_file
        return None
    
    def _load_version(self, prompt_file: Path, version: str) -> dict:
        """加载指定版本的Prompt"""
        # 使用Git加载历史版本
        # 实现略
        pass
    
    def list_prompts(
        self,
        module: Optional[str] = None,
        sub_module: Optional[str] = None
    ) -> List[dict]:
        """
        列出Prompt
        
        Args:
            module: 模块名（可选）
            sub_module: 子模块名（可选）
            
        Returns:
            List[dict]: Prompt列表
        """
        prompts = []
        
        # 遍历模板目录
        search_path = self.template_dir
        if module:
            search_path = search_path / module
            if sub_module:
                search_path = search_path / sub_module
        
        for prompt_file in search_path.rglob("*.yaml"):
            with open(prompt_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            prompts.append({
                "name": data['metadata']['name'],
                "module": data['metadata']['module'],
                "sub_module": data['metadata']['sub_module'],
                "version": data['metadata']['version'],
                "description": data['metadata']['description']
            })
        
        return prompts
    
    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()
        self._template_cache.clear()
```

#### 5.2.2 Prompt服务API

```python
# services/prompt/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(title="Prompt Management Service")

class GetPromptRequest(BaseModel):
    """获取Prompt请求"""
    module: str
    sub_module: str
    name: str
    version: Optional[str] = None

class RenderPromptRequest(BaseModel):
    """渲染Prompt请求"""
    module: str
    sub_module: str
    name: str
    variables: Dict
    version: Optional[str] = None

class PromptResponse(BaseModel):
    """Prompt响应"""
    name: str
    module: str
    sub_module: str
    version: str
    description: str
    template: str
    variables: List[dict]
    output_format: dict

@app.post("/api/prompt/get", response_model=PromptResponse)
async def get_prompt(request: GetPromptRequest):
    """获取Prompt模板"""
    try:
        prompt = prompt_manager.get_prompt(
            request.module,
            request.sub_module,
            request.name,
            request.version
        )
        return PromptResponse(
            name=prompt.name,
            module=prompt.module,
            sub_module=prompt.sub_module,
            version=prompt.version,
            description=prompt.description,
            template=prompt.template,
            variables=prompt.variables,
            output_format=prompt.output_format
        )
    except PromptNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/prompt/render")
async def render_prompt(request: RenderPromptRequest):
    """渲染Prompt"""
    try:
        rendered = prompt_manager.render_prompt(
            request.module,
            request.sub_module,
            request.name,
            request.variables,
            request.version
        )
        return {"rendered_prompt": rendered}
    except PromptNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TemplateError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/prompt/list")
async def list_prompts(
    module: Optional[str] = None,
    sub_module: Optional[str] = None
):
    """列出Prompt"""
    prompts = prompt_manager.list_prompts(module, sub_module)
    return {"prompts": prompts}

@app.post("/api/prompt/cache/clear")
async def clear_cache():
    """清除缓存"""
    prompt_manager.clear_cache()
    return {"message": "Cache cleared"}
```

---

## 6. 使用示例

### 6.1 在执行服务中使用

```python
# services/execution/modules/intent/analyzer.py
from services.prompt.client import PromptClient

class IntentAnalyzer:
    """意图分析器"""
    
    def __init__(self, prompt_client: PromptClient, model_client: ModelClient):
        self.prompt_client = prompt_client
        self.model_client = model_client
    
    async def analyze(self, user_input: str, context: dict, tools: List[Tool]) -> dict:
        """
        分析用户意图
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            tools: 可用工具列表
            
        Returns:
            dict: 意图分析结果
        """
        # 1. 获取Prompt模板
        prompt = self.prompt_client.render_prompt(
            module="execution",
            sub_module="intent",
            name="analyze_intent",
            variables={
                "user_input": user_input,
                "context": context,
                "tools": tools
            }
        )
        
        # 2. 调用模型
        request = {
            "messages": [
                {"role": "system", "content": prompt}
            ],
            "tools": [self._get_intent_analysis_tool()],
            "stream": True
        }
        
        response = await self.model_client.chat_completion(request)
        
        # 3. 解析结果
        return self._parse_response(response)
```

### 6.2 在模型服务中使用

```python
# services/model/modules/call/function_calling.py
from services.prompt.client import PromptClient

class FunctionCallingService:
    """Function Calling服务"""
    
    def __init__(self, prompt_client: PromptClient):
        self.prompt_client = prompt_client
    
    async def select_tool(
        self,
        user_input: str,
        available_tools: List[Tool]
    ) -> Tool:
        """
        选择合适的工具
        
        Args:
            user_input: 用户输入
            available_tools: 可用工具列表
            
        Returns:
            Tool: 选择的工具
        """
        # 获取工具选择Prompt
        prompt = self.prompt_client.render_prompt(
            module="model",
            sub_module="function_calling",
            name="select_tool",
            variables={
                "user_input": user_input,
                "available_tools": available_tools
            }
        )
        
        # 调用模型
        # ...
```

### 6.3 Prompt客户端

```python
# common/clients/prompt_client.py
import httpx
from typing import Dict, List, Optional

class PromptClient:
    """Prompt客户端"""
    
    def __init__(self, base_url: str = "http://prompt-service:8006"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def get_prompt(
        self,
        module: str,
        sub_module: str,
        name: str,
        version: Optional[str] = None
    ) -> dict:
        """获取Prompt模板"""
        response = await self.client.post(
            f"{self.base_url}/api/prompt/get",
            json={
                "module": module,
                "sub_module": sub_module,
                "name": name,
                "version": version
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def render_prompt(
        self,
        module: str,
        sub_module: str,
        name: str,
        variables: Dict,
        version: Optional[str] = None
    ) -> str:
        """渲染Prompt"""
        response = await self.client.post(
            f"{self.base_url}/api/prompt/render",
            json={
                "module": module,
                "sub_module": sub_module,
                "name": name,
                "variables": variables,
                "version": version
            }
        )
        response.raise_for_status()
        return response.json()["rendered_prompt"]
    
    async def list_prompts(
        self,
        module: Optional[str] = None,
        sub_module: Optional[str] = None
    ) -> List[dict]:
        """列出Prompt"""
        params = {}
        if module:
            params["module"] = module
        if sub_module:
            params["sub_module"] = sub_module
        
        response = await self.client.get(
            f"{self.base_url}/api/prompt/list",
            params=params
        )
        response.raise_for_status()
        return response.json()["prompts"]
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
```

---

## 7. 版本管理

### 7.1 Git集成

```python
# services/prompt/modules/version/git_manager.py
import git
from pathlib import Path
from typing import List, Optional

class GitVersionManager:
    """Git版本管理器"""
    
    def __init__(self, repo_path: str = "prompts/versions"):
        self.repo_path = Path(repo_path)
        self.repo = git.Repo(self.repo_path)
    
    def get_versions(self, prompt_file: str) -> List[str]:
        """获取Prompt的所有版本"""
        commits = list(self.repo.iter_commits(paths=prompt_file))
        return [commit.hexsha[:7] for commit in commits]
    
    def get_version_content(self, prompt_file: str, version: str) -> str:
        """获取指定版本的Prompt内容"""
        commit = self.repo.commit(version)
        blob = commit.tree[prompt_file]
        return blob.data_stream.read().decode('utf-8')
    
    def create_version(self, message: str) -> str:
        """创建新版本"""
        self.repo.index.add(["templates/"])
        commit = self.repo.index.commit(message)
        return commit.hexsha[:7]
    
    def rollback(self, version: str):
        """回滚到指定版本"""
        self.repo.git.checkout(version)
```

### 7.2 版本策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **语义化版本** | 主版本.次版本.修订版本 | 正式发布 |
| **时间戳版本** | YYYYMMDD-HHMMSS | 开发测试 |
| **Git Commit** | Git commit hash | 精确回滚 |

---

## 8. 配置管理

### 8.1 Prompt配置

```yaml
# prompts/config/prompt_config.yaml
prompt_service:
  # 模板目录
  template_dir: "prompts/templates"
  
  # 版本目录
  version_dir: "prompts/versions"
  
  # 缓存配置
  cache:
    enabled: true
    type: "memory"  # memory | redis
    ttl: 3600  # 缓存过期时间（秒）
  
  # 版本管理
  version_control:
    enabled: true
    type: "git"  # git | database
    auto_commit: true
  
  # 模板引擎
  template_engine:
    type: "jinja2"
    autoescape: false
  
  # 监听配置
  watch:
    enabled: true
    interval: 5  # 监听间隔（秒）
```

### 8.2 模型配置

```yaml
# prompts/config/model_config.yaml
models:
  gpt-4:
    provider: openai
    max_tokens: 4096
    temperature: 0.7
    prompt_format: "chat"
  
  gpt-3.5-turbo:
    provider: openai
    max_tokens: 4096
    temperature: 0.7
    prompt_format: "chat"
  
  claude-3-opus:
    provider: anthropic
    max_tokens: 4096
    temperature: 0.7
    prompt_format: "messages"
```

---

## 9. 部署架构

### 9.1 Docker Compose

```yaml
# docker-compose.yml
services:
  # Prompt管理服务
  prompt-service:
    build: ./services/prompt
    ports:
      - "8006:8006"
    volumes:
      - ./prompts/templates:/app/prompts/templates
      - ./prompts/versions:/app/prompts/versions
      - ./prompts/config:/app/prompts/config
    environment:
      - CACHE_ENABLED=true
      - WATCH_ENABLED=true
    depends_on:
      - redis

  # Redis（缓存）
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### 9.2 Kubernetes

```yaml
# kubernetes/prompt-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prompt-service
  labels:
    app: prompt-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: prompt-service
  template:
    metadata:
      labels:
        app: prompt-service
    spec:
      containers:
      - name: prompt-service
        image: octopus/prompt-service:latest
        ports:
        - containerPort: 8006
        volumeMounts:
        - name: prompts-templates
          mountPath: /app/prompts/templates
        - name: prompt-config
          mountPath: /app/prompts/config
        env:
        - name: CACHE_ENABLED
          value: "true"
        - name: WATCH_ENABLED
          value: "true"
      volumes:
      - name: prompts-templates
        configMap:
          name: prompts-templates
      - name: prompt-config
        configMap:
          name: prompt-config
---
apiVersion: v1
kind: Service
metadata:
  name: prompt-service
spec:
  selector:
    app: prompt-service
  ports:
  - port: 8006
    targetPort: 8006
  type: ClusterIP
```

---

## 10. 监控与日志

### 10.1 监控指标

| 指标类型 | 指标名称 | 说明 |
|----------|----------|------|
| **性能指标** | prompt_load_time | Prompt加载时间 |
| | prompt_render_time | Prompt渲染时间 |
| | cache_hit_rate | 缓存命中率 |
| **质量指标** | prompt_usage_count | Prompt使用次数 |
| | prompt_error_rate | Prompt错误率 |
| **资源指标** | memory_usage | 内存使用量 |
| | cache_size | 缓存大小 |

### 10.2 日志规范

```json
{
  "timestamp": "2026-03-27T10:30:00Z",
  "level": "INFO",
  "service": "prompt-service",
  "module": "PromptManager",
  "action": "render_prompt",
  "data": {
    "module": "execution",
    "sub_module": "intent",
    "name": "analyze_intent",
    "version": "1.0.0",
    "render_time_ms": 15,
    "cache_hit": true
  }
}
```

---

## 11. 实施计划

### 11.1 第一阶段（2周）：基础功能

| 周次 | 任务 | 交付物 |
|------|------|--------|
| 第1周 | Prompt管理器开发 | PromptManager、PromptTemplate |
| 第2周 | Prompt服务API开发 | REST API、客户端SDK |

### 11.2 第二阶段（2周）：高级功能

| 周次 | 任务 | 交付物 |
|------|------|--------|
| 第3周 | 版本管理开发 | Git集成、版本回滚 |
| 第4周 | 缓存和监听 | 缓存管理、文件监听 |

### 11.3 第三阶段（2周）：集成优化

| 周次 | 任务 | 交付物 |
|------|------|--------|
| 第5周 | 服务集成 | 执行服务、模型服务集成 |
| 第6周 | 测试和文档 | 单元测试、集成测试、文档 |

---

## 12. 最佳实践

### 12.1 Prompt编写规范

1. **清晰的结构**：使用Markdown格式，清晰的标题和段落
2. **明确的指令**：使用祈使句，明确告诉模型要做什么
3. **示例引导**：提供Few-shot示例，引导模型理解
4. **变量占位**：使用Jinja2语法标记变量位置
5. **版本标注**：在metadata中标注版本和更新说明

### 12.2 性能优化

1. **缓存策略**：启用缓存，减少重复加载
2. **预加载**：服务启动时预加载常用Prompt
3. **异步加载**：使用异步IO，避免阻塞
4. **批量渲染**：支持批量渲染，减少网络开销

### 12.3 安全考虑

1. **输入验证**：验证变量类型和格式
2. **输出过滤**：过滤敏感信息
3. **访问控制**：限制Prompt访问权限
4. **审计日志**：记录Prompt使用情况

---

## 13. 结论

本文档定义了八爪鱼AI智能体的Prompt统一管理和模板服务方案，实现了：

1. **集中管理**：所有Prompt集中存储和管理
2. **模块化组织**：按模块和名称组织Prompt
3. **版本控制**：支持Prompt版本管理
4. **动态加载**：支持运行时动态加载和更新
5. **变量替换**：支持Prompt模板变量替换
6. **多模型适配**：支持不同模型的Prompt格式

通过统一的Prompt管理服务，可以：
- 提高Prompt的可维护性
- 方便Prompt的优化和迭代
- 支持A/B测试和效果评估
- 降低开发和维护成本

---

**文档结束**

**变更历史**:
- v1.0 (2026-03-27): 初始版本
