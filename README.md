# NewNet
## 项目文件目录说明
* /logs:存储项目的日志错误等调试信息
* /mirgrations:数据库迁移目录和配置信息
* /static:静态文件iamge,js等
* /templates:html文件
* /test 测试
* /utils:工具包和第三方框架包等
* /views:蓝图包,项目对应模块的视图
* config.py:配置信息
* constans.py:变量昵称
* initapp.py: 工厂函数create_app和相应的配置
* manage.py:项目的启动文件和一些迁移配置
* models.py:模型实体
* learnontime.md:项目需要的依赖包名称

## 2018-05-29
### New 
* 用mvc对项目框架的搭建,用flask蓝图admin,news,user这三个模块分离
* 封装app模块,对flask全局上下文app封装并传入配置参数并注册蓝图
* 配置config文件,对数据库配置和debug配置
## 2018-06-01
### new
* 根据业务分别创建了6个表:用户信息,新闻分类,新闻评论,新闻信息,新闻收藏,用户关注
* 增加了数据库扩展命令迁移命令并创建表
## 2018-06-05
### new
* 完成注册功能包括了图片验证码和短信验证码
* 完成登录
* 登录退出
* 对日志文件的输入和的配置
* 自定义了一个log输入工具

### fix
* 完善了项目的结构
* 修改models下密码判断到用户信息表UserInfo
* app.py文件名更改为--->initapp.py
* newsnet.py文件名更改为--->manage.py


