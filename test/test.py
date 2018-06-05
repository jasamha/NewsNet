"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-6-2 下午5:25
 *  @ 创建描述    
 *  
"""
from utils.logutils import Log

str1 = "a68c"
print(str1.upper())
str2 = None
dict1 = dict(a=1, b=2)
dict1.pop("b")
if dict1.get("a"):
    dict1.pop("a")
print(dict1)
