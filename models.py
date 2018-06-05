"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-30 上午8:57
 *  @ 创建描述    
 *  
"""
import pymysql

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

pymysql.install_as_MySQLdb()

db = SQLAlchemy()


class BaseModel(object):
    """
    代码重用基类
    """
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Boolean, default=False)


class NewsCategory(db.Model, BaseModel):
    """
    新闻分类表
    """
    __tablename__ = 'news_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    # 关系属性：不会在表中生成字段
    # lazy='dynamic'惰性加载category.news
    # category=NewsCategory.query.get(1)
    # 当使用lazy='dynamic'时不会查询分类的新闻信息
    # 这样设置的好处：可能本次只是使用分类对象，不想使用新闻对象，则可以减少数据库的查询量
    news = db.relationship('NewsInfo', backref='category', lazy='dynamic')


class NewsInfo(db.Model, BaseModel):
    """
    新闻信息类
    """
    __tablename__ = 'news_info'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('news_category.id'))
    pic = db.Column(db.String(50))
    title = db.Column(db.String(30))
    summary = db.Column(db.String(200))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    click_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    reason = db.Column(db.String(100), default='')
    comments = db.relationship('NewsComment', backref='news', lazy='dynamic', order_by='NewsComment.id.desc()')


"""
 用户关注用户关系
 """
tb_user_follow = db.Table(

    'tb_user_follow',
    db.Column('origin_user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True),
    db.Column('follow_user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True)
)
"""
    用户收藏关系表
    """
tb_news_collect = db.Table(

    'tb_news_collect',
    db.Column('user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True),
    db.Column('news_id', db.Integer, db.ForeignKey('news_info.id'), primary_key=True)
)


class UserInfo(db.Model, BaseModel):
    """
    个人用户信息表
    """
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(50), default='user_pic.png')
    nick_name = db.Column(db.String(20))
    signature = db.Column(db.String(200))
    public_count = db.Column(db.Integer, default=0)
    follow_count = db.Column(db.Integer, default=0)
    mobile = db.Column(db.String(11))
    password_hash = db.Column(db.String(200))
    gender = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    # 用户对新闻为1：多，所以将新闻关联属性定义在User类中
    news = db.relationship('NewsInfo', backref='user', lazy='dynamic')
    # 用户对评论为1：多，所以将评论关联属性定义在User类中
    comments = db.relationship('NewsComment', backref='user', lazy='dynamic')
    # 用户对收藏新闻为多：多，此时关系属性可以定义在任意类中，当前写在了User类中
    news_collect = db.relationship(
        'NewsInfo',
        # 多对多时，指定关系表，因为外键存储在这个关系表中
        secondary=tb_news_collect,
        lazy='dynamic'
        # 此处没有定义backref，作用是根据新闻找用户，因为不需要使用这个功能，所以可以不定义
    )
    # 用户关注用户为自关联多对多，关系属性只能定义在User类中
    # 使用user.follow_user可以获得当前user用户关注的用户列表
    # select * from users inner join tb_user_follow on user.id=origin_user_id
    follow_user = db.relationship(
        'UserInfo',
        # 多对多，所以指定关系表
        secondary=tb_user_follow,
        lazy='dynamic',
        # user.follow_by_user可以获得当前user用户的粉丝用户列表
        backref=db.backref('follow_by_user', lazy='dynamic'),
        # 在使用user.follow_user时，user.id与关系表中哪个字段判等
        primaryjoin=id == tb_user_follow.c.origin_user_id,
        # 在使用user.follow_by_user时，user.id与关系表中的哪个字段判等
        secondaryjoin=id == tb_user_follow.c.follow_user_id
    )

    @property
    def password(self):
        pass

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.password_hash, pwd)


class NewsComment(db.Model, BaseModel):
    """用户评论"""
    __tablename__ = 'news_comment'
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news_info.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    like_count = db.Column(db.Integer, default=0)
    comment_id = db.Column(db.Integer, db.ForeignKey('news_comment.id'))
    msg = db.Column(db.String(200))
    comments = db.relationship('NewsComment', lazy='dynamic')
