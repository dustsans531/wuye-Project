# routes包初始化文件

from flask import Blueprint

# 创建API蓝图
api_bp = Blueprint('api', __name__)

# 导入各个路由模块
from . import user_routes
from . import property_routes
from . import owner_routes
from . import maintenance_routes
from . import payment_routes
from . import announcement_routes

__all__ = ['api_bp']