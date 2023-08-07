import numpy as np
import matplotlib.pyplot as plt
import sys

FILE = sys.argv[-1]

def main():
    with open(FILE) as f:
        t, v = np.loadtxt(f, delimiter=',', dtype='string', comments='#', usecols=(3,4), unpack=True)

    for i in range(10):
	    plt.plot(t[1000*(i-1):1000*(i)], v[1000*(i-1):1000*(i)])
	    plt.xlabel('time (s)')
	    plt.ylabel('voltage (V)')
	    plt.show()
	    return 0

if __name__ == '__main__':
	main()