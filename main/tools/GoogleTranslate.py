import requests
import json
import execjs  # 必须，需要先用pip 安装，用来执行js脚本
from urllib.parse import quote

# 用来判断是否需要打印日志
debug = False


class Py4Js:

    def __init__(self):
        self.ctx = execjs.compile(""" 
            function TL(a) { 
                var k = ""; 
                var b = 406644; 
                var b1 = 3293161072;       
                var jd = "."; 
                var $b = "+-a^+6"; 
                var Zb = "+-3^+b+-f";    
                for (var e = [], f = 0, g = 0; g < a.length; g++) { 
                    var m = a.charCodeAt(g); 
                    128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
                    e[f++] = m >> 18 | 240, 
                    e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
                    e[f++] = m >> 6 & 63 | 128), 
                    e[f++] = m & 63 | 128) 
                } 
                a = b; 
                for (f = 0; f < e.length; f++) a += e[f], 
                a = RL(a, $b); 
                a = RL(a, Zb); 
                a ^= b1 || 0; 
                0 > a && (a = (a & 2147483647) + 2147483648); 
                a %= 1E6; 
                return a.toString() + jd + (a ^ b) 
            };      
            function RL(a, b) { 
                var t = "a"; 
                var Yb = "+"; 
                for (var c = 0; c < b.length - 2; c += 3) { 
                    var d = b.charAt(c + 2), 
                    d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
                    d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
                    a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
                } 
                return a 
            }
        """)

    def get_tk(self, text):
        return self.ctx.call("TL", text)


def build_url(text, tk, tl='zh-CN'):
    """
    需要用转URLEncoder
    :param text:
    :param tk:
    :param tl:
    :return:
    """
    return 'https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=' + tl + '&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&source=btn&ssel=0&tsel=0&kc=0&tk=' \
           + str(tk) + '&q=' + quote(text, encoding='utf-8')


def translate(js, text, tl='zh-CN'):
    """
    tl为要翻译的语言
    de：德语
    ja：日语
    sv：瑞典语
    nl：荷兰语
    ar：阿拉伯语
    ko：韩语
    pt：葡萄牙语
    zh-CN：中文简体
    zh-TW：中文繁体
    """

    header = {
        'authority': 'translate.google.cn',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        # 'cookie': '_ga=GA1.3.110668007.1547438795; _gid=GA1.3.791931751.1548053917; 1P_JAR=2019-1-23-1; NID=156=biJbQQ3j2gPAJVBfdgBjWHjpC5m9vPqwJ6n6gxTvY8n1eyM8LY5tkYDRsYvacEnWNtMh3ux0-lUJr439QFquSoqEIByw7al6n_yrHqhFNnb5fKyIWMewmqoOJ2fyNaZWrCwl7MA8P_qqPDM5uRIm9SAc5ybSGZijsjalN8YDkxQ',
        'cookie': '_ga=GA1.3.110668007.1547438795; _gid=GA1.3.1522575542.1548327032; 1P_JAR=2019-1-24-10; NID=156=ELGmtJHel1YG9Q3RxRI4HTgAc3l1n7Y6PAxGwvecTJDJ2ScgW2p-CXdvh88XFb9dTbYEBkoayWb-2vjJbB-Rhf6auRj-M-2QRUKdZG04lt7ybh8GgffGtepoA4oPN9OO9TeAoWDY0HJHDWCUwCpYzlaQK-gKCh5aVC4HVMeoppI',
        # 'cookie': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'x-client-data': 'CKi1yQEIhrbJAQijtskBCMG2yQEIqZ3KAQioo8oBCL+nygEI7KfKAQjiqMoBGPmlygE='
    }
    url = build_url(text, js.get_tk(text), tl)
    res = []
    try:
        r = requests.get(url, headers=header)
        result = json.loads(r.text)
        r.encoding = "UTF-8"
        if debug:
            print(r.url)
            print(r.headers)
            print(r.request.headers)
            print(result)

        res = result[0]
        if res is None:
            if result[7] is not None:
                # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
                try:
                    correct_text = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
                    if debug:
                        print(correct_text)
                    correct_url = build_url(correct_text, js.get_tk(correct_text), tl)
                    correct_response = requests.get(correct_url)
                    correct_result = json.loads(correct_response.text)
                    res = correct_result[0]
                except Exception as e:
                    if debug:
                        print(e)
                    res = []

    except Exception as e:
        res = []
        if debug:
            print(url)
            print("翻译" + text + "失败")
            print("错误信息:")
            print(e)
    finally:
        return res


def get_translate(word, tl='zh-CN'):
    js = Py4Js()
    translate_result = translate(js, word, tl)

    if debug:
        print("word== %s, tl== %s" % (word, tl))
        print(translate_result)
    return translate_result


if __name__ == '__main__':
    debug = True
    translate_text = '3.Hear voice prompt \"start configuration mode\". click \"reset successfully\" button\n'
    results = get_translate(translate_text, 'zh-CN')
    translate_result = ""

    if "." in translate_text or "?" in translate_text:
        for result in results:
            if result[0]:
                translate_result += result[0]
    else:
        result_translate = results[0]

    if debug:
        print("translate_result:" + translate_result)
