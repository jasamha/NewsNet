"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-6-2 上午11:40
 *  @ 创建描述    
 *  
"""
import logging


class Log(object):
    """
    自定义的log输出
    """
    _self_sign = "zhang__"

    @classmethod
    def debug(cls, content):
        logging.debug(cls._self_sign + repr(content))

    @classmethod
    def warning(cls, content):
        logging.warning(cls._self_sign + repr(content))

    @classmethod
    def error(cls, what="", content=None):
        if content is None:
            logging.error(cls._self_sign + what + "__")
        else:
            logging.error(cls._self_sign + what + "__" + repr(content))

    @classmethod
    def info(cls, content):
        logging.info(cls._self_sign + repr(content))
