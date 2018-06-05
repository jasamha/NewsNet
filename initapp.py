"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-29 上午9:21
 *  @ 创建描述   创建工厂函数并且配置好文件参数
 *  
"""
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_wtf import CSRFProtect

from views.views_admin import admin_views
from views.views_news import news_views
from views.views_user import user_views


def config_logger(app, config):
    """
    配置日志输入
    @param app:app对象
    @param config: 配置文件
    @type app:flask_app
    @return: 无
    """

    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = \
        RotatingFileHandler(config.BASE_DIR + "/logs/newsnet.log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
    app.print_log = logging
    # current_app.print_log.error('错误信息')


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    # 蓝图注册
    app.register_blueprint(user_views)
    app.register_blueprint(news_views)
    app.register_blueprint(admin_views)
    # app.register_blueprint(errors_views)
    config_logger(app, config)
    # 进行csrf防御
    CSRFProtect(app)
    return app
