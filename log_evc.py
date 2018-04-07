import mpmath as mp
from mpmath import *
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import re
pattern = re.compile("([0-9])+\.([0])+")


mp.dps = 100
mp.pretty = True

def positive_rate(n ,r):
    file = "./Experiment 2/" + str(n)+"-1000.out"
    data = np.loadtxt(file)


    mp_init = np.frompyfunc(mp.fadd ,2,1)
    empty = np.zeros(n)
    primes = mp_init(data[0] , empty)

    event_vectors = mp_init(data[1:r] ,  empty)



    evc = np.prod(primes**event_vectors , axis =1)

    mp_log = np.frompyfunc(mp.log, 1, 1)

    logevc = mp_log(evc)


    idx = [x for x in range(0, len(evc))]
    pairs = list(permutations(idx , 2))


    true_positives = 0
    positives = 0
    li=[]
    for pair in pairs:


        if np.min(event_vectors[pair[0]] - event_vectors[pair[1]])>=0:
            true_positives+=1

            if logevc[pair[0]]>logevc[pair[1]]:

                v =mp.exp(logevc[pair[0]] - logevc[pair[1]])

                if bool(pattern.match(str(v))) and len(pattern.match(str(v)).group(0)) == len(str(v)):
                    positives += 1


    print(true_positives, true_positives- positives)


def negative_rate(n ,r):
    file = "./Experiment 2/"+str(n)+"-1000.out"
    data = np.loadtxt(file)


    mp_init = np.frompyfunc(mp.fadd ,2,1)
    empty = np.zeros(n)
    primes = mp_init(data[0] , empty)

    event_vectors = mp_init(data[1:r] ,  empty)



    evc = np.prod(primes**event_vectors , axis =1)
    mp_log = np.frompyfunc(mp.log, 1, 1)

    logevc = mp_log(evc)

    idx = [x for x in range(0, len(evc))]
    pairs = list(permutations(idx , 2))


    true_negatives = 0
    false_positives = 0
    li=[]
    for pair in pairs:


        if np.min(event_vectors[pair[0]] - event_vectors[pair[1]])<0 and np.max(event_vectors[pair[0]] - event_vectors[pair[1]])>0:

            true_negatives+=1

            if logevc[pair[0]]>logevc[pair[1]]:

                v =mp.exp(logevc[pair[0]] - logevc[pair[1]])

                if bool(pattern.match(str(v))) and len(pattern.match(str(v)).group(0)) == len(str(v)):

                    false_positives += 1


            elif logevc[pair[0]]<logevc[pair[1]]:

                v =mp.exp(logevc[pair[1]] - logevc[pair[0]])

                if bool(pattern.match(str(v))) and len(pattern.match(str(v)).group(0)) == len(str(v)):

                    false_positives += 1


    print(true_negatives, false_positives)



positive_rate(50,100)

negative_rate(50,100)