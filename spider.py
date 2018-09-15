'''
断点续传在测试豌豆荚的UC浏览器时失效
豌豆荚			狗屎！豌豆荚网页结构改了
百度			组织上已经决定就拿你测试了！
华为			ua有效，暂时没发现需要cookie。下载链接js
安智
'''
import sys
import time
import sys
import requests
from bs4 import BeautifulSoup
import os
import re
import sqlite3
from pybloom_live import BloomFilter
import shutil


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
num_wandoujia = 2					# max=41
num_baidu = 2						# max=8
num1 = 10
num2 = 4
num3 = 4
num4 = 4
num_total=num1+num2+num3+num4
total_num=0
requests.packages.urllib3.disable_warnings()
DB_PATH = 'C:\\Users\\hasee\\Desktop\\spider\\apk.db'

def guiguiguiguigui0():
	if os.path.exists('C:\\Users\\hasee\\Desktop\\spider\\apk.db'):
		os.remove('C:\\Users\\hasee\\Desktop\\spider\\apk.db')
	if os.path.exists('C:\\Users\\hasee\\Desktop\\spider\\apk.bloom'):
		os.remove('C:\\Users\\hasee\\Desktop\\spider\\apk.bloom')
	if os.path.exists('C:\\Users\\hasee\\Desktop\\spider\\download'):
		shutil.rmtree('C:\\Users\\hasee\\Desktop\\spider\\download',True)
	os.mkdir('C:\\Users\\hasee\\Desktop\\spider\\download')
	print('白茫茫一片真干净')

def init():	
	#数据库文件绝句路径
	global DB_PATH
	DB_PATH = 'C:\\Users\\hasee\\Desktop\\spider\\apk.db'
	#数据库表名称
	global TABLE_NAME
	TABLE_NAME = 'apk_info'
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	result_c=c.execute("select count(*) from sqlite_master where type='table' and name='apk_info'")
	result_n = str(result_c.fetchall()[0]).replace('(','').replace(')','').replace(',','')
	if result_n=='0':
		c.execute('''CREATE TABLE apk_info
			(NAME			NVARCHAR(10)		NOT NULL,
			 URL			TEXT		NOT NULL,
			 TYPE			NVARCHAR(4)		NOT NULL,
			 INTRO			TEXT		NOT NULL,
			 DOWN			TEXT			NOT NULL,
			 MARK			INT		NOT NULL,
			 VERSION		TEXT		NOT NULL);''')
		c.execute('''CREATE TABLE total_info
			(num			INT			NOT NULL,
			 current		TEXT);''')
		c.execute('''insert into total_info(num,current) values(0, 0)''')
		bf_i = BloomFilter(100000)
		bf_i.tofile(open('C:\\Users\\hasee\\Desktop\\spider\\apk.bloom','wb+'))
		print('初始化成功！')
	else:
		print('已进行过初始化')
	conn.commit()
	conn.close()


def insert_values(name_i,url_i,type_i,intro_i,down_i,mark_i,version_i):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	sql_i = 'INSERT INTO apk_info(name,url,type,intro,down,mark,version) VALUES (\''+name_i+'\',\''+url_i+'\',\''+type_i+'\',\''+intro_i+'\',\''+down_i+'\','+mark_i+',\''+version_i+'\')'
	c.execute(sql_i)
	conn.commit()
	conn.close()


def myAlign(string, length=0):
	if length == 0:
		return string
	jud = countchar(string)
	placeholder = chr(12288)
	res = string
	if jud%2==0:
		state=0
		slen = len(string) - jud/2
	else:
		state=1
		slen = len(string) - (jud-1)/2
	while slen < length:
		res += placeholder
		slen += 1
	if state==1:
		res+=' '
	return res


def countchar(str1):
	len1=len(str1)
	str2 = re.sub("[A-Za-z0-9\!\%\[\]\,\。\.\-\(\)\@\#\$\^\&\*\=\+]", "", str1)
	len2=len(str2)
	return len1-len2


def download(url, file_path):
	global total_num
	# 第一次请求是为了得到文件总大小
	r1 = requests.get(url, stream=True, verify=False)
	total_size = int(r1.headers['Content-Length'])

	# 这重要了，先看看本地文件下载了多少
	if os.path.exists(file_path):
		temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
	else:
		temp_size = 0
	# 显示一下下载了多少   
	#print('当前文件已经下载',temp_size,'字节')
	#print('当前文件总计大小',total_size,'字节')
	# 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
	headers = {'Range': 'bytes=%d-' % temp_size}  
	# 重新请求网址，加入新的请求头的
	r = requests.get(url, stream=True, verify=False, headers=headers)

	# 下面写入文件也要注意，看到"ab"了吗？
	# "ab"表示追加形式写入文件
	with open(file_path, "ab") as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				temp_size += len(chunk)
				f.write(chunk)
				f.flush()

				###这是下载实现进度显示####
				done = int(50 * temp_size / total_size)
				sys.stdout.write("\rAPK总数:%d[%s%s] %d%%" % (total_num,'█' * done, '  ' * (50 - done), 100 * temp_size / total_size))
				sys.stdout.flush()
	#sys.stdout.write("\r")
	print()  # 避免上面\r 回车符


