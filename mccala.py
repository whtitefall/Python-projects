import random, threading,queue,time,math,multiprocessing,argparse,os,matplotlib
matplotlib.use('Agg')
import numpy.random as rm
import matplotlib.pyplot as plt

import numpy as np
from multiprocessing import Pool,Process
from tqdm import tqdm
import testfunc
import operator
import datetime

def func(x,name):
    if name == "1":
        return testfunc.func[0](x)
    elif name == "2":
        return testfunc.func[1](x)
    elif name == "3":
        return testfunc.func[2](x)
    


def draw(args):

    start = args[0]
    end = args[1]
    funcList = args[2]
    Parray = args [3]
    array = args[4]
    name = args[5]
    N = args[6]
    M = args[7]
    K = args[8]
    K2 = args[9]
    Times = args[10]
    startTime = args[11]

        
    if len(args ) == 12:
        
        
        y = []
        x = np.linspace(start,end,50)

        for i in x :
            y.append(func(i,name))

        plt.clf()
        plt.plot(x, y, '-k')

        plt.plot(np.arange(0.0,1.0000001,1/(len(array)-1)),array, marker='o', linestyle='--')
        plt.plot(np.arange(0.0,1.0000001,1/(len(Parray)-1)),Parray, marker='.')

        ymax = 1

        plt.ylim(0,ymax)


        
        dir = "testResult/"+name+"_"+N+"_"+M+"_"+startTime+"/"
        if not os.path.exists(dir):
            os.makedirs(dir)
            
        plt.title("# Exp: "+str(Times)+", # Iter:"+K+", N: "+N+", M:"+M)

        plt.savefig(dir+K+".png")

        
def draw2 (name,N,M,startTime,RWarray,Times,K):
        plt.figure(2)
    
        plt.plot(RWarray, marker='.')

        maxValue = max(RWarray)
        plt.axhline(maxValue)

        dir = "testResult/"+name+"_"+N+"_"+M+"_"+startTime+"/"
        if not os.path.exists(dir):
            os.makedirs(dir)
            
        #plt.title("# Exp: "+str(Times)+", # Iter:"+K+", N: "+N+", M:"+M)

        plt.title("# Exp: "+str(Times)+", # Iter:"+K+", N: "+N+", M:"+M)

        plt.savefig(dir+"result"+".png")
            


def mccala (position,N,M,name,q,q2,K,K2,selectedCoreInRangeCounter,core,statRange):

    # selectedCoreInRangeCounter = np.zeros(shape=(statRange,))
    #i =  random.randint(0,N*M)
    # core = i/ (N*M)
    #print(casheRW)
    casheRW = 0 
    step = 1/(N*M)
    #print(K)
    for k in range(K):
        #print(k)
        lam = random.uniform(core-1/N,core+1/N)
        
        if lam > 0 and lam < 1:
            response = rm.binomial(1,func(lam,name),1)[0]
            if response == 1:
                casheRW += 1 
                if lam < core :
                    core = core - step
                    #i-= 1
                else:
                    core = core + step
                    #i+= 1
        
        #print(k,K2)
        if k > K2 :
            #print(statRange)
            selectedCoreInRangeCounter[int(core*statRange)] += 1
        
 
        #selectedCoreInRangeCounter[int(core*statRange)] += 1
    #print(2222222222222222)
    #print(casheRW)
    q2.put(casheRW)
    #print(1)
    q.put([selectedCoreInRangeCounter,core])

def R(i,N,M,func):

    
    #print(testfunc.L([i/(M*N),N,func]))
    return (testfunc.L([(M+i)/(M*N),N,func] )/testfunc.L([i/(M*N),N,func]) )


