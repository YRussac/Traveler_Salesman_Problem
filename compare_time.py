# Importation

import numpy as np
import os
import time
from visualization import heatmap
import TSP_OpenCL_Paralellization as opencl_file
import TSP_Multiprocessing_Parallelization as multiprocessing_file
import TSP_No_Parallelization as nopar
import TSP_Threading_Parallelization as threading_file
import matplotlib.pyplot as plt

os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
os.environ['PYOPENCL_CTX'] = '1'

# setting examples

np.random.seed(6)
rangeVilles = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
rho_exp = 0.05
d_exp = 3
rangeN_exp = [500, 1000, 3000, 5000, 8000, 12000, 16000, 22000, 30000, 40000, 50000]
alpha_exp = 0.99
init_exp = 1


# Comparison script
if __name__ == '__main__':

    timeNopar = []
    timeThread = []
    timeProcess = []
    timeGPU = []

    ticks = []

    f = open('saveres.txt', 'w')

    for NVilles, N_exp in zip(rangeVilles, rangeN_exp):
        ticks.append("Villes={}\n Sim={}".format(NVilles, N_exp))
        print('Number of cities: {}'.format(NVilles))

        # generate distance matrix
        dMat = np.matrix(np.random.randint(1, NVilles, size=(NVilles, NVilles)))
        dMat = (dMat + dMat.T)/2
        for i in range(NVilles):
            dMat[i, i] = 0

        # No paralellization
        t = nopar.TSP(rho=rho_exp, d=d_exp, N=N_exp,
                      distanceMatrix=dMat, alpha=alpha_exp, init=init_exp, timer=True)
        timeNopar.append(t)
        f.write('{}; {}; {}\n'.format(NVilles, N_exp, t))

        # Threading parallelization
        t = threading_file.TSP_thread_parallel_partial(rho=rho_exp, d=d_exp, N=N_exp,
                                                       distanceMatrix=dMat, alpha=alpha_exp,
                                                       init=init_exp, timer=True)
        timeThread.append(t)
        f.write('{}; {}; {}\n'.format(NVilles, N_exp, t))

        # Multiprocessing parallelization
        t = multiprocessing_file.TSP_process_parallel(rho=rho_exp, d=d_exp, N=N_exp,
                                                      distanceMatrix=dMat, alpha=alpha_exp,
                                                      init=init_exp, timer=True)
        timeProcess.append(t)
        f.write('{}; {}; {}\n'.format(NVilles, N_exp, t))

        # GPU parallelization
        t = opencl_file.TSP_GPU(rho=rho_exp, d=d_exp, N=N_exp, distanceMatrix=dMat,
                                alpha=alpha_exp, init=init_exp, timer=True)
        timeGPU.append(t)
        f.write('{}; {}; {}\n'.format(NVilles, N_exp, t))

    f.close()
    plt.figure(figsize=(10,10))
    plt.plot(rangeVilles, timeNopar, 'r--', rangeVilles, timeThread, 'bs',
             rangeVilles, timeProcess, 'g^', rangeVilles, timeGPU)
    plt.title('Execution time of one iteration of algorithms')
    plt.xticks(rangeVilles, ticks)
    plt.xlabel('Parameters')
    plt.ylabel('Time (s)')
    plt.legend(['No paralellization', 'Multi-threading', 'Multi-processing', 'GPU'], loc='best')
    plt.show()
