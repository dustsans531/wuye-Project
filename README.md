# 物业管理系统 - 后台框架

## 项目介绍
这是一个使用Python和MySQL构建的物业管理系统后台框架，提供了业主管理、物业信息管理、维修请求处理、费用支付和公告发布等功能。

## 技术栈
- Python 3.8+
- Flask 2.3.2
- Flask-SQLAlchemy 3.0.3 (ORM)
- Flask-Migrate 4.0.4 (数据库迁移)
- Flask-RESTful 0.3.9 (RESTful API)
- PyMySQL 1.0.3 (MySQL驱动)
- python-dotenv 1.0.0 (环境变量管理)
- bcrypt 4.0.1 (密码加密)

## 项目结构
```
wuye-Project/
├── app/                  # 应用程序主目录
│   ├── __init__.py       # 包初始化文件
│   ├── models/           # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── property.py   # 物业模型
│   │   ├── owner.py      # 业主模型
│   │   ├── maintenance.py # 维修请求模型
│   │   ├── payment.py    # 支付模型
│   │   └── announcement.py # 公告模型
│   └── routes/           # API路由
│       ├── __init__.py   # 路由初始化
│       ├── user_routes.py # 用户路由
│       ├── property_routes.py # 物业路由
│       ├── owner_routes.py # 业主路由
│       ├── maintenance_routes.py # 维修请求路由
│       ├── payment_routes.py # 支付路由
│       └── announcement_routes.py # 公告路由
├── app.py                # 主应用程序入口
├── config.py             # 配置文件
├── .env                  # 环境变量配置
├── requirements.txt      # 项目依赖
└── .gitignore            # Git忽略文件
```

## 安装指南

### 1. 克隆项目
```bash
git clone <repository-url>
cd wuye-Project
```

### 2. 创建虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
编辑 `.env` 文件，设置数据库连接信息和密钥：
```
# 开发环境数据库
DEV_DATABASE_URL=mysql+pymysql://root:password@localhost/wuye_db

# 测试环境数据库
TEST_DATABASE_URL=mysql+pymysql://root:password@localhost/wuye_test_db

# 密钥配置
SECRET_KEY=your-secret-key-here

# Flask配置
FLASK_APP=app.py
FLASK_ENV=development
```

### 5. 初始化数据库
```bash
# 创建数据库迁移仓库
flask db init

# 创建初始迁移
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

### 6. 运行应用
```bash
flask run
```

## API 端点

### 用户管理
- `GET /api/users` - 获取所有用户
- `GET /api/users/<id>` - 获取单个用户
- `POST /api/users` - 创建新用户
- `PUT /api/users/<id>` - 更新用户信息
- `DELETE /api/users/<id>` - 删除用户

### 物业信息管理
- `GET /api/properties` - 获取所有物业
- `GET /api/properties/<id>` - 获取单个物业
- `POST /api/properties` - 创建新物业
- `PUT /api/properties/<id>` - 更新物业信息
- `DELETE /api/properties/<id>` - 停用物业

### 业主管理
- `GET /api/owners` - 获取所有业主
- `GET /api/owners/<id>` - 获取单个业主
- `POST /api/owners` - 创建新业主
- `PUT /api/owners/<id>` - 更新业主信息
- `DELETE /api/owners/<id>` - 删除业主

### 维修请求管理
- `GET /api/maintenance` - 获取所有维修请求
- `GET /api/maintenance/<id>` - 获取单个维修请求
- `POST /api/maintenance` - 创建新维修请求
- `PUT /api/maintenance/<id>` - 更新维修请求
- `DELETE /api/maintenance/<id>` - 删除维修请求

### 费用支付管理
- `GET /api/payments` - 获取所有支付记录
- `GET /api/payments/<id>` - 获取单个支付记录
- `POST /api/payments` - 创建新支付记录
- `PUT /api/payments/<id>` - 更新支付记录
- `DELETE /api/payments/<id>` - 删除支付记录

### 公告管理
- `GET /api/announcements` - 获取所有公告
- `GET /api/announcements/<id>` - 获取单个公告
- `POST /api/announcements` - 创建新公告
- `PUT /api/announcements/<id>` - 更新公告
- `DELETE /api/announcements/<id>` - 删除公告

## 后续计划
1. 添加用户认证和授权系统
2. 实现JWT令牌认证
3. 添加分页和过滤功能
4. 实现数据导入/导出功能
5. 添加定时任务（如费用计算、到期提醒）
6. 集成支付系统
7. 完善数据验证和错误处理
8. 添加日志记录系统
9. 编写单元测试
10. 开发前端界面接口

## 注意事项
- 确保MySQL服务已启动并正确配置
- 在生产环境中，请勿使用默认的SECRET_KEY和数据库密码
- 定期备份数据库
- 遵循安全最佳实践