# Use: ./partition.py flag algorithm inputfile
# Going to have to include a makefile
import sys
import random
import math
n = 100

MAX_ITER = 25000
MAX_VAL = 10**12
class MaxHeap:
    def __init__(self, arr=None):
        self.heap = arr[:] if arr else []
        if self.heap:
            self.build_heap()

    def build_heap(self):
        n = len(self.heap)
        for i in range((n // 2) - 1, -1, -1):
            self._sift_down(i)

    def insert(self, value):
        heap = self.heap
        heap.append(value)
        i = len(heap) - 1

        while i > 0:
            p = (i - 1) // 2
            if heap[p] >= heap[i]:
                break
            heap[p], heap[i] = heap[i], heap[p]
            i = p

    def extract_max(self):
        heap = self.heap
        if not heap:
            raise IndexError("extract_max from empty heap")

        if len(heap) == 1:
            return heap.pop()

        max_val = heap[0]
        heap[0] = heap.pop()
        self._sift_down(0)
        return max_val

    def _sift_down(self, i):
        heap = self.heap
        n = len(heap)

        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            largest = i

            if left < n and heap[left] > heap[largest]:
                largest = left
            if right < n and heap[right] > heap[largest]:
                largest = right

            if largest == i:
                break

            heap[i], heap[largest] = heap[largest], heap[i]
            i = largest

    def __len__(self):
        return len(self.heap)
    


def KK(A):
    A_new = MaxHeap(A)
    while len(A_new.heap) > 1:
        a = A_new.extract_max()
        b = A_new.extract_max()
        A_new.insert(a - b)
    return A_new.extract_max()

def random_sol(n): #random standard solution
    S = []
    for i in range(n):
        val = random.choice((-1, 1))
        S.insert(i, val)
    return S

def random_prepar_sol(n): #random prepartition solution
    P = []
    for i in range(n):
        val = random.choice(range(1, n+1))
        P.insert(i, val)
    return P

def random_move(S):
    #randomly move from S to a neighbor (for standard solution S)
    N = S.copy()
    i = random.randint(0, n-1)
    j = i
    while j == i:
        j = random.randint(0,n-1)
    N[i] = -(N[i])
    
    rand_val = random.random()
    if rand_val < 0.5:
        N[j] = -N[j]

    return N

def random_prepar_move(P):
    #randomly move from P to a neighbor (for prepartitioned solution P)
    N = P.copy()
    i = random.randint(0, n-1) #indices are 0 to n-1
    j = random.randint(1, n) #VALUES are 1 to n
    while P[i] == j:
        j = random.randint(1, n)
    N[i] = j
    return N

def prepar_to_std(A, P): 
    #given a prepartitioned solution P and the original A, return residue
    A_new = [0 for _ in range(n)]
    for i in range(0, n):
        p_i = P[i]
        A_new[p_i - 1] += A[i]
    
    return KK(A_new)

def std_residue(S, A):
    #find the residue from a standard solution S
    residue = 0
    for i in range(len(A)):
        residue += S[i]*A[i]
    return abs(residue)

def repeated_random(A):
    #S is an initial random solution
    S = random_sol(len(A))
    for i in range(MAX_ITER):
        S_new = random_sol(len(A))
        if std_residue(S_new,A) < std_residue(S,A):
            S = S_new
    return S

def hill_climbing(A):
    S = random_sol(len(A))
    for i in range(MAX_ITER):
        neighbor = random_move(S)
        if std_residue(neighbor,A) < std_residue(S,A):
            S = neighbor
    return S

def simulated_annealing(A):
    S = random_sol(len(A))
    S_dprime = S.copy()
    for i in range(MAX_ITER):
        neighbor = random_move(S)
        T_iter = (10**10)*(0.8)**(i/300)
        n_res = std_residue(neighbor,A)
        s_res = std_residue(S,A)
        
        if n_res < s_res:
            S = neighbor
        else: 
            prob = math.exp(-(n_res - s_res)/T_iter)
            rand = random.random()
            if rand < prob:
                S = neighbor
        
        if std_residue(S,A) < std_residue(S_dprime,A):
            S_dprime = S
    
    return S_dprime

def prepar_repeated_rand(A):
    #P is an initial prepartitioned random solution
    P = random_prepar_sol(len(A))
    for i in range(MAX_ITER):
        P_new = random_prepar_sol(len(A))
        if prepar_to_std(A, P_new) < prepar_to_std(A, P):
            P = P_new
    return P

def prepar_hill_climbing(A):
    P = random_prepar_sol(len(A))
    curr_res = prepar_to_std(A, P)

    for _ in range(MAX_ITER):
        neighbor = random_prepar_move(P)
        neigh_res = prepar_to_std(A, neighbor)
        if neigh_res < curr_res:
            P = neighbor
            curr_res = neigh_res
    return P

def prepar_simulated_annealing(A):
    P = random_prepar_sol(len(A))
    curr_res = prepar_to_std(A, P)
    P_best = P.copy()
    best_res = curr_res

    for i in range(MAX_ITER):
        neighbor = random_prepar_move(P)
        neigh_res = prepar_to_std(A, neighbor)
        T_iter = (10**10) * (0.8)**(i / 300)

        if neigh_res < curr_res:
            P = neighbor
            curr_res = neigh_res
        else:
            prob = math.exp(-(neigh_res - curr_res) / T_iter)
            if random.random() < prob:
                P = neighbor
                curr_res = neigh_res

        if curr_res < best_res:
            P_best = P.copy()
            best_res = curr_res

    return P_best

def make_random_A():
    A = [0 for _ in range(n)]
    for i in range(n):
        A[i] = random.randint(1,MAX_VAL)
    return A

def main():
    # flag will be 0 when autograder runs, but we can do testing with it
    flag = int(sys.argv[1])

    if flag == 0: #autograder solutions
        ''' algorithm is a code:
        0 Karmarkar-Karp
        1 Repeated Random
        2 Hill Climbing
        3 Simulated Annealing
        11 Prepartitioned Repeated Random
        12 Prepartitioned Hill Climbing
        13 Prepartitioned Simulated Annealing '''
        algorithm = int(sys.argv[2])

        # inputfile is a list of 100 (unsorted) integers, one per line
        inputfile = sys.argv[3]
        A = []
        with open(inputfile) as file:
            nums = file.readlines()
            for num in nums:
                A.append(int(num.strip()))
        #A is now a list of the integers from the input file
        if algorithm == 0:
            residue = KK(A)
        elif algorithm == 1:
            #repeated random
            sol = repeated_random(A) 
            residue = std_residue(sol,A)
        elif algorithm == 2:
            #hill climbing
            sol = hill_climbing(A)
            residue = std_residue(sol,A)
        elif algorithm == 3:
            #simulated annealing
            sol = simulated_annealing(A)
            residue = std_residue(sol,A) 
        elif algorithm == 11:
            #prepartitioned repeated random
            prepar_sol = prepar_repeated_rand(A)
            residue = prepar_to_std(A, prepar_sol)
        elif algorithm == 12:
            #prepartitioned hill climbing
            prepar_sol = prepar_hill_climbing(A)
            residue = prepar_to_std(A, prepar_sol)
        elif algorithm == 13:
            #prepartitioned simulated annealing
            prepar_sol = prepar_simulated_annealing(A)
            residue = prepar_to_std(A, prepar_sol)
        print(residue)
    elif flag == 1:
        '''generate 50 random instances of the problem, and for each one,
           find the result using the KK algorithm, the repeated rand, hill climb,
           simulated annealing, using both representations of solutions; 
           algorithms should use at least 25000 iterations'''
        print(f"{'Instance':<10} {'KK':<10} {'RepRand':<12} {'Hill':<10} {'SimAnn':<10} {'PreRepRand':<12} {'PreHill':<10} {'PreSimAnn':<10}")
        for i in range(50):
            A = make_random_A()
            kk_res = KK(A)
            rand = repeated_random(A)
            hill = hill_climbing(A)
            sim = simulated_annealing(A)
            pre_rand = prepar_repeated_rand(A)
            pre_hill = prepar_hill_climbing(A)
            pre_sim = prepar_simulated_annealing(A)

            print(f"{i:<10} {kk_res:<10} {std_residue(rand,A):<12} {std_residue(hill,A):<10} {std_residue(sim,A):<10} {prepar_to_std(A, pre_rand):<12} {prepar_to_std(A,pre_hill):<10} {prepar_to_std(A,pre_sim):<10}")


if __name__ == "__main__":    
    main()