# Use: python partition.py flag algorithm inputfile
# Going to have to include a makefile of some kind ??
import sys




def main():
    # flag will be 0 when autograder runs, but we can do testing with it
    flag = sys.argv[1] 
    
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


if __name__ == "__main__":    
    main()