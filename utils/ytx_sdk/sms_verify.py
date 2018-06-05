"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-6-2 上午10:53
 *  @ 创建描述    
 *  
"""
from .CCPRestSDK import REST

# import ConfigParser

# 主帐号
accountSid = "8a216da863b5b9c20163be4f724f03cd"

# 主帐号Token
accountToken = 'fd6ff50fcc9f4efa9db8de7db2ad4f09'

# 应用Id
appId = '8a216da863b5b9c20163be4f72a703d3'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

def send_template_sms(to, datas, temp_id):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, temp_id)
    return result.get('statusCode')
