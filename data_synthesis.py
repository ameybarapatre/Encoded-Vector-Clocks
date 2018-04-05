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





def synthesize(n , sthreshold = 0.5, rthreshold = 0.5 , max =2147483647 ):
    pid = np.arange(0,n ,dtype='int32')

    primes = np.array(prime_generator(n))

    vector_clock = np.zeros((n, n))

    queue = np.zeros((n, int(sthreshold*64*n), n))

    recv = np.zeros(n, dtype= 'int32')

    evc = np.prod(primes**vector_clock, axis = 1).astype('uint64')

    events = 0

    dataout = np.reshape( primes , (1,n))
    while np.max(evc) <= max and events < 1000 :

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

        evc = np.prod(primes**vector_clock , axis = 1  , dtype = "uint64")
        events += 1
        #print(np.log(np.max(evc)))
        dataout = np.append(dataout , vector_clock[np.argmax(evc)][np.newaxis,] , axis=0)


    np.savetxt("./64/" + str(n)+".out", np.array(dataout, dtype = 'int64'))

    return np.max(vector_clock[np.argmax(evc)]),  np.sum(vector_clock[np.argmax(evc)]) , events , evc[np.argmax(evc)]


















def exp2_synthesize(n , sthreshold = 0.5, rthreshold = 0.5 , max =2147483647 ):
    pid = np.arange(0,n ,dtype='int32')

    primes = np.array(prime_generator(n))

    vector_clock = np.zeros((n, n))

    queue = np.zeros((n, int(sthreshold*1000*n), n))

    recv = np.zeros(n, dtype= 'int32')

    evc = np.prod(primes**vector_clock, axis = 1).astype('uint64')

    events = 0

    dataout = np.reshape( primes , (1,n))
    while np.log(np.max(evc)) <= max and events < 1200 :

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

        evc = np.prod(primes**vector_clock , axis = 1  , dtype = "uint64")
        events += 1
        #print(np.log(np.max(evc)))
        dataout = np.append(dataout , vector_clock[selection[0]][np.newaxis,] , axis=0)


    np.savetxt("./Experiment 2/" + str(n)+"-1200.out", np.array(dataout, dtype = 'int64'))

    return np.max(vector_clock[np.argmax(evc)]),  np.sum(vector_clock[np.argmax(evc)]) , events , evc[np.argmax(evc)]



if __name__ == '__main__':
    # 9223372036854775807
    # 2147483647
    for i in range(2,200,10):
        print(synthesize(i,0.5 ,max = 9223372036854775807))
    #print(exp2_synthesize(10, 0.5, max=2147483647))