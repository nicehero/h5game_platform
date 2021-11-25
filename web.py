#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeWapPayModel import AlipayTradeWapPayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeWapPayRequest import AlipayTradeWapPayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse
import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.options
import tornado.websocket
import tornado.autoreload
import tornado.httpclient
import tornado.auth
from tornado.httputil import url_concat
#import urllib2
import base64
import os
import hashlib
import time
import json
import struct

import datetime
import logging
import urllib
import urllib.request
import uuid
import re
import pickle

# 写入pickle
def pickle_write(file_path, data):
	f = open("./data/" + file_path, 'wb')
	pickle.dump(data, f)
	f.close()

# 读取pickle
def pickle_read(file_path):
	try:
		f = open("./data/" + file_path, 'rb')
		data = pickle.load(f)
		f.close()
		return data
	except:
		return None
	

#url1 = "http://127.0.0.1:8810/"
games = {
"tinyHeart":{"name":"TinyHeart","img":"th.png","cost":0.1},
"linkGame":{"name":"连连看","img":"IMG20190118_173659.png","cost":0.0},
"2048":{"name":"2048","img":"2048x.jpg","cost":0.0},
"Gobang":{"name":"五子棋","img":"Gobangx.jpg","cost":0.0},
"RetroSnaker":{"name":"贪吃蛇","img":"snake.jpg","cost":0.0},
"Tetris":{"name":"俄罗斯方块","img":"Tetrisx.jpg","cost":0.0},
"tinyHeartFree":{"name":"TinyHeart免费版","img":"th.png","cost":0.0},
}#game list
plogin = '''
<html>
<style>
center
{
	margin-top:100px;
	margin-bottom:100px;
	margin-right:50px;
	margin-left:50px;
}
</style>
<body>
<script src="static/sha256.min.js"></script>
<script>
	function getParam(par){
		var local_url = document.location.href; 
		var get = local_url.indexOf(par +"=");
		if(get == -1){
			return "";   
		}   
		var get_par = local_url.slice(par.length + get + 1);	
		var nextPar = get_par.indexOf("&");
		if(nextPar != -1){
			get_par = get_par.slice(0, nextPar);
		}
		return decodeURIComponent(get_par);
	}
	function login(){
		let PARAMS = {}
		PARAMS.username = document.getElementById('username').value;
		PARAMS.password = sha256(document.getElementById('password').value);
		PARAMS.next = getParam('next').replace('/','')
		//document.cookie = "username=" + username
		//document.cookie = "pass=" + password
		//window.location.href='/'
		var temp = document.createElement("form");
		temp.action = "/login";
		temp.method = "post";
		temp.style.display = "none";
		for (var x in PARAMS) {
			var opt = document.createElement("textarea");
			opt.name = x;
			opt.value = PARAMS[x];
			temp.appendChild(opt);
		}
		document.body.appendChild(temp);
		let r = temp.submit();
		console.log(r);
		return temp;
	}
</script>
<center>
	<div>用户名: <input type="text" name="username" id="username"></div>
	<div>密码: <input type="password" name="password" id="password"></div>
	<div><input type='button' value='登陆' onclick='login()'></input>
	<a id="hrefSignup">注册</a></div>
	<div><a href="./">返回主页</a></div>
</center>
<script>
let next = getParam('next').replace('/','')
if (next == ""){
	document.getElementById("hrefSignup").setAttribute("href","./signup");
}
else {
	document.getElementById("hrefSignup").setAttribute("href","./signup?next=" + next);
}
message = "%s";
if (message != ""){
	alert(message);
}

</script>
</body></html>
'''
psignup = '''
<html>
<style>
center
{
	margin-top:100px;
	margin-bottom:100px;
	margin-right:50px;
	margin-left:100px;
}
</style>
<body>
<script src="static/sha256.min.js"></script>
<script>
	function getParam(par){
		var local_url = document.location.href; 
		var get = local_url.indexOf(par +"=");
		if(get == -1){
			return "";   
		}   
		var get_par = local_url.slice(par.length + get + 1);	
		var nextPar = get_par.indexOf("&");
		if(nextPar != -1){
			get_par = get_par.slice(0, nextPar);
		}
		return decodeURIComponent(get_par);
	}
	function signup(){
		let PARAMS = {}
		PARAMS.username = document.getElementById('username').value;
		PARAMS.password = sha256(document.getElementById('password').value);
		let passwordAgain = sha256(document.getElementById('passwordAgain').value);
		if (PARAMS.password != passwordAgain){
			alert("两次密码输入不同!");
			return;
		}
		PARAMS.next = getParam('next').replace('/','')
		//document.cookie = "username=" + username
		//document.cookie = "pass=" + password
		//window.location.href='/'
		var temp = document.createElement("form");
		temp.action = "/signup";
		temp.method = "post";
		temp.style.display = "none";
		for (var x in PARAMS) {
			var opt = document.createElement("textarea");
			opt.name = x;
			opt.value = PARAMS[x];
			temp.appendChild(opt);
		}
		document.body.appendChild(temp);
		let r = temp.submit();
		console.log(r);
		return temp;
	}
</script>
<center><div align="left">
	<div><div>用户名:</div> <input type="text" name="username" id="username">用户名需要6到12个字母或数字或下划线_,只能字母开头</div>
	<div><div>密码:</div> <input type="password" name="password" id="password">密码需要8到12个字母或数字加特殊符号</div>
	<div><div>再输入一次密码:</div> <input type="password" name="password" id="passwordAgain"></div>
	<div><input type='button' value='注册' onclick='signup()'></input></div>
	<div><a href="./">返回主页</a></div>
</div></center>
<script>
message = "%s";
if (message != ""){
	alert(message);
}
</script>
</body></html>
'''
NUM_LETTER = re.compile("^(?!\d+$)[\da-zA-Z_]+$")     #数字和字母组合，不允许纯数字
FIRST_LETTER = re.compile("^[a-zA-Z]")           #只能以字母开头

