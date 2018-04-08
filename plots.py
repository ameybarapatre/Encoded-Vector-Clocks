import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp
def plots():
    for i in range(2,100,10):

        file = "./Experiment 1/" + str(i) +"-32.out"
        data = np.loadtxt(file)
        primes = data[0]
        event_vectors = data[1:]
        mp_init = np.frompyfunc(mp.fadd, 2, 1)
        empty = np.zeros(i)
        primes = mp_init(primes, empty)

        event_vectors = mp_init(event_vectors , empty)

        evc = np.prod(primes**event_vectors , axis = 1)

        mp_log = np.frompyfunc(mp.log, 1, 1)

        bits = mp_log(evc) / mp.log(2)

        mp_ceil = np.frompyfunc(mp.ceil, 1, 1)

        bits = mp_ceil(bits)
        print(bits)
        plt.plot(bits)
        plt.title(str(i)+" Processes , 32 bit")
        plt.savefig("./Plots/"+str(i)+"-32.png")
        plt.clf()



def proc_plot():
    x = [i for i in range(2,100,10)]
    y=[]

    for i in range(2,100,10):

        file = "./Experiment 1/" + str(i) +"-32.out"
        data = np.loadtxt(file)
        primes = data[0]
        event_vectors = data[1:]
        y.append(len(event_vectors))

    plt.plot(x,y)
    plt.title("32 Bit")
    plt.savefig("32bit.png")
    plt.clf()



def prob_plot():
    x = [0.0 , 0.1,0.2,0.3,0.4, 0.5 , 0.6 , 0.7 , 0.8, 0.9,1.0]
    y=[]

    for i in x:
        print(i)
        file = "./Experiment 1A/10-" + str(i) +".out"
        data = np.loadtxt(file)
        primes = data[0]
        event_vectors = data[1:]
        y.append(len(event_vectors))

    plt.plot(x,y)
    plt.title("Probability vs Number of Events")
    plt.savefig("64prob.png")
    plt.clf()


if __name__ == '__main__':
    #prob_plot()
    proc_plot()
    #plots()