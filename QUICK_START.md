# 八爪鱼快速开始指南

## 1. 启动服务

### Windows系统

双击运行 `start.bat` 文件，脚本会自动完成以下操作：
- 检查Python安装
- 创建虚拟环境
- 安装依赖包
- 启动程序

### 手动启动

```bash
# 1. 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python src/main.py
```

## 2. 验证服务

启动服务后，访问以下URL验证服务是否正常运行：

- 接入服务: http://localhost:8000/health
- 控制服务: http://localhost:8001/health
- 实时输出服务: http://localhost:8002/health
- 执行服务: http://localhost:8003/health
- 能力服务: http://localhost:8004/health

## 3. 快速测试

### 测试HTTP接口

```bash
# 测试接入服务
curl -X POST http://localhost:8000/api/access/message \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"你好\", \"user_id\": \"test\"}"

# 测试控制服务 - 用户注册
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"testuser\", \"password\": \"123456\", \"email\": \"test@example.com\"}"

# 测试控制服务 - 用户登录
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"testuser\", \"password\": \"123456\"}"
```

### 运行测试套件

```bash
# 运行所有测试
python tests/run_all_tests.py

# 运行单个服务测试
python tests/test_access_service.py
python tests/test_control_service.py
python tests/test_realtime_service.py
```

## 4. 常用命令

```bash
# 启动单个服务
python src/services/access/app.py      # 接入服务 (端口8000)
python src/services/control/app.py     # 控制服务 (端口8001)
python src/services/realtime/app.py    # 实时输出服务 (端口8002)

# 查看端口占用
netstat -ano | findstr :8000          # Windows
lsof -i :8000                          # Linux/macOS

# 终止占用端口的进程
taskkill /PID <进程ID> /F              # Windows
kill -9 <进程ID>                       # Linux/macOS
```

## 5. 故障排除

### 端口被占用

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Linux/macOS
lsof -i :8000
kill -9 <进程ID>
```

### 模块导入错误

```bash
# 确保已激活虚拟环境
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS

# 重新安装依赖
pip install -r requirements.txt
```

## 6. 下一步

- 查看详细文档: [USER_MANUAL.md](USER_MANUAL.md)
- 查看测试报告: `test_reports/comprehensive_test_report.html`
- 查看产品规划: `doc/01/charter/产品规划.md`

---

**快速帮助：** 如遇问题，请查看 [USER_MANUAL.md](USER_MANUAL.md) 的故障排除章节。
