import hashlib

# 将string url转换成md5格式
def strURL_to_md5(url):
    if isinstance(url, str):  #python3中，str格式即unicode格式
        url = url.encode(encoding='utf8')
    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()

# if __name__ == '__main__':
#     print(strURL_to_md5('http://www.jobbole.com/'.encode(encoding='utf8')))

# _name__ 是当前模块名，当模块被直接运行时模块名为 __main__
# 这句话的意思就是，当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
