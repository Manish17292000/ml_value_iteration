import numpy as np
import os
iteration=0
Y=0.99
delta=1e-3
stepcost=-20
stepcost_shoot=-20
finalreward=10
action="-1"
recharge_prob=0.8
attack_prob=0.5
dodge_prob=0.8
arrow_prob=0.8

def recharge(i, j, k, utility):
	return (recharge_prob)*(stepcost+Y*utility[i][j][min(utility.shape[2]-1, k+1)])+ (1-recharge_prob)*(stepcost+Y*utility[i][j][k])

def shoot(i, j, k, utility):
	global stepcost
	global stepcost_shoot
	if j and k:
		# print(stepcost_shoot)
		if i==1:
			return attack_prob*(stepcost_shoot+finalreward+Y*utility[i-1][j-1][k-1])+(1-attack_prob)*(stepcost_shoot+Y*utility[i][j-1][k-1])
		else:
			return attack_prob*(stepcost_shoot+Y*utility[i-1][j-1][k-1])+(1-attack_prob)*(stepcost_shoot+Y*utility[i][j-1][k-1])
	else :
		return -100000

def dodge(i, j, k, utility):
	if k==2:
		return dodge_prob*(arrow_prob*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-1])+(1-arrow_prob)*(stepcost+Y*utility[i][j][k-1]))+(1-dodge_prob)*(arrow_prob*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-2])+(1-arrow_prob)*(stepcost+Y*utility[i][j][k-2]))
	elif k==1:
		return arrow_prob*(stepcost+Y*utility[i][min(j+1, utility.shape[1]-1)][k-1])+(1-arrow_prob)*(stepcost+Y*utility[i][j][k-1])
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

		# print(i, j, k,shoot(i, j, k, previousutility),dodge(i, j, k, previousutility),recharge(i, j, k, previousutility) )

toprint=""
def solve():
	global iteration
	global Y
	global delta
	global action
	global toprint
	toprint=""
	utility=np.zeros([5, 4, 3], dtype=float)
	new=np.zeros([5, 4, 3], dtype=float)
	iteration=0
	actionarr=np.zeros([5, 4, 3], dtype=object)
	while 1:
		previousutility=np.copy(utility)
		# print("iteration=", iteration, sep="")
		toprint+="iteration="
		toprint+=str(iteration)
		toprint+="\n"
		for i in range(0,utility.shape[0]):
			for j in range(0, utility.shape[1]):
				for k in range(0, utility.shape[2]):
					action="-1"
					updateutility(i, j, k, utility, previousutility)
		
		for i in range(0,utility.shape[0]):
			for j in range(0, utility.shape[1]):
				for k in range(0, utility.shape[2]):
					action="-1"
					newutility=np.copy(utility)
					updateutility(i, j, k, newutility, utility)
					toprint+="("+str(i)+"," +str(j)+ ","+str(k)+"):"+str(action)+"=["+ str(round(utility[i][j][k], 3))+str("]")+"\n"
					# print("(", i, ",", j, ",", k, "):",action,"=[", round(utility[i][j][k], 3), "]", sep="")
		

		if delta>np.max(abs(previousutility-utility)):
			break
		toprint+="\n\n"
		iteration+=1



if os.path.exists("outputs")==0:
	os.mkdir("outputs")
solve()
file = open("outputs/task_1_trace.txt", "w") 
file.write(toprint) 
file.close()


stepcost=-2.5
stepcost_shoot=-0.25
iteration=0
solve()
file = open("outputs/task_2_part_1_trace.txt", "w") 
file.write(toprint) 
file.close()


Y=0.1
stepcost=-2.5
stepcost_shoot=-2.5
iteration=0
solve()
file = open("outputs/task_2_part_2_trace.txt", "w") 
file.write(toprint) 
file.close()


Y=0.1
stepcost=-2.5
stepcost_shoot=-2.5
delta=1e-10
iteration=0
solve()
file = open("outputs/task_2_part_3_trace.txt", "w") 
file.write(toprint) 
file.close()