def wandoujia():
	#print("{0:{4}^5}\t丨{1:{4}^3}\t丨{2:{4}^3}\t丨{3:{4}^3}丨".format('名称','分类','下载量','好评率',chr(12288)))
	#print(myAlign('名称',num1)+'丨'+myAlign('分类',num2)+'丨'+myAlign('下载量',num3)+'丨'+myAlign('好评率',num4)+'丨')
	#print(myAlign('名称',num1_wandoujia),'\t丨',myAlign('分类',num2_wandoujia),'\t丨',myAlign('下载量',num3_wandoujia),'\t丨',myAlign('好评率',num4_wandoujia),'\t丨')
	print(''.ljust(num_total*2, '-')+'------')
	url_app_store = 'https://www.wandoujia.com/category/app'
	#body = 'app-top clearfix  li'
	res = requests.get(url_app_store)
	soup = BeautifulSoup(res.text, 'html.parser')
	#result = soup.find_all('a','name')	
	category=soup.select('.container ul .parent-cate')
	for j in category:
		category_url = j.select('a')[0]['href']
		for k in range(1,num_wandoujia):
			category_url_bypage = category_url+'/'+str(k)
			res2 = requests.get(category_url_bypage)
			soup3 = BeautifulSoup(res2.text, 'html.parser')

		#for i in soup.select('.app-box #j-top-list li'):
			for i in soup3.select('#j-tag-list li'):
				app_url = i.select('.app-desc .app-title-h2 a')[0]['href']
				detail = requests.get(app_url)
				soup2 = BeautifulSoup(detail.text, 'html.parser')
				#name = i.select('.app-desc .app-title-h2 a')[0].text
				name = soup2.select('.app-name .title')[0].text
				#type = i.select('.tag-link')[0].text
				type = soup2.select('.tag-box a')[0].text
				#intro = i.select('.app-desc .comment')[0].text
				#intro = soup2.select('.desc-info p').text
				intro="Null"
				down = soup2.select('.app-info-data i')[0].text
				mark = soup2.select('.app-info-data i')[1].text 
				dl_url = soup2.select('.download-wp a')[1]['href']
				#print(intro)
				#print(name,'\t丨',type,'\t丨',intro,'\t丨',app_url,'\t丨',down,'\t丨',mark)
				#print("{0:{4}^5}\t丨{1:{4}^3}\t丨{2:{4}^3}\t丨{3:{4}^3}丨".format(myAlign(name,5),myAlign(type,3),myAlign(down,3),myAlign(mark,3),chr(12288)))
				#print(myAlign(name,num1)+'丨'+myAlign(type,num2)+'丨'+myAlign(down,num3)+'丨'+myAlign(mark,num4)+'丨')
				#time.sleep(1)


