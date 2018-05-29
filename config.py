"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-29 上午9:17
 *  @ 创建描述   创建配置文件
 *  
"""


class ReleaseConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://jasamha:1@localhost:3306/newsnet'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopConfig(ReleaseConfig):  # 继承ReleaseConfig
    DEBUG = True
    ZSH = "66666"
