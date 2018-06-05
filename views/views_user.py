"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-5-29 上午9:53
 *  @ 创建描述    用户视图
 *  
"""
from flask import Blueprint, session, make_response, jsonify, request

import constants
from models import UserInfo, db
from utils.logutils import Log

user_views = Blueprint("user", __name__, url_prefix="/user")


@user_views.route('/login_out', methods=["POSt"])
def login_out():
    """
    登录退出
    :return:
    """
    if session.get(constants.USER_ID):
        session.pop(constants.USER_ID)
    return jsonify(result=1)


@user_views.route('/login', methods=["POST"])
def login():
    """
    用户登录
    :return:
    """
    dictvalue = request.form
    mobile = dictvalue.get(constants.MOBILE)
    password = dictvalue.get(constants.PASSWORD)
    Log.error("手机值:", mobile)
    Log.error("密码:", password)
    # 验证有效性
    if not all([mobile, password]):
        return jsonify(result=1)
    user = UserInfo.query.filter_by(mobile=mobile).first()
    # 判断mobile是否正确
    if user:
        # 进行密码对比，flask内部提供了密码加密、对比的函数
        if user.check_pwd(password):
            # 状态保持
            session[constants.USER_ID] = user.id
            # 返回成功的结果
            # return jsonify(result=4)
            return jsonify(result=4, avatar=user.avatar, nick_name=user.nick_name)
        else:
            # 密码错误
            return jsonify(result=3)
    else:
        # 如果查询不到数据返回None，表示mobile错误
        return jsonify(result=2)


@user_views.route('/register', methods=['POST'])
def register():
    """
    注册功能
    :return:
    """
    # 接收数据
    dict1 = request.form  # 获取表单对象
    mobile = dict1.get(constants.MOBILE)
    yzm_image = dict1.get(constants.IMAGE_VERIFY)
    yzm_sms = dict1.get(constants.SMS_VERIFY)
    pwd = dict1.get(constants.PASSWORD)
    # 验证数据的有效性
    # 保证所有的数据都被填写,列表中只要有一个值为False,则结果为False
    if not all([mobile, yzm_image, yzm_sms, pwd]):
        return jsonify(result=1)
    # 对比图片验证码
    if yzm_image.upper() != session[constants.IMAGE_VERIFY].upper():
        return jsonify(result=2)
    # 对比短信验证码
    if int(yzm_sms) != session[constants.SMS_VERIFY]:
        return jsonify(result=3)
    # 判断密码的长度
    import re
    if not re.match(r'[a-zA-Z0-9_]{6,20}', pwd):
        return jsonify(result=4)
    # 验证mobile是否存在
    mobile_count = UserInfo.query.filter_by(mobile=mobile).count()
    if mobile_count > 0:
        return jsonify(result=5)
    # 验证通过写入数据库创建对象
    user = UserInfo()
    user.nick_name = mobile
    user.mobile = mobile
    user.password = pwd
    # 提交到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except(BaseException):
        Log.error('用户注册访问数据库失败')
        return jsonify(result=7)
    else:
        Log.error("注册成功")
        return jsonify(result=8)


@user_views.route('/image_verify')
def image_verify():
    """
    图片验证 使用验证码库基于pillow的captcha验证码库
    :return: response
    """
    from utils.captcha.captcha import captcha
    name, verify_code, image = captcha.generate_captcha()
    # verify_code表示随机生成的验证码字符串
    # 将数据进行保存，方便方面对比
    session[constants.IMAGE_VERIFY] = verify_code
    # image表示图片的二进制数据
    response = make_response(image)
    # 默认浏览器将数据作为text/html解析
    # 需要告诉浏览器当前数据的类型为image/png
    response.mimetype = 'image/png'
    return response


@user_views.route('/sms_verify')
def sms_verify():
    """
    短信验证
    :return:
    """
    # 接收数据：手机号，图片验证码
    dict1 = request.args
    mobile = dict1.get(constants.MOBILE)
    yzm = dict1.get('yzm')
    Log.error("手机:", mobile)
    Log.error("yzm:", yzm)
    # 对比图片验证码
    if yzm.upper() != session[constants.IMAGE_VERIFY].upper():
        return jsonify(result=1)

    # 随机生成一个4位的验证码
    import random
    yzm2 = random.randint(1000, 9999)

    # 将短信验证码进行保存，用于验证
    session[constants.SMS_VERIFY] = yzm2

    # 发送短信
    from utils.ytx_sdk.sms_verify import send_template_sms
    send_template_sms(mobile, {yzm2, 5}, 1)
    Log.error("yzm2", yzm2)

    return jsonify(result=2)
