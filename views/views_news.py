"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-29 上午9:53
 *  @ 创建描述    新闻主视图
 *  
"""
from flask import Blueprint, render_template, current_app

from utils.logutils import Log

news_views = Blueprint("news", __name__)


@news_views.route('/test')
def test():
    current_app.logger.debug('A value for debugging')
    return "helloword!"


@news_views.route('/')
def index():
    return render_template('news/index.html')
