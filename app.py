"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-29 上午9:21
 *  @ 创建描述   创建全局app对象并且配置好文件参数
 *  
"""
from flask import Flask

from views.views_admin import admin_views
from views.views_news import news_views
from views.views_user import user_views


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    # 蓝图注册
    app.register_blueprint(user_views)
    app.register_blueprint(news_views)
    app.register_blueprint(admin_views)
    return app