def account_name_format(Name):
	if NUM_LETTER.search(Name):
		if FIRST_LETTER.search(Name):
			return True
	return False

SESSION = {}
USERS = {}
class Session:
	def __init__(self, handler):
		self.handler = handler
	@staticmethod
	def _random_str():
		'''用随机数来作为session_id'''
		return str(uuid.uuid4())
	def _get_cookie_sid(self):
		'''获取cookie中的session_id'''
		cookie_sid = self.handler.get_secure_cookie("__session", None)
		return str(cookie_sid, encoding="utf-8") if cookie_sid else None
	def __setitem__(self, key, value):
		cookie_sid = self._get_cookie_sid()
		if not cookie_sid:
			cookie_sid = self._random_str()
		self.handler.set_secure_cookie("__session", cookie_sid,samesite="Lax")
		SESSION.setdefault(cookie_sid, {"username" : ""}).__setitem__(key, value)
	def __getitem__(self, key):
		cookie_sid = self._get_cookie_sid()
		content = SESSION.get(cookie_sid, None)
		return content.get(key, None) if content else None
	def __delitem__(self, key):
		cookie_sid = self._get_cookie_sid()
		if not cookie_sid or not SESSION.get(cookie_sid):
			raise KeyError(key)
		del SESSION[cookie_sid][key]

class MyHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		current_user = self.session["username"]
		if current_user != "":
			return current_user
		return None
	def initialize(self):
		self.session = Session(self)

