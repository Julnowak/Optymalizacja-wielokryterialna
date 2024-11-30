import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import Callable,List
def topsis(decision_matrix : np.ndarray, bounds : np.ndarray, weights : np.ndarray,min_max_criterial_funct : List[Callable[[np.ndarray],float]],scorling_metric : Callable[[np.ndarray,np.ndarray],float], normalization_norm : Callable[[np.ndarray],float]):
    decision_matrix_copy = decision_matrix.copy()
    decision_matrix = decision_matrix[:,2:]
    bounds = bounds[:,2:]
    #filter
    lst = []
    lst2 = []
    for i in range(len(decision_matrix)):
        if ((bounds[0]<=decision_matrix[i,:]).all() and (decision_matrix[i,:]<=bounds[1]).all()):
            lst.append(list(decision_matrix[i,:]))
            lst2.append(list(decision_matrix_copy[i,:]))
    decision_matrix = np.array(lst,dtype=float)
    decision_matrix_copy = np.array(lst2,dtype=float)
    #normalization
    norms = [normalization_norm(decision_matrix[:,i]) for i in range(len(dec_matrix[0]))]
    for i in range(len(dec_matrix[0])):
        decision_matrix[:,i] = (weights[i]/norms[i])*decision_matrix[:,i]
    #print(decision_matrix)# heh Xd
    anty = [0 for i in range(len(decision_matrix[0]))]
    idealny = [0 for i in range(len(decision_matrix[0]))]
    for i in range(len(decision_matrix[0])):
        if min_max_criterial_funct[i] == np.min:
            anty[i] = np.max(decision_matrix[:,i])
            idealny[i] = np.min(decision_matrix[:,i])
        else:
            anty[i] = np.min(decision_matrix[:,i])
            idealny[i] = np.max(decision_matrix[:,i])
    # obliczanie odległości i wspolczynnyki skorlingowe
    scorling_vals = [(di_ := scorling_metric(idealny,decision_matrix[i]))/(di_ + scorling_metric(anty,decision_matrix[i])) for i in range(len(decision_matrix))]
    # ranking
    lst_temp = list(zip(*list(decision_matrix_copy.T),scorling_vals))
    lst_temp.sort(key=lambda x: x[-1])
    ranking = np.array(lst_temp,dtype=int)
    ranking = ranking[:,:-1]
    if len(decision_matrix[0]) == 3:
        fig=plt.figure(figsize=(3,3))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(decision_matrix[:,0],decision_matrix[:,1],decision_matrix[:,2],marker='+')
        ax.scatter(anty[0],anty[1],anty[2],marker='o')
        ax.scatter(idealny[0],idealny[1],idealny[2],marker='*')
        plt.show()
    return ranking
    pass

def niezdominiwane(decision_matrix : np.ndarray, bounds : np.ndarray,min_max_criterial_funct : List[Callable[[np.ndarray],float]]):
    decision_matrix_copy = decision_matrix.copy()
    decision_matrix = decision_matrix[:,2:]
    bounds = bounds[:,2:]
    #filter
    lst = []
    lst2 = []
    for i in range(len(decision_matrix)):
        if ((bounds[0]<=decision_matrix[i,:]).all() and (decision_matrix[i,:]<=bounds[1]).all()):
            lst.append(list(decision_matrix[i,:]))
            lst2.append(list(decision_matrix_copy[i,:]))
    decision_matrix = np.array(lst)
    decision_matrix_copy = np.array(lst2)
    lst = []
    for i in range(len(decision_matrix)):
        dominated = True
        for j in range(len(decision_matrix)):
            if i == j or not dominated:
                continue
            temp = np.array([decision_matrix[i,k]<decision_matrix[j,k] if min_max_criterial_funct[k] == np.min else decision_matrix[i,k]>decision_matrix[j,k]  for k in range(len(decision_matrix[0]))])
            if temp.any():
                dominated = False
        if not dominated:
            lst.append(list(decision_matrix_copy[i]))
    return np.array(lst)


if __name__=='__main__':
    dec_matrix = np.array([
        [700,2,6],
        [250,2,4],
        [1200,6,9],
        [880,4,9],
        [450,3,8],
        [1500,2,3]
    ],dtype=float)
    weights = np.array([0.45,0.3,0.25])
    min_max_crit = [np.min,np.max,np.max]
    norm = lambda x: np.sqrt(np.sum(x*x))
    #norm = lambda x: np.max(np.abs(x))
    metric = lambda x,y: norm(x-y)
    A = np.array([[1,1,700,  2, 6],
     [1,1, 250,  2, 4],
     [1,1, 1200, 6, 9],
     [1,1, 880,  4, 9],
     [1,1, 450,  3, 8],
     [1,1, 1500, 2, 3]])
    K = np.array([[1, 1, 200, 1, 3],
    [1, 1, 1200, 7, 10]])
    metric = lambda x,y: np.max(np.abs(x-y))
    print(topsis(A,K,weights,min_max_crit,metric,norm))
    print(niezdominiwane(A,K,min_max_crit))