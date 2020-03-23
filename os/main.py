import math
from collections import defaultdict,OrderedDict
import copy

class Schedule:
    def __init__(self, p_list):
        self.p_list = p_list
        self.n = len(p_list)
        self.p_list = dict(sorted(self.p_list.items(), key = lambda x: x[1][0]))
    def FCFS(self):
        
        order = ""
        time = 0
        for item in self.p_list.items():
            
            self.p_list[item[0]][3] = time - item[1][0] if time > item[1][0] else 0
            self.p_list[item[0]][4] = time - item[1][0] if time > item[1][0] else 0
            order += str(time) + " (" + item[0]+") "
            if time <= item[1][0]:
                time = item[1][0]+ item[1][1]
            else :
                time += item[1][1]
            order += str(time)+"| "
            self.p_list[item[0]][2] = time - item[1][0]
        self.evaluate(self.p_list.items(), "FCFS",order)
       
    
    def SJF(self):
        p = self.p_list
        items = p.items()
        items = sorted(items, key = lambda item: (item[1][0], item[1][1]))
        items = copy.deepcopy(items)
        time = 0
        order = " "
        for item in items:
            
            item[1][3] = time - item[1][0] if time > item[1][0] else 0
            item[1][4] = time - item[1][0] if time > item[1][0] else 0
            order +="[" +str(time) + " (" + item[0]+") "

            if time < item[1][0]:
                time = item[1][0]
            time +=item[1][1]
            order += str(time)+"] "
            item[1][2] = time - item[1][0]
        self.evaluate(items, "SJF", order)
    def SRTF(self):
        items = self.p_list.items()
        items = sorted(items, key = lambda item: (item[1][0], item[1][1]))
        items = copy.deepcopy(items)
        reserved = []
        time = 0
        complete = 0
        rt = [item[1][1] for item in items]
        minn = 9999
        check = False
        order = ""
        pre = ""
        for item in items:
            item[1][3] = 9999
        while complete != self.n:
            for i,item in enumerate(items):
                
                if item[1][0] <= time and rt[i] < minn and rt[i]>0:
                    print(item[1][0])
                    minn = rt[i]
                    short = i
                    check = True
            if check == False:
                order +="0"
                time +=1
                continue
            rt[short]-=1
            minn = rt[short]
            order += items[short][0][1]
            if items[short][1][3] > time:
                items[short][1][3] = time - items[short][1][0]
            if minn == 0 :
                minn = 999
            if rt[short] == 0:
                complete +=1
                check = False
                fint = time+1
                items[short][1][4] = fint - items[short][1][0] - items[short][1][1]
                items[short][1][2] = items[short][1][4] + items[short][1][1]
                if items[short][1][4] < 0:
                    items[short][1][4] = 0
            time +=1

        self.evaluate(items, "SRTF", order)
        
    
    def RR(self,tq):
        
        items = self.p_list.items()
        items = sorted(items, key = lambda item: item[1][0])
        items = copy.deepcopy(list(items))
        rt = [item[1][1] for item in items]
        complete = 0
        queue = [items[0]]
        time = 0
        order = ""
        for item in items:
            item[1][3] = 999
        
        while complete != self.n or len(queue) != 0 :
            t=0
            if len(queue)==0:
                time+=1
            else: 
                item = queue[0]
                
                t= tq if item[1][1] > tq else item[1][1]
                time += t
                item[1][1]-=t
                if item[1][1] ==0:
                    complete+=1
                if item[1][3] > (time-t):
                    item[1][3] = time-t
                if item[1][1]==0:
                    item[1][4] = time - t - item[1][0] - item[1][1]
                    item[1][2] = item[1][4] + item[1][1]
                    if item[1][4] < 0 :
                        item[1][4] = 0
                order += "["+str(time-t)+" "+ item[0] +" "+ str(time)+"] "
            for item in items:
                if item[1][0] <=time and item not in queue and item[1][1] !=0:
                    queue.append(item)

            if len(queue) != 0: queue.pop(0)
            if item[1][1] != 0:
                # queue.pop(0)
                queue.append(item)
            
        self.evaluate(items, "RR",order)
            
    def evaluate(self, items, name,order):
        print("Phương pháp "+name+" : ")
        if name=="SRTF":
            order = self.preprocessOrder(order)
        print("Thứ tự thực hiện: "+order)
        print("AVG Response time: "+ str(sum(map(float, [item[1][3] for item in items]))/self.n))
        print("AVG Waiting time: "+ str(sum(map(float, [item[1][4] for item in items]))/self.n))
        print("AVG Turnaround time: "+ str(sum(map(float, [item[1][2] for item in items]))/self.n))
        # print(items)
        print("end")
    def preprocessOrder(self, order):
        new_order = " "
        time = 0
        index = 0
        while index < len(order):
            item = order[index]
            t = 0
            for index_j, item_j in enumerate(order[index:]):
                if item_j != item:
                    break
                else : t+=1
            if item =="0":
                time +=t
            else : 
                new_order += "["+str(time) + " p"+item +" "+str(time+t)+"]"+" "
                time+=t
            index +=t
        return new_order





if __name__=="__main__":
    print("Số lượng tiến trình: ")
    n = int(input())
    p_list = defaultdict(lambda: [0,0,0,0,0])     # 0 : arrival time; 1 : burst time; 2: turnaround time; 3: response time; 4: waiting time
    print("arrival time: ")
    for i in range(n):
        arrival_time = int(input("P{0}: ".format(i+1)))
        p_list["p"+str(i+1)][0] = arrival_time
    print("burst time: ")
    for i in range(n):
        burst_time = int(input("P{0}: ".format(i+1)))
        p_list["p"+str(i+1)][1] = burst_time
    
    exitt = False
    model = Schedule(p_list)
    tq = 1
    

    while exitt == False:
        algo = input("Chọn thuật toán: FSFC (key: 1), SJF (key: 2), SRTF (key: 3), RR(4): ")
        if algo == "1":
            model.FCFS()
        elif algo=='2':
            model.SJF()
        elif algo=="3":
            model.SRTF()
        elif algo =="4":
            tq = int(input("TIME QUANTUM: "))
            model.RR(tq)
        else:
            print("Chọn lại thuật toán!")
        is_exit = input("Có muốn thoát không?(Yes: Y/ No: anykey) " )
        if is_exit =="Y":
            exitt = True
        

