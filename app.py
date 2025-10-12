import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config

# 加载环境变量
load_dotenv()

# 初始化数据库
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 注册蓝图
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

# 创建应用实例
app = create_app()

# 应用上下文处理器
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db}

if __name__ == '__main__':
    app.run(debug=True)