import numpy as np
import matplotlib.pyplot as plt

def plots():
    for i in range(2,200,10):

        file = "./64/" + str(i) +".out"
        data = np.loadtxt(file)
        primes = data[0]
        event_vectors = data[1:]

        evc = np.prod(primes**event_vectors , axis = 1 , dtype= 'int64')

        print(evc)

        bits = [int(x).bit_length() for x in evc]
        print(bits)

        plt.plot(bits)
        plt.title(str(i)+" Processes , 64 bit")
        plt.savefig("./Plots/"+str(i)+"-64.png")
        plt.clf()

def proc_plot():
    x = [i for i in range(2,200,10)]
    y=[]

    for i in range(2,200,10):

        file = "./64/" + str(i) +".out"
        data = np.loadtxt(file)
        primes = data[0]
        event_vectors = data[1:]
        y.append(len(event_vectors))

    plt.plot(x,y)
    plt.title("64 Bit")
    plt.savefig("64bit.png")
    plt.clf()

if __name__ == '__main__':
    proc_plot()
    plots()