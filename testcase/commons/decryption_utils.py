# -*- coding: utf-8 -*-
# @time    :2022/4/25 23:06
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :decryption_utils.py
import base64
import hashlib
import os

import rsa


class DecryptionUtils:
    # 得到绝对路径
    @staticmethod
    def get_abs_path():
        return os.getcwd().split("pytest")[0] + "pytest"

    # MD5加密
    @staticmethod
    def md5(args):
        args = str(args).encode("utf-8")
        return hashlib.md5(args).hexdigest().upper()

    # BASE64加密
    @staticmethod
    def bs64(args):
        args = str(args).encode("utf-8")
        return base64.b64encode(args).decode().upper()

    # RSA加密(获得公钥和私钥)
    def rsa_get_keys(self):
        public_key, private_key = rsa.newkeys(1024)

        public_pem = public_key.save_pkcs1().decode()
        private_pem = private_key.save_pkcs1().decode()
        # 写入公钥
        with open(self.get_abs_path() + "/public.pem", mode="w+", encoding="utf-8") as file:
            file.write(public_pem)

        # 写入私钥
        with open(self.get_abs_path() + "/private.pem", mode="w+", encoding="utf-8") as file:
            file.write(private_pem)
        print(public_pem, private_pem)

    # 公钥加密
    def public_key_encryption(self, args):
        args = str(args).encode('utf-8')
        # 获得公钥
        with open(self.get_abs_path() + "/public.pem", mode="r", encoding="utf-8") as file:
            public_key = rsa.PublicKey.load_pkcs1(file.read().encode('utf-8'))

        encryption_value = rsa.encrypt(args, public_key)
        # 将公钥加密后的值进行base64位加密
        return base64.b64encode(encryption_value).decode()

    # 私钥解密
    def private_key_decryption(self, args):
        args = str(args).encode('utf-8')
        # 将值进行base64解密
        decryption_value = base64.b64decode(args)
        # 读取私钥
        with open(self.get_abs_path() + "/private.pem", mode="r", encoding="utf-8") as file:
            private_key = rsa.PrivateKey.load_pkcs1(file.read().encode())
        # 根据私钥进行解密后返回
        return rsa.decrypt(decryption_value, private_key).decode()