gf = open("index.html",'rb')
mainIndex = gf.read().decode()
gf.close()
gt = '''<div id = "%s" name="game"><a href="./%s"><div><img src="./static/%s"/></div><div><font size="3">%s</font></div></a>
<div><font size="5" color="#FF0000">¥%s</font></div></div>
'''
gt1 = '''<div class="s-top-left">欢迎光临!</div>
<div class="s-top-right">
<div class="noLine"><a href="login">登陆</a></div>
<div class="noLine"><a href="signup">注册</a></div>
</div>
'''
gt2 = '''<div class="s-top-left">你好:%s!</div>
<div class="s-top-right">
<a href="./?logout=1">退出</a>
</div>
'''
class MainHandler(MyHandler):
	def get(self):
		isLogout = self.get_argument('logout',"")
		if isLogout != "":
			self.session["username"] = ""
		global mainIndex
		global gt
		global gt1
		user = self.current_user
		s = ""
		u = None
		if user in USERS:
			u = USERS[user]
		print("--------------------")
		print(u)
		print("--------------------")
		for i in games.keys():
			scost = "免费";
			if games[i]["cost"] > 0.009:
				scost = str(games[i]["cost"])
				try:
					if i in u["had"]:
						scost = "已购"
				except:
					pass
			s = s + (gt % (games[i]["name"],i,games[i]["img"],games[i]["name"],scost))
		if user != None:
			self.write(mainIndex % (gt2%user,s))
		else:
			self.write(mainIndex % (gt1,s))
