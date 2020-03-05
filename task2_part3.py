import numpy as np

iteration=0
Y=0.1
delta=1e-10
stepcost=-2.5
finalreward=10
utility=np.zeros([5, 4, 3], dtype=float)
action="-1"

def recharge(i, j, k, utility):
	return 0.8*(stepcost+Y*utility[i][j][min(utility.shape[2]-1, k+1)])+0.2*(stepcost+Y*utility[i][j][k])

def shoot(i, j, k, utility):
	if j and k:
		return 0.5*(stepcost+finalreward+Y*utility[i-1][j-1][k-1])+0.5*(stepcost+Y*utility[i][j-1][k-1])
	else :
		return -100000

def dodge(i, j, k, utility):
	if k==2:
		return 0.8*(0.8*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-1])+0.2*(stepcost+Y*utility[i][j][k-1]))+0.2*(0.8*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-2])+0.2*(stepcost+Y*utility[i][j][k-2]))
	elif k==1:
		return 0.8*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-1])+0.2*(stepcost+Y*utility[i][j][k-1])
	else :
		return -100000

def updateutility(i, j, k, utility):
	if i==0:
		utility[i][j][k]=0
	else :
		global action
		utility[i][j][k]=recharge(i, j, k, utility)
		action="RECHARGE"
		if utility[i][j][k]<dodge(i, j, k, utility):
			utility[i][j][k]=dodge(i, j, k, utility)
			action="DODGE"
		if utility[i][j][k]<shoot(i, j, k, utility):
			utility[i][j][k]=shoot(i, j, k, utility)
			action="SHOOT"
		# print(action)

while 1:
	previousutility=np.copy(utility)
	iteration+=1
	print("iteration=", iteration)
	for i in range(0,utility.shape[0]):
		for j in range(0, utility.shape[1]):
			for k in range(0, utility.shape[2]):
				action="-1"
				updateutility(i, j, k, utility)
				print("(", i, ",", j, ",", k, "):",action,"=[", utility[i][j][k], "]", sep="")
				
	print()
	print()
	if delta>np.max(previousutility-utility):
		break

print(iteration)