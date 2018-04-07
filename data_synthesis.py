import random
import numpy as np
import mpmath as mp


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





def synthesize(n , sthreshold = 0.5, rthreshold = 0.5 , max =32):
    pid = np.arange(0,n ,dtype='int32')

    primes = np.array(prime_generator(n))

    mp_init = np.frompyfunc(mp.fadd, 2, 1)
    empty = np.zeros(n)
    primes = mp_init(primes, empty)

    vector_clock = np.zeros((n, n))

    queue = np.zeros((n, int(64*n), n))

    recv = np.zeros(n, dtype= 'int32')

    vector_clock_m = mp_init(vector_clock , empty)

    evc = np.prod(primes**vector_clock_m, axis = 1)

    events = 0

    dataout = np.reshape( primes , (1,n))
    while mp.log(np.max(evc)) /mp.log(2) <= max*n :

        if np.random.random_sample() > sthreshold :
            selection = np.random.choice(pid, 2, replace=False)

            vector_clock[selection[0]][selection[0]]+=1
            queue[selection[1]][recv[selection[1]]] = vector_clock[selection[0]]
            recv[selection[1]] += 1





        else:
            selection = np.random.choice(pid, 1, replace=False)
            if recv[selection[0]]!=0 and np.random.random_sample() > rthreshold :
                 #print("Before:", vector_clock , recv, queue)
                 vector_clock[selection[0]] += np.clip(queue[selection[0]][0] - vector_clock[selection[0]] , a_min=0 ,a_max =None)
                 recv[selection[0]]-=1
                 queue[selection[0]][0] = np.zeros(n)
                 queue[selection[0]] = np.roll(queue[selection[0]], -1, axis=0)
                 vector_clock[selection[0]][selection[0]] += 1

                 #print("After:", vector_clock , recv , queue)

            else :
                vector_clock[selection[0]][selection[0]] += 1

        vector_clock_m = mp_init(vector_clock, empty)
        evc = np.prod(primes ** vector_clock_m, axis=1)
        events += 1
        #print(np.log(np.max(evc)))
        dataout = np.append(dataout , vector_clock[np.argmax(evc)][np.newaxis,] , axis=0)


    np.savetxt("./Experiment 1/" + str(n)+"-64.out", np.array(dataout))

    return events



def exp2_synthesize(n , sthreshold = 0.5, rthreshold = 0.5 , max = 32 ):
    pid = np.arange(0,n ,dtype='int32')

    primes = np.array(prime_generator(n))

    mp_init = np.frompyfunc(mp.fadd, 2, 1)
    empty = np.zeros(n)
    primes = mp_init(primes, empty)

    vector_clock = np.zeros((n, n))

    queue = np.zeros((n, int(sthreshold*1000*n), n))

    recv = np.zeros(n, dtype= 'int32')

    vector_clock_m = mp_init(vector_clock , empty)

    evc = np.prod(primes**vector_clock_m, axis = 1)

    events = 0

    dataout = np.reshape( primes , (1,n))
    while mp.log(np.max(evc)) /mp.log(2) <= 1000*n and events<=1000:

        if np.random.random_sample() > sthreshold :
            selection = np.random.choice(pid, 2, replace=False)

            vector_clock[selection[0]][selection[0]]+=1
            queue[selection[1]][recv[selection[1]]] = vector_clock[selection[0]]
            recv[selection[1]] += 1





        else:
            selection = np.random.choice(pid, 1, replace=False)
            if recv[selection[0]]!=0 and np.random.random_sample() > rthreshold :
                 #print("Before:", vector_clock , recv, queue)
                 vector_clock[selection[0]] += np.clip(queue[selection[0]][0] - vector_clock[selection[0]] , a_min=0 ,a_max =None)
                 recv[selection[0]]-=1
                 queue[selection[0]][0] = np.zeros(n)
                 queue[selection[0]] = np.roll(queue[selection[0]], -1, axis=0)
                 vector_clock[selection[0]][selection[0]] += 1

                 #print("After:", vector_clock , recv , queue)

            else :
                vector_clock[selection[0]][selection[0]] += 1

        vector_clock_m = mp_init(vector_clock, empty)
        evc = np.prod(primes ** vector_clock_m, axis=1)
        events += 1

        dataout = np.append(dataout , vector_clock[selection[0]][np.newaxis,] , axis=0)


    np.savetxt("./Experiment 2/" + str(n)+"-1000.out", np.array(dataout))

    return events



if __name__ == '__main__':
    # 9223372036854775807
    # 2147483647
    #for i in range(2,100,10):
       print(synthesize(10 ,max = 64))
    #print(exp2_synthesize(10, 0.5, max=32))