def calP(N,M,func,step):
    P = np.zeros(shape=(N*M+1,))
    P[0] = 100
 
    pFinal = np.zeros(shape=(step+1,))

    ran = int(N*M/step)

    
    
    for i in range(1,M*N+1):
        #print(R(i,N,M,func))
        P[i] = P[i-1]*R(i,N,M,func)
        pFinal[int(i//ran)] += P[i]
        

    
    
    return pFinal/sum(pFinal)



if __name__ == '__main__':
    
    start = time.time()
    step = 50 
    
    q = multiprocessing.Manager().Queue()
    q2 = multiprocessing.Manager().Queue()
    parser = argparse.ArgumentParser()
    parser.add_argument("func",help = "function picked")
    parser.add_argument("N",help = "search range")
    parser.add_argument("M",help = "density")
    parser.add_argument("K",help = "K")
    parser.add_argument("cacheSize",help = "cacheSize")
    parser.add_argument("Threads",help = "num of threads")

    args = parser.parse_args()
    L = multiprocessing.cpu_count()
    
    startTime = str(time.time())
    NumOfThread = int(args.Threads)
    threads = []
    RWarray = [] 
    N = int(args.N)
    M = int(args.M)
    K = int(args.K)
    cacheSize = int(args.cacheSize)
    statRange = 50
    cacheStep = int(K//cacheSize)
    #print(cacheStep)

    # initial

    
    
    for i in range(NumOfThread):
        q.put([np.zeros(shape=(statRange,)),random.randint(0,N*M)/(M*N)])
    q2.put(0)
    #print(q2.get())
    
    
    for k in tqdm((range(0,K+1,cacheStep))):
        
        pool = Pool(L)
        Pdivde = calP(N,M,testfunc.func[int(args.func)-1],step)
        sumResultArr = np.zeros(shape=(statRange,))
        for i in range(NumOfThread):
            #print(q.qsize())
            [selectedCoreInRangeCounter,core] = q.get()
            #casheRW = q2.get()
            #print(casheRW)
           # print(int(core*statRange))
            sumResultArr = map(operator.add, sumResultArr, selectedCoreInRangeCounter)
            
            pool.apply_async(func = mccala,args = (i,N,M,args.func,q,q2,k,0,np.zeros(shape=(statRange,)), core,statRange))
        #print(q2.qsize())
        #RWarray.append(q2.get()/cacheSize)
        #print(k,cacheStep)
        if k-cacheStep>0:
            #print(1111111)
            #print(list(sumResultArr))
            sumResultArr = list(map(lambda x:x/(NumOfThread*(k)), sumResultArr))
            #print(sumResultArr)
            arguments = (0,1,testfunc.func,Pdivde,sumResultArr,args.func,str(N),str(M),str(k-cacheStep),str(0),int(args.Threads),startTime)
            
            draw(arguments)
        countRW = 0 
        while not q2.empty():
            countRW+= q2.get()
        #print(countRW,"origin")
        if k != 0 :
            
            countRW = countRW/(NumOfThread*k)
        elif k == 0 :
            countRW = countRW/NumOfThread
        #print(countRW,"test")
        RWarray.append(countRW)
        
            
            
        
        pool.close()
        pool.join()
    #print(len(RWarray))
    #print("DONE")
    #print(q.qsize())
    #print(q.get())
    
    while not q.empty():
        [selectedCoreInRangeCounter,core] = q.get()
        sumResultArr = map(operator.add, sumResultArr, selectedCoreInRangeCounter)
    sumResultArr = list(map(lambda x:x/(NumOfThread*(K)), sumResultArr))
    #print("DONE2")
    #print(sumResultArr)

    Pdivde = calP(N,M,testfunc.func[int(args.func)-1],step)
    arguments = (0,1,testfunc.func,Pdivde,sumResultArr,args.func,str(N),str(M),str(k-cacheStep),str(0),int(args.Threads),startTime)

    #print(1111111)
    
    draw(arguments)
    
    #print(RWarray)

    

    draw2(args.func,str(N),str(M),startTime,RWarray,int(args.Threads),str(K))



