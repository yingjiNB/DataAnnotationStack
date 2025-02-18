# 数据标注系统部署文档

## 系统要求

### 硬件要求
- CPU: 2核心及以上
- 内存: 4GB及以上
- 硬盘空间: 10GB及以上

### 软件要求
- Python 3.10+
- Docker 20.10+
- Docker Compose 2.0+
- Git

## 部署方式

### 1. Docker部署（推荐）

1. 克隆代码仓库
```bash
git clone [repository-url]
cd DataAnnotationStack
```

2. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
vim .env

# 必要的环境变量：
DATABASE_URL=sqlite:///./sql_app.db
SECRET_KEY=your-secret-key-here
```

3. 构建和启动服务
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

4. 验证服务
```bash
# 检查服务状态
docker-compose ps

# 检查日志
docker-compose logs -f
```

5. 访问服务
- 前端界面：http://localhost:8501
- 后端API：http://localhost:8000/api/v1
- API文档：http://localhost:8000/docs

### 2. 本地开发环境部署

1. 创建并激活虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 初始化数据库
```bash
# 确保在项目根目录
python -m backend.db.init_db
```

4. 启动服务
```bash
# 启动后端服务
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 新开终端，启动前端服务
cd frontend
streamlit run app.py
```

## 目录结构
```
.
├── backend/
│   ├── api/            # API接口
│   ├── core/           # 核心配置
│   ├── db/             # 数据库相关
│   ├── models/         # 数据模型
│   └── services/       # 业务逻辑
├── frontend/
│   ├── components/     # 前端组件
│   ├── utils/          # 工具函数
│   └── app.py          # 主应用
├── docker/             # Docker配置
├── uploads/            # 文件上传目录
├── requirements.txt    # 依赖文件
└── docker-compose.yml  # Docker编排文件
```

## 配置说明

### 1. 数据库配置
- 默认使用SQLite数据库
- 数据库文件位置：项目根目录下的`sql_app.db`
- 可通过环境变量`DATABASE_URL`修改数据库配置

### 2. 文件存储配置
- 上传文件存储在`uploads`目录
- 支持的文件类型：PDF和JSON
- 单个文件大小限制：16MB

### 3. 安全配置
- 通过`SECRET_KEY`环境变量配置密钥
- CORS配置：默认允许所有来源
- 文件类型验证
- 文件大小限制

## 维护指南

### 1. 日常维护
```bash
# 查看服务状态
docker-compose ps

# 重启服务
docker-compose restart

# 更新代码后重新部署
git pull
docker-compose up -d --build
```

### 2. 数据备份
```bash
# 备份数据库
cp sql_app.db sql_app.db.backup

# 备份上传文件
cp -r uploads uploads.backup
```

### 3. 日志查看
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
```

## 故障排除

### 1. 服务无法启动
- 检查端口占用情况
- 检查环境变量配置
- 检查数据库文件权限
- 查看错误日志

### 2. 文件上传失败
- 检查uploads目录权限
- 检查文件大小是否超限
- 检查磁盘空间是否充足

### 3. 数据库错误
- 检查数据库文件权限
- 确保数据库文件未损坏
- 必要时恢复数据库备份

## 联系支持
如遇到问题，请联系：
- 技术支持邮箱：[support-email]
- 项目维护者：[maintainer-name] 