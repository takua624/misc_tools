import numpy as np

def HSV_to_RGB(H,S,V):
	# H: 0~360
	# S: 0~1
	# V: 0~1
	if not (0<=H<360 and 0<=S<=1 and 0<=V<=1):
		print("Please make sure that 0<=H<360 and 0<=S<=1 and 0<=V<=1")
		print("return black")
		return (0,0,0)
	C = S * V
	X = C * (1 - np.abs((H/60)%2-1))
	m = V - C
	R = m + C*(0<=H<60 or 300<=H<360) + X*(60<=H<120 or 240<=H<300)
	G = m + C*(60<=H<120 or 120<=H<180) + X*(0<=H<60 or 180<=H<240)
	B = m + C*(180<=H<240 or 240<=H<300) + X*(120<+H<180 or 300<=H<360)
	hex_string = "#" + hex(int(R*255))[2:] + hex(int(G*255))[2:] + hex(int(B*255))[2:]
	return (R,G,B, hex_string)
	
def HSL_to_RGB(H,S,L):
	# H: 0~360
	# S: 0~1
	# L: 0~1
	if not (0<=H<360 and 0<=S<=1 and 0<=L<=1):
		print("Please make sure that 0<=H<360 and 0<=S<=1 and 0<=V<=1")
		print("return black")
		return (0,0,0)
	C = (1 - np.abs(2*L-1)) * S
	X = C * (1 - np.abs((H/60)%2-1))
	m = L - C/2
	R = m + C*(0<=H<60 or 300<=H<360) + X*(60<=H<120 or 240<=H<300)
	G = m + C*(60<=H<120 or 120<=H<180) + X*(0<=H<60 or 180<=H<240)
	B = m + C*(180<=H<240 or 240<=H<300) + X*(120<+H<180 or 300<=H<360)
	hex_string = "#" + hex(int(R*255))[2:] + hex(int(G*255))[2:] + hex(int(B*255))[2:]
	return (R,G,B, hex_string)
	
def RGB_to_HSV(R=0,G=0,B=0, hex_string=""):
	# R: 0~255, or 0~1
	# G: 0~255, or 0~1
	# B: 0~255, or 0~1
	# hex_code: in the format "#rrggbb"
	if hex_string:
		R = int(hex_string[1:3],16)
		G = int(hex_string[3:5],16)
		B = int(hex_string[5:],16)
	if R>1 or G>1 or B>1:
		R = R/255
		G = G/255
		B = B/255
	Cmax = np.max((R,G,B))
	Cmin = np.min((R,G,B))
	delta = Cmax - Cmin
	
	if not delta:
		H = 0
	else:
		H = 0 + 60*(((G-B)/delta)%6)*(Cmax==R) + 60*((B-R)/delta+2)*(Cmax==G) + 60*((R-G)/delta+4)*(Cmax==B)
		
	if not Cmax:
		S = 0
	else:
		S = delta/Cmax
		
	V = Cmax
	
	return (H,S,V)
	
def RGB_to_HSL(R=0,G=0,B=0, hex_string=""):
	# R: 0~255, or 0~1
	# G: 0~255, or 0~1
	# B: 0~255, or 0~1
	# hex_code: in the format "#rrggbb"
	if hex_string and R==0 and G==0 and B==0:
		R = int(hex_string[1:3],16)
		G = int(hex_string[3:5],16)
		B = int(hex_string[5:],16)
	if R>1 or G>1 or B>1:
		R = R/255
		G = G/255
		B = B/255
	Cmax = np.max((R,G,B))
	Cmin = np.min((R,G,B))
	delta = Cmax - Cmin
	
	if not delta:
		H = 0
	else:
		H = 0 + 60*(((G-B)/delta)%6)*(Cmax==R) + 60*((B-R)/delta+2)*(Cmax==G) + 60*((R-G)/delta+4)*(Cmax==B)
		
	L = (Cmax+Cmin)/2
	
	if not delta:
		S = 0
	else:
		S = delta/(1-np.abs(2*L-1))
		
	return (H,S,L)
	
def HSV_to_HSL(H,S,V):
	(R,G,B,_) = HSV_to_RGB(H,S,V)
	return RGB_to_HSL(R,G,B)
	
def HSL_to_HSV(H,S,L):
	(R,G,B,_) = HSL_to_RGB(H,S,L)
	return RGB_to_HSV(R,G,B)
	
# (R,G,B) = (86,163, 170)
# print((R,G,B))
# # print(hex_string)
# # print(RGB_to_HSV(R,G,B))
# # print(RGB_to_HSL(R,G,B))
# H1,S1,V1 = RGB_to_HSV(R,G,B)
# print((H1,S1,V1))
# H2,S2,L2 = (0,0,0)
# for ii in range(10):
	# R,G,B,hex_string = HSV_to_RGB(H1,S1,V1)
	# H1,S1,V1 = RGB_to_HSV(hex_string=hex_string)
	# print((H1,S1,V1))
	# print((R,G,B))
# # print(HSL_to_HSV(185, 0.33070866, 0.501960784))
# # print(RGB_to_HSV(hex_string=hex_string))