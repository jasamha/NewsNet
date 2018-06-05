"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-29 上午9:24
 *  @ 创建描述  启动模块
 *  
"""
from flask import render_template
from flask_script import Manager, Command

from initapp import create_app
from config import DevelopConfig
from flask_migrate import Migrate, MigrateCommand

from models import db
from utils.logutils import Log

main_app = create_app(config=DevelopConfig)
manager_start = Manager(main_app)
db.init_app(main_app)
# 添加迁移的命令
# 初始化迁移对象，参数为app对象，db对象
Migrate(main_app, db)
manager_start.add_command('db', MigrateCommand)


@main_app.errorhandler(404)
def page_not_found(e):
    Log.error("没有捕捉到啊")
    return render_template("news/404.html"), 404


class Show(Command):
    def run(self):
        print('这是我们自定义的命令')


manager_start.add_command('show', Show())
if __name__ == '__main__':
    print("zhang_____" + main_app.config.get("ZSH"))
    manager_start.run()  # 主程序启动
