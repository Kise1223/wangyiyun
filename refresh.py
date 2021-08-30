import json,base64,random,requests,re,os
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from  binascii import hexlify
from configparser import ConfigParser
import os
current_path = os.getcwd()
path_config = current_path + '\\init.config'
def add_to_16(text):
    # 补全成16的倍数
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

def make_random():
    str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    random_str = ''
    for i in range(16) :
        index = random.randint(0, len(str) - 1)
        random_str += str[index]
    return random_str


def AESEncrypt(clear_text, key):
    """
    AES加密, 对应函数b
    :param clear_text: 需要加密的数据
    :return:
    """
    # 数据填充
    clear_text = pad(data_to_pad=clear_text.encode(), block_size=AES.block_size)
    key = key.encode()
    iv = '0102030405060708'
    iv = iv.encode()
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv = iv)
    cipher_text = aes.encrypt(plaintext=clear_text)
    # 字节串转为字符串
    cipher_texts = base64.b64encode(cipher_text).decode()
    return cipher_texts
def make_params_encSecKey(text):
    # song_name = input('要下载歌曲的名字:')
    text = json.dumps(text)
    key = '0CoJUm6Qyw8W8jud'
    # key = key.encode('utf-8')
    frist_aes =AESEncrypt(text,key)
    random_str = make_random()
    encSecKey = make_encSecKey(random_str)
    # print(frist_aes)
    fan_key = frist_aes.encode()
    params = AESEncrypt(frist_aes,random_str)
    # print(params)
    data = {
        'params': params,
        'encSecKey': encSecKey
    }
    return data
    # fanl_text = str(frist_aes,encoding='utf-8')
    # parmas = aes_encrypt(fanl_text,random_str)

def make_encSecKey(text):
        text = text[::-1]
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        pub_key = '010001'
        rs = pow(int(hexlify(text.encode('utf-8')), 16), int(pub_key, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

def print_id_list(data):
    # data = make_params_encSecKey()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    id_url = 'https://music.163.com/weapi/v3/playlist/detail?csrf_token='
    response = requests.post(id_url,data,headers).text
    # print(response.text)
    # names = re.findall(r'"name":"(.*?)"',response)
    # ids = re.findall(r'","id":(.*?),"pst"',response)
    # i = 0
    # for id in ids :
    #     # a = int(id)
    #     # if a>10000 and a<100000 :
    #     print(i,id)
    #     i = i+1
    # print(i)
    ids_list = json.loads(response)['playlist']['trackIds']
    count = 0
    info_list = []
    for id_info in ids_list:
        song_id = id_info['id']
        info_list.append(song_id)
        count += 1
    return info_list

if __name__ == '__main__':
    config = ConfigParser()
    config.read(path_config, encoding='UTF-8-sig')
    while 1:
        songid = input("歌单id\n")
        text = {"id": songid, "n": "1000","csrf_token": ""}
        data = make_params_encSecKey(text)
        # print(text)
        ids_list = print_id_list(data)
        try:
            print(",".join(repr(i) for i in ids_list))
        except:
            print("歌单可能没歌 或者填错歌单id")
            print(ids_list)
        finally:
            config.set("setting", "id", (",".join(repr(i) for i in ids_list)))
            with open("init.config", "w+") as f:
                config.write(f)
            f.close()
            input('Enter again ')


    # while True:
    #     input_index = eval(input("请输入要下载歌曲的序号(按666退出): "))
    #     if input_index == 666:
    #         break
    #     download_info = ids_list[input_index]
    #     song_d = {
    #         "ids": str([download_info[0]]),
    #         "level": " ",
    #         "encodeType": "aac",
    #         "csrf_token": ""
    #     }
    #     print(song_d)
    #     把song_d用AES和RSA加密以后变成params和en写进请求
    #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    #                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    #     data = make_params_encSecKey(song_d)
    #     print(data)
    #     song_url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    #     song_response = requests.post(song_url,data,headers).text
    #     print(song_response)
    #     inti_download_url = re.findall(r'"url":"(.*?)","', song_response,re.S)
    #     print(inti_download_url[0])
    #     download_url = re.findall(r'[(.*?)]', inti_download_url, re.S)
    #     print(download_url)
    #     download_url = 1+inti_download_url
    #     print(download_url[0])
    #     download_location = r'D:'
    #     os.mkdir('d:\网易云音乐下载')
    #     download_song = requests.get(inti_download_url[0],headers)
    #     name=str(song_name)+'.mp3'
    #     with open(name, 'wb') as f:
    #         f.write(download_song.content)
    #     print("下载成功")