def baidu():
	judg= os.path.exists('C:\\Users\\hasee\\Desktop\\spider\\apk.db') and os.path.exists('C:\\Users\\hasee\\Desktop\\spider\\apk.bloom') and os.path.exists('C:\\Users\\hasee\\Desktop\\spider\\download')
	if judg == 0:
		print('请初始化')
		return
	global total_num
	bf = BloomFilter.fromfile(open('C:\\Users\\hasee\\Desktop\\spider\\apk.bloom','rb'))
	#print(myAlign('名称',num1)+'丨'+myAlign('分类',num2)+'丨'+myAlign('下载量',num3)+'丨'+myAlign('好评率',num4)+'丨')
	#print(''.ljust(num_total*2, '-')+'------')
	url_app_store = 'https://shouji.baidu.com/software/'
	res = requests.get(url_app_store)
	soup = BeautifulSoup(res.text, 'html.parser')
	category=soup.select('.cate li .cate-head')
	for j in category:
		category_url = j.select('a')[0]['href']
		for k in range(1,num_baidu):
			category_url_bypage = 'https://shouji.baidu.com'+category_url+'list_'+str(k)+'.html'
			#print(category_url_bypage)
			res2 = requests.get(category_url_bypage)
			res2.encoding='UTF-8'
			soup3 = BeautifulSoup(res2.text, 'html.parser')

			#for i in soup.select('.app-box #j-top-list li'):
			for i in soup3.select('.app-bd ul .firrow'):
				app_url = 'https://shouji.baidu.com'+i.select('a')[0]['href']
				detail = requests.get(app_url)
				detail.encoding='UTF-8'
				soup2 = BeautifulSoup(detail.text, 'html.parser')
				#name = i.select('.app-desc .app-title-h2 a')[0].text
				name = soup2.select('.content-right h1 span')[0].text[0:10]
				#type = i.select('.tag-link')[0].text
				type = soup2.select('.nav a')[2].text
				#intro = i.select('.app-desc .comment')[0].text
				intro = str(soup2.select('.section-body .brief-long p')).replace('[<p class="content content_hover">','').replace('<span class="occupied"></span></p>]','').replace('<br/>','\n')
				#intro="Null"
				down = soup2.select('.detail span')[2].text[6:]
				mark = soup2.select('.content-right .app-feature .star-xbig .star-percent')[0]['style'][6:].replace('%', '')
				dl_url = soup2.select('.area-download a')[1]['href']
				#print(isinstance(dl_url,str))				
				version = soup2.select('.detail span')[1].text[3:]
				if (app_url in bf) == False:
					dl_path='C:\\Users\\hasee\\Desktop\\spider\\download\\'+name+'.apk'
					sql_bd2='update total_info set current =\''+dl_url+'\''
					sql_bd3='''update total_info set current = '0' '''
					conn = sqlite3.connect(DB_PATH)
					c = conn.cursor()
					total_num=int(str(c.execute('select num from total_info').fetchall()[0]).replace('(','').replace(')','').replace(',',''))
					url_bd=str(c.execute('select current from total_info').fetchall()[0]).replace('(','').replace(')','').replace('\'','').replace(',','')
					c.execute(sql_bd2)
					conn.commit()
					conn.close()
					print('正在下载',name)
					if url_bd == '0':
						insert_values(name,app_url,type,intro,down,mark,version)
						download(dl_url,dl_path)
						total_num+=1
					else:
						download(url_bd,dl_path)
					bf.add(app_url)
					sql_bd1='update total_info set num ='+str(total_num)
					conn = sqlite3.connect(DB_PATH)
					c = conn.cursor()
					c.execute(sql_bd1)
					c.execute(sql_bd3)
					conn.commit()
					conn.close()
					bf.tofile( open('C:\\Users\\hasee\\Desktop\\spider\\apk.bloom','wb'))
				#print(version)
				#print(name,'\t丨',type,'\t丨',intro,'\t丨',app_url,'\t丨',down,'\t丨',mark)
				#print("{0:{4}^5}\t丨{1:{4}^3}\t丨{2:{4}^3}\t丨{3:{4}^3}丨".format(myAlign(name,5),myAlign(type,3),myAlign(down,3),myAlign(mark,3),chr(12288)))
				#print(name,'丨',type,'丨',down,'丨',mark,'丨')
				#print(myAlign(name,num1)+'丨'+myAlign(type,num2)+'丨'+myAlign(down,num3)+'丨'+myAlign(mark,num4)+'丨')
				#time.sleep(1)
	

def huawei():
	print(myAlign('名称',num1)+'丨'+myAlign('分类',num2)+'丨'+myAlign('下载量',num3)+'丨'+myAlign('好评率',num4)+'丨')
	print(''.ljust(num_total*2, '-')+'------')
	url_app_store = 'http://app.hicloud.com/soft/list'
	res = requests.get(url_app_store,headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	category=soup.select('.head-right a')
	for j in category:
		category_url = j['href']
		
		category_url_bypage = 'http://app.hicloud.com'+category_url
		#print(category_url_bypage)
		res2 = requests.get(category_url_bypage,headers=headers)
		res2.encoding='UTF-8'
		soup3 = BeautifulSoup(res2.text, 'html.parser')

		#for i in soup.select('.app-box #j-top-list li'):
		for i in soup3.select('.unit-main .list-game-app'):
			app_url = 'http://app.hicloud.com'+i.select('.title a')[0]['href']
			detail = requests.get(app_url,headers=headers)
			detail.encoding='UTF-8'
			soup2 = BeautifulSoup(detail.text, 'html.parser')
			#name = i.select('.app-desc .app-title-h2 a')[0].text
			name = soup2.select('.lay-left span')[0].text
			#type = i.select('.tag-link')[0].text
			type = soup3.select('.head-right span')[0].text
			#intro = i.select('.app-desc .comment')[0].text
			#intro = soup2.select('.desc-info p').text
			intro="Null"
			down = soup2.select('.lay-left span')[1].text[3:]
			mark = re.sub("[A-Za-z\[\]\'\_]", "", str(soup2.select('.lay-main div div div div ul span')[2]['class']))
			#dl_url = soup2.select('.area-download a')[1]['href']
			#print(intro)
			#print(name,'\t丨',type,'\t丨',intro,'\t丨',app_url,'\t丨',down,'\t丨',mark)
			#print("{0:{4}^5}\t丨{1:{4}^3}\t丨{2:{4}^3}\t丨{3:{4}^3}丨".format(myAlign(name,5),myAlign(type,3),myAlign(down,3),myAlign(mark,3),chr(12288)))
			#print(name,'丨',type,'丨',down,'丨',mark,'丨')
			print(myAlign(name,num1)+'丨'+myAlign(type,num2)+'丨'+myAlign(down,num3)+'丨'+myAlign(mark,num4)+'丨')
			#time.sleep(1)


if __name__ == '__main__':
	choice=-1
	while choice!=0:
		sys.stdout.write('1.初始化\n2.爬取市场\n3.归归归归归零！\n')
		choice = int(input("做出你的选择: "))		
		os.system('cls')
		if choice==1:
			init()
		elif choice==3:
			guiguiguiguigui0()
		elif choice ==2:
			baidu()
		time.sleep(1)
