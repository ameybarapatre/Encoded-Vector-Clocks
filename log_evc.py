import mpmath as mp
from mpmath import *
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import re
pattern = re.compile("[0-9]+.[0]+")


mp.dps = 800
mp.pretty = True

def positive_rate(n ,r):
    file = "./Experiment 2/" + str(n)+"-" + str(r)+ ".out"
    data = np.loadtxt(file)


    mp_init = np.frompyfunc(mp.fadd ,2,1)
    empty = np.zeros(n)
    primes = mp_init(data[0] , empty)

    event_vectors = mp_init(data[1:] ,  empty)



    evc = np.prod(primes**event_vectors , axis =1)
    logevc = [mp.log(evc[x])  for x in range(0 ,len(evc))]


    idx = [x for x in range(0, len(evc))]
    pairs = list(permutations(idx , 2))


    true_positives = 0
    positives = 0
    li=[]
    for pair in pairs:


        if np.min(event_vectors[pair[0]] - event_vectors[pair[1]])>=0:
            true_positives+=1

            if logevc[pair[0]]>logevc[pair[1]]:

                #print(event_vectors[pair[0]], event_vectors[pair[1]])
                #print(logevc[pair[0]] - logevc[pair[1]])

                v =mp.exp(logevc[pair[0]] - logevc[pair[1]])

                # if (float(str(v)) - int(float(str(v)))) == 0.0:
                if bool(pattern.match(str(v))):
                    positives += 1

                    #print(int(float(str(v))))

    print(true_positives, true_positives- positives)


def negative_rate(n ,r):
    file = "./Experiment 2/" + str(n)+"-" + str(r)+ ".out"
    data = np.loadtxt(file)


    mp_init = np.frompyfunc(mp.fadd ,2,1)
    empty = np.zeros(n)
    primes = mp_init(data[0] , empty)

    event_vectors = mp_init(data[1:] ,  empty)



    evc = np.prod(primes**event_vectors , axis =1)
    logevc = [mp.log(evc[x])  for x in range(0 ,len(evc))]


    idx = [x for x in range(0, len(evc))]
    pairs = list(permutations(idx , 2))


    true_negatives = 0
    false_positives = 0
    li=[]
    for pair in pairs:


        if np.min(event_vectors[pair[0]] - event_vectors[pair[1]])<0:
            true_negatives+=1

            if logevc[pair[0]]>logevc[pair[1]]:

                #print(event_vectors[pair[0]], event_vectors[pair[1]])
                #print(logevc[pair[0]] - logevc[pair[1]])

                v =mp.exp(logevc[pair[0]] - logevc[pair[1]])

                #print(str(v))

                #if (float(str(v)) - int(float(str(v)))) == 0.0:
                if bool(pattern.match(str(v))):
                    false_positives += 1

                    #print(int(float(str(v))))

    print(true_negatives, false_positives)



positive_rate(10,100)
negative_rate(10,100)
print("Next:")

positive_rate(10,200)
negative_rate(10,200)
print("Next:")


positive_rate(10,300)
negative_rate(10,300)
print("Next:")


positive_rate(10,500)
negative_rate(10,500)
print("Next:")


positive_rate(10,800)
negative_rate(10,800)
print("Next:")


positive_rate(10,1000)
negative_rate(10,1000)
print("Next:")


positive_rate(10,1200)
negative_rate(10,1200)
print("Next:")


