#!/user/bin/python
#coding=utf-8

import filecmp
import os,sys
import re

#需要全路径显示时，添加当前目录前半段路径
prepath = ""


filtertype = [] #过滤数组，可直接添加
screentype = [] #帅选数组，可直接添加
operatetype = 0
curpath = sys.path[0]

def menu_fun():
    global filtertype
    global screentype
    global operatetype
    print "\n==========文件比对工具============="
    print "           --Mr.--\n"
    print "     1、查看目录下的所有文件"
    print "     2、查看文件或目录大小"
    print "     3、输出文件版本更新列表"
    print "     4、设置过滤或帅选文件类型"
    print "     5、显示帮助"
    print "     0、退出\n"
    while True:
        sel = raw_input("\n  请选择: ")
        if sel=="1":
        	rawpath  = raw_input("请输入文件夹路径:")
        	rawpath  = rawpath.strip()
        	if isEmpty(rawpath):
        		print("目录不能为空")
        		continue
        	filelist = all_path(rawpath)
        	savepath(filelist)
        elif sel=="2":
			rawpath  = raw_input("请输入文件或文件夹路径:")
			rawpath  = rawpath.strip()
			if os.path.isfile(rawpath):
				print ("文件大小为:%s"%getFileSize(rawpath))
				continue
			if isEmpty(rawpath):
				print("目录不能为空")
				continue
			print ("总大小为:%s"%getContentsSize(rawpath))
			dirs = os.listdir(rawpath)
			for subdir in dirs:
				subsize = getContentsSize(rawpath + "/" +subdir)
				print ("%s :  %s"%(subdir.ljust(20," "),subsize))
        elif sel=="3":
        	newpath  = raw_input("请输入文件夹新路径:").strip()
        	oldpath  = raw_input("请输入文件夹原路径:").strip()
        	if isEmpty(newpath) | isEmpty(oldpath):
        		print("目录不能为空")
        	else:
				content = all_path(newpath)
				changelist(content,newpath,oldpath)
        elif sel=="4":
        	selectType = raw_input("请输入操作类型(f:过滤,s:帅选,n:无):").strip()
        	if selectType == "f":
        		operatetype = 1
        		typestr = raw_input("请输入需要过滤的类型(以空格分隔):").strip()
        		filtertype = typestr.split(" ")
        	elif selectType == "s":
        		operatetype = 2
        		typestr = raw_input("请输入需要帅选的类型(以空格分隔):").strip()
        		screentype = typestr.split(" ")
        	else:
        		operatetype = 0
        		filtertype = []
        		screentype = []

        	print("设置成功")
    	elif sel=="5":
    		help()
        else:
        	exit()
    return


def isEmpty(string):
    if string == None or len(string) == 0:
        return True
    else:
        return False

def getFileType(path):
    strA = path.split("/")
    targetN = strA[-1].split(".")
    name = targetN[-1]
    return name

def isFilter(filePath):
	if len(filtertype) == 0:
		return False
	typeA = filePath.split(".")
	typename = typeA[-1]
	for x in filtertype:
		if typename == x:
			return True
		
	return False

def isScreen(filePath):
	if len(screentype) == 0:
		return False
	typeA = filePath.split(".")
	typename = typeA[-1]
	for x in screentype:
		if typename == x:
			return True
		
	return False

def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1000
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1000:
        M = kb / 1000
        if M >= 1000:
            G = M / 1000
            return "%.6fG" % (G)
        else:
            return "%.4fM" % (M)
    else:
        return "%.2fkb" % (kb)

def getFileSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)

def getContentsSize(path):
	if os.path.isfile(path):
		return getFileSize(path)
	sumsize = 0
	try:
	    filename = os.walk(path)
	    for root, dirs, files in filename:
	     	for fle in files:
	     		apath = os.path.join(root,fle)
	     		size = os.path.getsize(apath)
	     		sumsize += size
	    return formatSize(sumsize)
	except Exception as err:
		print("计算大小异常")

def all_path(dirname):
	result = []
	if operatetype == 1:
		for maindir, subdir, file_name_list in os.walk(dirname):
			for filename in file_name_list:
				if not isFilter(filename):	
					apath = os.path.join(maindir,filename)
					result.append(apath)
	elif operatetype == 2:
		for maindir, subdir, file_name_list in os.walk(dirname):
			for filename in file_name_list:
				if isScreen(filename):
					apath = os.path.join(maindir,filename)
					result.append(apath)
	else:
		for maindir, subdir, file_name_list in os.walk(dirname):
			for filename in file_name_list:
				apath = os.path.join(maindir,filename)
				result.append(apath)

	return result

def savepath(re):
	file = open(curpath + "/path.txt","w")
	line = ""
	for k in range(0, len(re)):
		filepath = str(re[k])
		nameA = filepath.split("/")	
		name = nameA[-1].ljust(45," ")
		size = getFileSize(filepath)
		line = line + name + size.ljust(15," ") + prepath + filepath + "\n"

	if line == "":
		line = "该目录无文件"
	file.write(line)
	file.close()
	print("结果已保存至path.txt中")

def changelist(re,rawpath, rawpath2):
	file = open(curpath + "/compare.txt","w")
	line = ""
	for k in range(0, len(re)):
		fileName = str(re[k])
		nameA = fileName.split("/")
		name = nameA[-1].ljust(30," ")
		path2 = fileName.replace(rawpath, rawpath2, 1)
		filetype = getFileType(re[k])
		size = getFileSize(fileName)
		change = ""
		if os.path.exists(path2):
			isbool = filecmp.cmp(fileName,path2)
			if not isbool:
				change = "修改  "
				line = line  + name + filetype.ljust(8, " ") + change.ljust(10, " ")+ size.ljust(15," ") + "  " + prepath + fileName.replace(rawpath, "", 1) + "\n"
		else:
			change = "新增  "
			line = line + name + filetype.ljust(8, " ") + change.ljust(10, " ")+ size.ljust(15," ") + "  " + prepath + fileName.replace(rawpath, "", 1) + "\n"
		
	if line == "":
		line = "该目录无更新文件"
	file.write(line)
	file.close()
	print("结果已保存至compare.txt中")
		
def help():
	print("\n 该工具主要查看指定目录下的所有文件及路径,对比两文件夹文件的不同,具体内容如下:\n 选1:则输出当前目录及子目录所有文件信息\n 选2:则输出文件夹的大小及子一级文件或目录的大小\n 选3:则输出版本更新文件列表，修改或新增列表，输入目录顺序不同结果不同\n 选4:设置全局的帅选或过滤条件（类型无需输入.）,若需取消则需重新设置为空\n 选5:则查看帮助\n 选0:则退出工具\n\n 注意: 若输入目录中包含中文则可能导致结果错误")
	return

def main():
	menu_fun()
	return

main()













