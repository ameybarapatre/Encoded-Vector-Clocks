import random
import numpy as np



def prime_generator(n):
    count = 1
    primes = []
    primes.append(2)
    i = 3
    flag = False
    while count!=n :

        for j in range(2,i):
            if i%j == 0 :
                flag = True

        if flag==False:
            count+=1
            primes.append(i)

        i+=1
        flag = False
    return primes


def synthesize(n , threshold = 0.5 , max =2147483647 ):
    pid = np.arange(0,n ,dtype='int32')

    primes = np.array(prime_generator(n))

    vector_clock = np.zeros((n, n))

    queue = np.zeros((n, 64, n))

    recv = np.zeros(n, dtype= 'int32')

    evc = np.prod(primes**vector_clock, axis = 1)

    events = 0

    while np.max(evc) <= max :

        if np.random.random_sample() > threshold :
            selection = np.random.choice(pid, 2, replace=False)

            vector_clock[selection[0]][selection[0]]+=1
            queue[selection[1]][recv[selection[1]]] = vector_clock[selection[0]]
            recv[selection[1]] += 1




        else:
            selection = np.random.choice(pid, 1, replace=False)
            if recv[selection[0]]!=0 and np.random.random_sample() > threshold :
                 #print("Before:", vector_clock , recv, queue)
                 vector_clock[selection[0]] += np.clip(queue[selection[0]][0] - vector_clock[selection[0]] , a_min=0 ,a_max =None)
                 recv[selection[0]]-=1
                 queue[selection[0]][0] = np.zeros(n)
                 queue[selection[0]] = np.roll(queue[selection[0]], -1, axis=0)
                 vector_clock[selection[0]][selection[0]] += 1
                 #print("After:", vector_clock , recv , queue)

            else :
                vector_clock[selection[0]][selection[0]] += 1

        evc = np.prod(primes**vector_clock , axis = 1)
        events+=1


    return np.max(vector_clock[np.argmax(evc)]),  np.sum(vector_clock[np.argmax(evc)]) , events

if __name__ == '__main__':
    # 9223372036854775807
    # 2147483647
    for i in range(2,200):
        print(synthesize(i,0.5 ,max = 9223372036854775807))