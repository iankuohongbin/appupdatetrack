# -*- coding: utf-8 -*-
#coding=utf-8

import urllib.request;
import json;
import os;
import string;
#设定
url_base = 'https://itunes.apple.com/cn/lookup?id='
database = ('/Users/xorworm/Documents/coder/python/scrapy/update')

print ('获取更新输入1\n增加新项目输入2')
option = input()
if option == "1":
	print ('更新中，请稍候')
	update_file = open(database,'r+')
	apps=[line.strip() for line in update_file.readlines()]
	apps_list=[]
	item_list=[]
	for line in apps:
		url = url_base+str(json.loads(line)["trackId"])
		#print (url)
		app_old = json.loads(line)
	#	print(type(app_old))
	#	print (app_old)
		app_new_raw =urllib.request.urlopen(url).read()
		app_new_json=json.loads(app_new_raw.decode('utf-8'))['results'][0]
		app_new_dict = {"trackId":app_new_json["trackId"],
				"trackName":app_new_json["trackName"],
				"description":app_new_json["description"],
				"currentVersionReleaseDate":app_new_json["currentVersionReleaseDate"],
				"primaryGenreName":app_new_json["primaryGenreName"],
				"trackViewUrl":app_new_json["trackViewUrl"],
				"artworkUrl512":app_new_json["artworkUrl512"],
				"releaseNotes":app_new_json["releaseNotes"],
				"lastupdate":"Y",
				"version":app_new_json["version"],
				"history":app_new_json["currentVersionReleaseDate"]+"\t"+app_new_json["version"]+"\n"+app_new_json["releaseNotes"]+"\n"
				} #获取完两个字典
	#	print (app_new_dict)
	#	print (type(app_old))
		#比较两个字典
		if app_new_dict["version"] ==app_old["version"]:
			app_old["lastupdate"] = 'N'
		else:
			app_old["description"] = app_new_dict["description"]
			app_old["currentVersionReleaseDate"]=app_new_dict["currentVersionReleaseDate"]
			app_old["artworkUrl512"]=app_new_dict["artworkUrl512"]
			app_old["releaseNotes"] = app_new_dict["releaseNotes"]
			app_old["version"]= app_new_dict["version"]
			app_old["history"] = app_old["history"]+app_new_dict["history"]
			item_list.append(app_old["trackName"])
			app_old["lastupdate"]="Y"

		apps_list.append(app_old)

	update_file.close()
	update_file=open(database,'w') #写入新内容
	for line in apps_list: 
		newJson = json.dumps(line)
		update_file.writelines(newJson+'\n')
	update_file.close()
	print ("有"+str(len(item_list))+"个更新")
	for item in item_list:
		print(item+"有更新")
	print ('查看更新内容，按1')
	check = input()
	if check =="1":
		print ('\n\n\n\n\n\n')
		for line in apps_list:
			if line["lastupdate"]=="Y":
				print ("==============================")
				print ("trackName:"+str(line["trackName"])+"\ntrackid:"+str(line["trackId"])+"\t类型:"+str(line["primaryGenreName"])+"\nversion:"+str(line["version"])+"\t 更新日期："+str(line["currentVersionReleaseDate"])+"\n更新内容:"+str(line["releaseNotes"]))




