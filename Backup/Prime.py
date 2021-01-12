#from random import randint
from secrets import randbelow
def Checker(I_Num): # Uses Fermat's last theorem? to give true if high probability of prime
    L_Prime = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    for i in L_Prime:
        if (I_Num%i == 0):
            if (I_Num == i):
                return True;
            return False;
    L_Prime = L_Prime[:6]
    for i in L_Prime:
        if (pow(i,I_Num-1,I_Num) == 1):
            continue;
        else:
            return False;
    return True;

def RandNum_With_MinOne_Factors(I_Length,Min,Max):
    while True:
        I_Prime, L_Factors = RandNum_Factored(I_Length,Min,Max)
        I_Prime, L_Factors = 2*I_Prime + 1, [2] + L_Factors
        print (I_Prime,L_Factors)
        if Checker(I_Prime):
            return (I_Prime, L_Factors);

def RandNum_Factored(Length,Min,Max):
    Random_Num = 1
    L_Factors = []
    while (Random_Num<pow(2,Length)):
        Add = Rand_Prime(Min,Max)
        L_Factors.append(Add)
        Random_Num = Add*Random_Num
    return (Random_Num,L_Factors);

def Rand_Prime(Min,Max):
    while True:
        Prime = randbelow(Max)
        if Prime>=Min and Checker(Prime):
            return Prime;
#print(RandNum_Factored(10))
#print(Rand_Prime(pow(2,13900),pow(2,19050)))
    
#print((2**511 - 187)*2+1)
