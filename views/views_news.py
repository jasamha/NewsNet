"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-29 上午9:53
 *  @ 创建描述    新闻主视图
 *  
"""
from flask import Blueprint

news_views = Blueprint("news", __name__)


@news_views.route('/test')
def test():
    return "helloword!"
