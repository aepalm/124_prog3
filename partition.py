# Use: ./partition.py flag algorithm inputfile
# Going to have to include a makefile
import sys
import random
import heapq
import math

MAX_ITER = 25000

def KK(A):
    n = len(A)
    heapq.heapify_max(A)
    for i in range(n-1):
        max1 = heapq.heappop_max(A)
        max2 = heapq.heappop_max(A)
        diff = abs(max1 - max2)
        heapq.heappush_max(diff)
    return heapq.heappop_max(A) #returns residue

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
    N = S
    n = len(S)
    i = random.randint(1, n)
    j = i
    while j == i:
        j = random.randint(1,n)
    N[i] = -N[i]
    
    rand_val = random.random()
    if rand_val < 0.5:
        N[j] = -N[j]

    return N

def random_prepar_move(P):
    #randomly move from P to a neighbor (for prepartitioned solution P)
    N = P
    n = len(P)
    i = random.randint(1, n)
    j = random.randint(1, n)
    while P[i] == j:
        j = random.randint(1,n)
    N[i] = j
    return N

def prepar_to_std(A, P): 
    #given a prepartitioned solution P and the original A, return residue
    n = len(P)
    A_new = [0 for _ in range(n)]
    for i in range(1, n+1):
        p_i = P[i]
        A_new[p_i] += A[i]
    
    return KK(A_new)

def std_residue(S, A):
    #find the residue from a standard solution S
    residue = 0
    for i in range(len(A)):
        residue += S[i]*A[i]
    return residue

def repeated_random(A):
    #S is an initial random solution
    S = random_sol(len(A))
    for i in range(MAX_ITER):
        S_new = random_sol(len(A))
        if std_residue(S_new) < std_residue(S):
            S = S_new
    return S

def hill_climbing(A):
    S = random_sol(len(A))
    for i in range(MAX_ITER):
        neighbor = random_move(S)
        if std_residue(neighbor) < std_residue(S):
            S = neighbor
    return S

def simulated_annealing(A):
    S = random_sol(len(A))
    S_dprime = S
    for i in range(MAX_ITER):
        neighbor = random_move(S)
        T_iter = (10^10)*(0.8)^(i/300)
        n_res = std_residue(neighbor)
        s_res = std_residue(S)
        prob = math.exp(-(n_res - s_res)/T_iter)
        if n_res < s_res:
            S = neighbor
        else: 
            rand = random.random()
            if rand < prob:
                S = neighbor
        
        if std_residue(S) < std_residue(S_dprime):
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
    #P is an initial prepartitioned random solution
    P = random_prepar_sol(len(A))
    for i in range(MAX_ITER):
        neighbor = random_prepar_move(len(A))
        if prepar_to_std(A, neighbor) < prepar_to_std(A, P):
            P = neighbor
    return P

def prepar_simulated_annealing(A):
    P = random_prepar_sol(len(A))
    P_dprime = P
    for i in range(MAX_ITER):
        neighbor = random_prepar_move(P)
        T_iter = (10^10)*(0.8)^(i/300)
        n_res = prepar_to_std(neighbor)
        p_res = prepar_to_std(P)
        prob = math.exp(-(n_res - p_res)/T_iter)
        if n_res < p_res:
            P = neighbor
        else: 
            rand = random.random()
            if rand < prob:
                P = neighbor
        
        if std_residue(P) < std_residue(P_dprime):
            P_dprime = P
    
    return P_dprime

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
        algorithm = sys.argv[2]

        # inputfile is a list of 100 (unsorted) integers, one per line
        inputfile = sys.argv[3]
        A = []
        with open(inputfile) as file:
            nums = file.readlines()
            for num in nums:
                A.append(num)
        #A is now a list of the integers from the input file
        if algorithm == 0:
            residue = KK(A)
        elif algorithm == 1:
            #repeated random
            sol = repeated_random(A) 
            residue = std_residue(sol)
        elif algorithm == 2:
            #hill climbing
            sol = hill_climbing(A)
            residue = std_residue(sol)
        elif algorithm == 3:
            #simulated annealing
            sol = simulated_annealing(A)
            residue = std_residue(sol) 
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
        return residue
    elif flag == 1:
        '''generate 50 random instances of the problem, and for each one,
           find the result using the KK algorithm, the repeated rand, hill climb,
           simulated annealing, using both representations of solutions; 
           algorithms should use at least 25000 iterations'''
        for i in range(50):
            print("Instance \t KK \t RepRand \t Hill \t SimAnn \t PreRepRand \t PreHill \t PreSimAnn")
            A = [random.randint(1,(10^12)) for _ in range(100)]
            kk_res = KK(A)
            rand = repeated_random(A)
            hill = hill_climbing(A)
            sim = simulated_annealing(A)
            pre_rand = prepar_repeated_rand(A)
            pre_hill = prepar_hill_climbing(A)
            pre_sim = prepar_simulated_annealing(A)
            print(i, "\t", kk_res, "\t", std_residue(rand), "\t", std_residue(hill), "\t", std_residue(sim), "\t", prepar_to_std(pre_rand), "\t", prepar_to_std(pre_hill), "\t", prepar_to_std(pre_sim))

            


if __name__ == "__main__":    
    main()