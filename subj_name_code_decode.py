import pandas as pd
import numpy as np
import re
import os
import random

def dec_to_baseb(val,bb):
	# bb should be between 1 and 9
	tmp = val
	result = ''
	while tmp>=bb:
		result = str(tmp%bb) + result
		tmp = tmp//bb
	result = str(tmp)+result
	return int(result)
	
def baseb_to_dec(val,bb):
	# bb should be between 1 and 9
	tmp = str(val)
	tmp = tmp[::-1]
	result = 0
	for ii,dd in enumerate(tmp):
		result += int(dd)*(bb**ii)
	return result

# def name_code_simple(ss):
	# ss = ss.lower()
	# result = "# "
	# for cc in ss:
		# result += "%.3d"%(dec_to_baseb(ord(cc),9))
	# result = [cc for cc in result]
	
	# foil_n = random.sample(range((len(result)-2)//6),1)[0]
	# foil_id = random.sample(range(2,len(result)),foil_n)
	# for ii in foil_id:
		# result.insert(ii,'9')
	# result = ''.join(result)	
	# return result

def name_code(ss=""):
	if ss=="":
		ss = input("Tell me the name you want to encode.\n")
	ss = ss.lower()
	ord_list = []
	for cc in ss:
		ord_list += ["%.3d"%ord(cc)]
	# print(ord_list)
	ord_list = ["".join(ord_list[ii*2:(ii+1)*2]) for ii in range(len(ord_list)//2)]+[ord_list[-1]+"000"]*(len(ord_list)%2)
	ord_list = ["%.6d"%(dec_to_baseb(int(oo),9)) for oo in ord_list]
		
	result = "# "+"".join(ord_list)
	result = [cc for cc in result]
	
	foil_n = random.sample(range((len(result)-2)//6),1)[0]
	foil_id = random.sample(range(2,len(result)),foil_n)
	for ii in foil_id:
		result.insert(ii,'9')
	result = ''.join(result)	
	print("This is the encoded name:")
	print(result)
	return result
	
def name_decode(ss=""):
	if ss=="":
		ss = input("Tell me the name you want to decode.\n")
	ss = ss[2:]
	ss = [ii for ii in ss if ii!='9']
	ss = ["".join(ss[ii*6:(ii+1)*6]) for ii in range(len(ss)//6)]
	ss = ["%.6d"%baseb_to_dec(int(ii),9) for ii in ss]
	# print(ss)
	ss = [chr(int(cc[:3]))+chr(int(cc[3:]))*(cc[3:]!="000") for cc in ss]
	result="".join(ss)
	
	result = " ".join([nn.capitalize() for nn in result.split(" ")])
	print("This is the decoded name:")
	print(result)
	return result
	
# def name_decode_simple(ss):
	# ss = ss[2:]
	# ss = [ii for ii in ss if ii!='9']
	# ss = ["".join(ss[ii*3:(ii+1)*3]) for ii in range(len(ss)//3)]
	# result = "".join([chr(baseb_to_dec(int(ii),9)) for ii in ss])
	# result = " ".join([nn.capitalize() for nn in result.split(" ")])
	# print(result)
	# return result

code = name_code()
print()
name_decode()