elif option =="2":   #输入新ID
	print ('输入选项ID')
	id_input = input()
	bool_id_input = 0
	id_file = open(database,'r')
	id_list = [line.strip() for line in id_file.readlines()]
	for line in id_list:
		if str(json.loads(line)["trackId"])==id_input: # 比较是否存在
		#	print (str(json.loads(line)["trackId"]) +'=='+ id_input )
			bool_id_input = 1
		#else:
		#	print (str(json.loads(line)["trackId"])+'!='+ id_input )

	id_file.close()   #读完关闭

	if bool_id_input == 1: #开始写入新的
		print(id_input+'项目已存在')
	elif bool_id_input ==0: #添加新项目
		url = url_base+id_input
		update_file = open(database,'a')
		rawtext = urllib.request.urlopen(url).read()
		json_count = json.loads(rawtext.decode('utf-8'))['resultCount']
		if json_count == 1:
			jsonStr = json.loads(rawtext.decode('utf-8'))['results'][0]
			newDict = {"trackId":jsonStr["trackId"],
				"trackName":jsonStr["trackName"],
				"description":jsonStr["description"],
				"currentVersionReleaseDate":jsonStr["currentVersionReleaseDate"],
				"primaryGenreName":jsonStr["primaryGenreName"],
				"trackViewUrl":jsonStr["trackViewUrl"],
				"artworkUrl512":jsonStr["artworkUrl512"],
				"releaseNotes":jsonStr["releaseNotes"],
				"lmastupdate":"Y",
				"version":jsonStr["version"],
				"history":jsonStr["currentVersionReleaseDate"]+"\n"+jsonStr["releaseNotes"]+"\n"
				}

			newJson = json.dumps(newDict) #写入
			update_file.writelines(newJson+'\n')
			print (id_input+"项目已添加，是否查看最新更新 y/n")
			new_view =input()
			if new_view == "y":
				print ("==============================")
				print ("trackName:"+str(newDict["trackName"])+"\ntrackid:"+str(newDict["trackId"])+"\t类型:"+str(newDict["primaryGenreName"])+"\nversion:"+str(newDict["version"])+"\n更新内容:"+str(newDict["releaseNotes"])+"\n")
			elif new_view =='n':
				print("好的，不看")		
		else:
			print (str(json_count)+"\n新项目无法获取")
		update_file.close() #写完关闭

elif option == "3":
	update_file = open(database,'r+')
	apps=[line.strip() for line in update_file.readlines()]
	for line in apps:
		app_old = json.loads(line)
		print (str(app_old["trackId"])+"\t"+str(app_old["trackName"]))
	update_file.close

elif option == "4":
	print ("请输入新数据库路径")

#        #添加ID
#        print('Input your Tracking ID:')
#        id_input = input()
#        
#        id_file = open('/Users/xorworm/Documents/coder/python/scrapy/appid','r')
#        #id_list = id_file.readlines()
#        id_list = [line.strip() for line in id_file.readlines()]
#        #print type(id_list)
#        #print id_list
#        id_file.close()
#        repeat = 'n'
#        for app in id_list:
#        	if id_input == app:
#        		repeat = 'y'
#        if repeat == 'n':
#        	id_list.append(id_input)
#        #print id_list
#        
#        #写入新列表
#        id_file = open('/Users/xorworm/Documents/coder/python/scrapy/appid','w')
#        for app in id_list:
#        	id_file.writelines(app+'\n')
#        
#        id_file.close()
#        
#        #生成地址
#        urldb=[]
#        id_file = open('/Users/xorworm/Documents/coder/python/scrapy/appid','r')
#        id_list = [line.strip() for line in id_file.readlines()]
#        for trackid in id_list:
#        	if trackid != '':
#        		url=url_base+trackid
#        		urldb.append(url)
#        #print urldb
#        id_file.close()
#        #获取更新
#        update_file = open('/Users/xorworm/Documents/coder/python/scrapy/update','w')
#        for url in urldb:
#        	rawtext = urllib.request.urlopen(url).read()
#        	jsonCount = json.loads(rawtext.decode('utf-8'))['resultCount']
#        	if jsonCount == 1 :
#        		if("trackId" in json.loads(rawtext.decode('utf-8'))['results'][0]):
#        			jsonStr = json.loads(rawtext.decode('utf-8'))['results'][0]
#        			
#        			newDict = {'trackId':jsonStr["trackId"],'Trackname':jsonStr["trackName"],
#        			'description':jsonStr["description"],
#        			"currentVersionReleaseDate":jsonStr["currentVersionReleaseDate"],
#        			"primaryGenreName":jsonStr["primaryGenreName"],
#        			"trackViewUrl":jsonStr["trackViewUrl"],
#        			"artworkUrl512":jsonStr["artworkUrl512"],
#        			"releaseNotes":jsonStr["releaseNotes"],
#        			"version":jsonStr["version"]
#        			}
#        			print (url +'信息已更新')
#        			#print rawtext
#        			#print jsonCount
#        			newJson = json.dumps(newDict)
#        			update_file.writelines(newJson+'\n')
#        		else:
#        			print(url + "对应编号非软件")
#        
#        	elif jsonCount ==0:
#        		print (url + "信息无法获取")
#        
#        update_file.close#        