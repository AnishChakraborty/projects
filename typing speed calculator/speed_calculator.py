from time import *
import random as r

def mistake(paratest,usertest):
    error = 0
    for i in range(len(paratest)):
        try:
            if paratest[i]!=usertest[i]:
                error = error + 1
        except:
            error = error + 1
    return error

def speed_time(time_s,time_e,user_input):
    time_Delay = time_e - time_s
    round_time = round(time_Delay,2)
    speed = len(user_input)/round_time
    return round(speed,2)


test = ["i am anish",'i love coding']

test1 = r.choice(test)
print('typing speed')
print(test1)
print("")
print("")
time1 = time()
input1 = input("Enter: ")
time2 = time()
print("Speed: ",speed_time(time1,time2,input1),"words/sec")
print("errors count: ", mistake(test1,input1))