import numpy as np

iteration=0
Y=0.99
delta=1e-3
stepcost=-20
finalreward=10
utility=np.zeros([5, 4, 3], dtype=float)
new=np.zeros([5, 4, 3], dtype=float)
actionarr=np.zeros([5, 4, 3], dtype=object)
action="-1"

def recharge(i, j, k, utility):
	return round(0.8*(stepcost+Y*utility[i][j][min(utility.shape[2]-1, k+1)])+0.2*(stepcost+Y*utility[i][j][k]), 11)

def shoot(i, j, k, utility):
	if j and k:
		if i==1:
			return round(0.5*(stepcost+finalreward+Y*utility[i-1][j-1][k-1])+0.5*(stepcost+Y*utility[i][j-1][k-1]),11)
		else:
			return round(0.5*(stepcost+Y*utility[i-1][j-1][k-1])+0.5*(stepcost+Y*utility[i][j-1][k-1]),11)
	else :
		return -100000

def dodge(i, j, k, utility):
	if k==2:
		return round(0.8*(0.8*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-1])+0.2*(stepcost+Y*utility[i][j][k-1]))+0.2*(0.8*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-2])+0.2*(stepcost+Y*utility[i][j][k-2])),11)
	elif k==1:
		return round(0.8*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-1])+0.2*(stepcost+Y*utility[i][j][k-1]),11)
	else :
		return -100000

def updateutility(i, j, k, utility,  previousutility):
	if i==0:
		utility[i][j][k]=0
	else :
		global action
		utility[i][j][k]=shoot(i, j, k, previousutility)
		action="SHOOT"
		if utility[i][j][k]<dodge(i, j, k, previousutility):
			utility[i][j][k]=dodge(i, j, k, previousutility)
			action="DODGE"
		if utility[i][j][k]<recharge(i, j, k, previousutility):
			utility[i][j][k]=recharge(i, j, k, previousutility)
			action="RECHARGE"

		# print(shoot(i, j, k, previousutility),dodge(i, j, k, previousutility),recharge(i, j, k, previousutility) )

while 1:
	previousutility=np.copy(utility)
	print("iteration=", iteration, sep="")
	for i in range(0,utility.shape[0]):
		for j in range(0, utility.shape[1]):
			for k in range(0, utility.shape[2]):
				action="-1"
				updateutility(i, j, k, utility, previousutility)
				actionarr[i][j][k]=action
				# if delta<abs(previousutility[i][j][k]-utility[i][j][k]) or i==0:
				# print("(", i, ",", j, ",", k, "):",action,"=[", round(utility[i][j][k], 3), "]", sep="")
	
	

	if delta>np.max(abs(previousutility-utility)):
		previousutility=np.copy(utility)
		for i in range(0,utility.shape[0]):
			for j in range(0, utility.shape[1]):
				for k in range(0, utility.shape[2]):
					action="-1"
					updateutility(i, j, k, new, previousutility)
					print("(", i, ",", j, ",", k, "):",action,"=[", round(utility[i][j][k], 3), "]", sep="")
					
		print()
		print()
		break
	for i in range(0,utility.shape[0]):
		for j in range(0, utility.shape[1]):
			for k in range(0, utility.shape[2]):
				print("(", i, ",", j, ",", k, "):",actionarr[i][j][k],"=[", round(utility[i][j][k], 3), "]", sep="")

	print()
	print()
	iteration+=1

print(iteration)