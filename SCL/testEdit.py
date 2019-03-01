from ctypes import *
import os

# 参考 https://docs.python.org/3/library/ctypes.html
# Q&A1：注意返回 [Error 193] 可能是因为电脑是64位的而 .dll是32位的 所以造成这个错误，将Python换成32 位的即可
# Q&A1参考:https://blog.csdn.net/a19990412/article/details/79375272

def test():
    # 搜索已配置控制器
    # 1.开始查找
    libs.SCL_SeekStart.argtypes = [c_uint16, c_char_p, c_uint16, c_char_p, c_bool]
    isSeekStart = c_bool(libs.SCL_SeekStart(2, b"", 28123, b"255.255.255.0", True))
    # 2.获取控制器返回的Ip地址
    libs.SCL_SeekGetAItem.argtypes = [c_char_p, c_char_p]
    ip = create_string_buffer(16)
    name = create_string_buffer(16)
    isSeekGetAItem = c_bool(libs.SCL_SeekGetAItem(ip, name))
    print('isSeekStart:{}'.format(isSeekStart))
    print('isSeekGetAItem:{}'.format(isSeekGetAItem))
    print('\tip:{}\n\tname:{}'.format(ip.raw, name.raw))
    # 3.退出查找
    isSeekClose = c_bool(libs.SCL_SeekClose())
    print('isSeekClose:{}'.format(isSeekClose))


libs = windll.LoadLibrary('SCL_API_stdcall123.dll')
test()
os.system('pause')