class LoginHandler(MyHandler):
	def get(self):
		self.write(plogin % "")
	def post(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		next = self.get_argument("next")
		if len(username) < 6 or len(username) > 12 or not account_name_format(username):
			self.write(plogin % "用户名格式错误")
			return
		if not username in USERS:
			u = pickle_read(username)
			if not u:
				self.write(plogin % "用户名不存在或密码错误")
				return
			USERS[username] = u
		if USERS[username]["password"] != password:
			self.write(plogin % "用户名不存在或密码错误")
			return
		self.session["username"] = username
		self.redirect("/" + next)
class SignupHandler(MyHandler):
	def get(self):
		self.write(psignup % "")
	def post(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		if len(username) < 6 or len(username) > 12 or not account_name_format(username):
			self.write(psignup % "用户名格式错误")
			return
		if len(password) < 8:
			self.write(psignup % "密码格式错误")
			return
		if username in USERS:
			self.write(psignup % "用户名已存在")
			return
		u = pickle_read(username)
		if u != None:
			self.write(psignup % "用户名已存在")
			return
		USERS[username] = {"username":username,"password":password}
		pickle_write(username,USERS[username])
		next = self.get_argument("next")
		self.session["username"] = username
		self.redirect("/" + next)

#logging.basicConfig(level=logging.INFO,filename='web.log')
logger = logging.getLogger('')

"""
设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
"""
alipay_client_config = AlipayClientConfig()
alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
alipay_client_config.app_id = '2021000118654178'
alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAlUteUgP7uN0FbS7mTCJHtSzshznBOfVV05EdIfCrKTKAYPcwYgk+uf1VD6HH0FpbIKgMIn5n7kRPwbbRDv5CegjynZXU9TBfluazHF7kIE9rrTMknK1b46XRpcsK1kflc+QDCRwiR25ObkLZuvd1+4SaW7/3gn/f9PTgrfdg0vj2DzXEzMfHWst0uCzy8JXOvadVSlfOdDDiXZvLsv95Ak/0oTb8/RYKYv8IQZnSCuktjYh95kVQFvLNjmCW2cMixncBkmyUS8r5Rh+fN0KhsR0yg3RD0H8U/PrLkEWSIdZwcM0YqKzrbHeaP6EKKbcT7EpiTAxlkIsNNLAiowX0zwIDAQABAoIBABqZHujFxOcemYTmQil2QghJRKqi44YL64qR4/rUAeqJEM41u+z7cK16MNlkHVFFh869ocvTcXjFut/sTjq5meZcCb2BoDs+rwkXePmo/kOzYp+s6OzxBdn9BOjgz8F1da+8A75vwLuxL0/9oQTqaZ6x9T47aUFavu/JYO4dkKaFZQdm25LxpLTV3URG3j+lca2H0d+d9tI6+PUiWReEGbYUw+AwK7HtgMCRvj+QgkVkaiks4TTHaPxelC9YShYszuusUI3q5uM2+1KqUPycCbhH3QTKwJFFcAJhxUTwr7Ucg/m0zgYW5QQAjU/y0bYPJUZSN0FAEsT8KAIcvVhJEkECgYEA9IzzrF6Ih3sI5Y0JP64HokDNBly1uJSxL5CbfGq+S7/ArZfkVXajJMmipu1Nxxa+9wcORpFFD+OzSX7/Q31qK4UJLPYv2mmCnXcdAAliFHoWhdvRc1DeoOnL9hiQ1dkcyc/QHB9KXGL9AKDwFG6UyxRoNaISMknFxvXckeyO/fcCgYEAnEi6iB9gfvbxyL3F5Ge/WFxe1obZz1thonxrQaXOQt/XaahTAfyk0+z5INcWPd3Uc3FcyLRRmU87/uMrGEijk1pwzq90qW/3h7X6vH63GwVaOaoCSpQEZ6AUcYQ0U533R/NSlr1fKHNjPiLxHu5rng6IVXTuzHekzZs/Rjtd6ekCgYAQ7vmog9s8Vl6lVoC/chOBPq9zs1O59kHWo1LA6LtIj3yOCKh86nwdfgDPQjtSf9a1UD3C0ShRE1lEy5BtYe/KF6os/NcPbqLmuGq/p+asuE968V+tdnoT9lxzK/xLcn810jf82oXRo+EU/A/jukx/S2hz3kcYSFdzkW62hATavQKBgB5wG8Q/ODACMH0EWPJvMlknRGFLykgUaCOZT9ptTIrBxdaSLfiJGCEeWjcHLRHHjoUdYxDD7dCKGgk+fToxi4o7ZxUaHwKRCAiqbLchhtAAbt4kOmYEBgeYqeKh+P8AGRUuUruBDnN2ZbHIZGW90b/q3KqoJ4ozEynoPp6TGWthAoGANY5vQwfowDiwX+QNQfQ+LdzHNVeBgVI35iLaK1byUYGhOfGdvydM7tLkjvK6NYHi0VQznXhWvefXYkYj3qlusFbjqwHfk9tm24xLnXonNdKHnvxknYrMwIjYtkB+nzdBu8+/a51/d/MSJrSANlCezNnD+B0I3CV9i8o7NcbfIL0='
alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApnBWmglUkd3OtdCSKWrXwUInvfUgeNT+wAgHSzV077PrIb/GFU1Ib/HnABGfcc4kZgf2D0gXsIah8mjxSnKer73Ckqyx8XX/S0zJGnDbWGNPR6C4KLybMDNvzfzkQpxXWSAlYKePbq39k0xLs+cCOUZF/8+d3AD4lw7/Z6miYJHgKOEmB+euKhLCcBIWtxbAIlxwMlu0uWIYanxmW1dpC2DoN55BqKfrUxsIRpaqpXjFG/WSYmC3XCI+xV3jk931JQQfnamgzWRpdoFIDx4fZqhycY/QdalKtmqpuNB5yzRtiRVei1dTlMc+ivM19jFrncFJTAkJaREN74vfq80cXwIDAQAB'
alipay_client_config.sign_type = 'RSA2'

"""
得到客户端对象。
注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
logger参数用于打印日志，不传则不打印，建议传递。
"""
client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
"""
g_model = AlipayTradeQueryModel()
g_model.out_trade_no = "tinyHeart_yuyinda"
g_req = AlipayTradeQueryRequest(biz_model=g_model)
g_o = client.execute(g_req)
print("--------------------------------")
print(g_o)
print("--------------------------------")
g_model = AlipayTradeQueryModel()
g_model.out_trade_no = "tinyHeart_test00001"
g_req = AlipayTradeQueryRequest(biz_model=g_model)
g_o = client.execute(g_req)
print("--------------------------------")
print(g_o)
print("--------------------------------")
"""
class AnyHandler(MyHandler):
	def checkAlipay(self,subject,user,name,u):
		model = AlipayTradeQueryModel()
		model.out_trade_no = subject
		req = AlipayTradeQueryRequest(biz_model=model)
		o = client.execute(req)
		print("--------------------------------")
		print(o)
		print("--------------------------------")
		jo = json.loads(o)
		if jo["msg"] == "Success" and float(jo["total_amount"]) + 0.01 >= games[name]["cost"]:
			try:
				t = "" in u["had"]
			except:
				u["had"] = []
			u["had"].append(name)
			USERS[name] = u
			pickle_write(user,u)
			return True
		payUrl = str(games[name]["cost"])+"&product="+name+"&user="+subject
		self.redirect('AliPay?amount=' + payUrl)
		return False
	def isBuy(self,name,user,u):
		subject = name + "_" + user
		isFind = True
		try:
			if not name in u["had"]:
				isFind = False
		except:
			isFind = False
		if isFind == True:
			return True
		return self.checkAlipay(subject,user,name,u)
	@tornado.web.authenticated 
	def get(self):
		user = self.current_user
		name = self.request.path[1:]
		if not name in games:
			self.write("no game")
			return
		if not user:
			self.redirect('/login?redirect=' + name)
			return
		u = None
		if user in USERS:
			u = USERS[user]
		if games[name]["cost"] > 0.009:
			if not self.isBuy(name,user,u):
				return
		f = open("./static/" + name + "/index.html", 'rb')
		self.write(f.read())
		f.close()


class AliPay(MyHandler):
	def get(self):
		#model = AlipayTradeAppPayModel()
		#model = AlipayTradePayModel()
		model = AlipayTradeWapPayModel()
		#model = AlipayTradePagePayModel()
		model.total_amount = self.get_query_argument('amount', '1')
		#model.product_code = 'FAST_INSTANT_TRADE_PAY'
		model.product_code = 'QUICK_WAP_PAY'
		model.subject = self.get_query_argument('user', '0_0')
		#model.out_trade_no = str(int(time.time())) + model.subject
		model.out_trade_no = model.subject
		model.seller_id = "gqfmha3170@sandbox.com"
		#model.seller_id = "9youzl@mail.m818.com"
		url0 = "http://" + self.request.host + "/"
		model.quit_url = url0
		#model.timeout_express = '10m'
		#request = AlipayTradeAppPayRequest(biz_model=model)
		#request.notify_url = url0 + 'AliPayOk'
		#response = client.sdk_execute(request)
		#logging.info("alipay.trade.app.pay response:" + response)
		#self.write(response)
		#pay_request = AlipayTradePagePayRequest(biz_model=model)
		pay_request = AlipayTradeWapPayRequest(biz_model=model)
		#pay_request = AlipayTradePayRequest(biz_model=model)
		#pay_request.notify_url = url0 + 'AliPayOk'   # 支付后回调地址
		pay_request.return_url = url0 + self.get_query_argument('product', '')
		#response = client.sdk_execute(pay_request)
		#self.write(response)
		pay_url = client.page_execute(pay_request, http_method='GET')
		self.redirect(pay_url)

def check_pay( params):  # 定义检查支付结果的函数
	from alipay.aop.api.util.SignatureUtils import verify_with_rsa
	sign = params.pop('sign', None)  # 取出签名
	print('public_key:')
	print(public_key)
	print('sign:')
	print(sign)
	params.pop('sign_type')  # 取出签名类型
	params = sorted(params.items(), key=lambda e: e[0], reverse=False)  # 取出字典元素按key的字母升序排序形成列表
	message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()  # 将列表转为二进制参数字符串
	print('message:')
	print(message)
	# with open(settings.ALIPAY_PUBLIC_KEY_PATH, 'rb') as public_key: # 打开公钥文件
	try:
		status = verify_with_rsa(public_key, message,sign)  # 验证签名并获取结果
		return status  # 返回验证结果
	except Exception as e:
		# 访问异常的错误编号和详细信息
		print(e.args)
		print(str(e))
		print(repr(e))
		return False

class AliPayOk(tornado.web.RequestHandler):
	def post(self):
		params = self.request.arguments
		logging.info("AliPayOk post")
		logging.info(params)
		params2 = {}
		for key in params.keys():
			params2[key] = params[key][0].decode()
		params = params2
		logging.info("------------------------------------------------------")
		logging.info(params)
		if params["trade_status"] != "TRADE_SUCCESS" and params["trade_status"] != "TRADE_FINISHED":
			logging.info("not success")
			return
		if check_pay(params):
			logging.info("check ok")
			m = hashlib.md5()
			orderID = "alipay_" + params["trade_no"]
			data = params["subject"]
			ii = data.find("_")
			user = data[ii + 1:]
			name = data[:ii]
			amount = str(params["total_amount"])
			if not name in games:
				logging.info("AlipayOK game not exist:" + name)
				self.write("not success")
				return
			if float(amount) + 0.01 < games[name]["cost"]:
				logging.info("AlipayOK amount error:" + name + "," + str(amount))
				self.write("success")
				return
			u = pickle_read(user)
			if not u:
				logging.info("AlipayOK user not exist:" + user)
				self.write("not success")
				return
			try:
				t = "" in u["had"]
			except:
				u["had"] = []
			u["had"].append(name)
			USERS[name] = u
			pickle_write(user,u)
			self.write("success")
		else:
			logging.info("check error")
			self.write("failed")
	def get(self):
		params = self.request.arguments
		logging.info("AliPayOk get")
		logging.info(params)
		params2 = {}
		for key in params.keys():
			params2[key] = params[key][0].decode()
		params = params2
		logging.info("------------------------------------------------------")
		logging.info(params)
		if params["trade_status"] != "TRADE_SUCCESS" and params["trade_status"] != "TRADE_FINISHED":
			logging.info("not success")
			return
		if check_pay(params):
			logging.info("check ok")
			m = hashlib.md5()
			orderID = "alipay_" + params["trade_no"]
			data = params["subject"]
			ii = data.find("_")
			user = data[ii + 1:]
			name = data[:ii]
			amount = str(params["total_amount"])
			if not name in games:
				logging.info("AlipayOK game not exist:" + name)
				self.write("not success")
				return
			if float(amount) + 0.01 < games[name]["cost"]:
				logging.info("AlipayOK amount error:" + name + "," + str(amount))
				self.write("success")
				return
			u = pickle_read(user)
			if not u:
				logging.info("AlipayOK user not exist:" + user)
				self.write("not success")
				return
			try:
				t = "" in u["had"]
			except:
				u["had"] = []
			u["had"].append(name)
			USERS[name] = u
			pickle_write(user,u)
			self.write("success")
		else:
			logging.info("check error")
			self.write("failed")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/login", LoginHandler),
			(r"/signup", SignupHandler),
			(r"/AliPay", AliPay),
			(r"/AliPayOk", AliPayOk),
		]
		for i in games.keys():
			handlers.append((r"/" + i,AnyHandler))
		settings = dict(
			cookie_secret="61oETzKXQAGaYdkL2gEmGeJJFuYh8EQnp2XdTP1o/Vo=",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			static_url_prefix = "/static/",
			login_url='/login',
			xsrf_cookies=False,
		)
		tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = Application()
	app.listen(8810)
	loop = tornado.ioloop.IOLoop.instance()
	tornado.ioloop.IOLoop.instance().start()

