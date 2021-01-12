#import time
def RightRotate(Text,I_Rotate):
    S_Text = bin(Text)[2:].zfill(32)
    while I_Rotate>=len(S_Text):
        I_Rotate-=len(S_Text)
    return int(S_Text[-I_Rotate:]+S_Text[:-I_Rotate],2);
def RightShift(Text,I_Shift):
    S_Text = bin(Text)[2:]
    try:
        return int(S_Text[:-I_Shift],2);
    except:
        return 0;
def MessageProcessing(Bin_Message):
    I_Length = len(Bin_Message)
    print(bin(I_Length)[2:].zfill(32))
    Bin_Message += "1" +"0"*(512-(I_Length+1+64)%512) + bin(I_Length)[2:].zfill(64)
    L_Bin_Message = []
    for i in range(len(Bin_Message)//512):
        L_Bin_Message.append(Bin_Message[512*(i):512*(i+1)])
    return L_Bin_Message;
def PreProcessing(S_Text):
    L_Hash = []
    for i in range(8):
        L_Hash.append(int((pow(L_Primes[i],.5) - int(pow(L_Primes[i],.5)))*4294967296))    #pow(2,32) 
    L_RoundConst = []
    for i in range(64):
        L_RoundConst.append(int((pow(L_Primes[i],(1/3)) - int(pow(L_Primes[i],(1/3))))*4294967296))    #pow(2,32)
    #print (time.time()-start)
    S_Salt = Salt(256)
    #S_Text += S_Salt
    Bin_Message = ''.join([i[2:].zfill(8) for i in list(map(bin,bytearray(S_Text,'utf8')))])
    
    #print (Binary)
    #print (len(L_Message[0])%512)
    return (L_Hash,L_RoundConst,S_Salt,MessageProcessing(Bin_Message));
def Salt(I_Len):
    from secrets import randbelow
    S_Salt = ""
    for i in range(I_Len):
        S_Salt += chr(randbelow(96)+32)
    return S_Salt;
def Sha_2(L_Hash,L_RoundConst,L_Primes,L_Bin_Message):
    for Chunk in L_Bin_Message:
        #print (Chunk)
        L_Schedule = [int(Chunk[32*i:32*(i+1)],2) for i in range(16)]
        
        for i in range(16,64):
            p0 = (RightRotate(L_Schedule[i-15],7)^RightRotate(L_Schedule[i-15],18))^RightShift(L_Schedule[i-15],3)
            p1 = (RightRotate(L_Schedule[i-2],17)^RightRotate(L_Schedule[i-2],19)^RightShift(L_Schedule[i-2],10))
            #print(L_Schedule[i-2],p1,L_Schedule[i-7],p0,L_Schedule[i-16])
            L_Schedule.append((L_Schedule[i-16]+p0+L_Schedule[i-7]+p1)%(pow(2,32)))
        #print(L_Schedule)
        L_Working = L_Hash[0:]
        for i in range (0,64):
            p0 =RightRotate(L_Working[4],6)^RightRotate(L_Working[4],11)^RightRotate(L_Working[4],25)

            p1 = (L_Working[4] & L_Working[5])^((~L_Working[4])&L_Working[6])

            temp1 = (L_Working[7]+p0+p1+L_RoundConst[i]+L_Schedule[i])%pow(2,32)

            p0 =RightRotate(L_Working[0],2)^RightRotate(L_Working[0],13)^RightRotate(L_Working[0],22)

            p1 = (L_Working[0]&L_Working[1])^(L_Working[0]&L_Working[2])^(L_Working[1]&L_Working[2])

            temp2 = (p0+p1)%pow(2,32)

            L_Temp = L_Working[0:]
            for l in range(8):
                L_Working[l] = L_Temp[l-1]
            #print (L_Working)
            #print (L_Temp)
            L_Working[0] = (temp1+temp2)%pow(2,32)
            L_Working[4] = (L_Working[4]+temp1)%pow(2,32)
        for i in range (8):
            L_Hash[i] = (L_Hash[i]+L_Working[i])%pow(2,32)
            #print (L_Hash)
    S_Out = ""
    for i in L_Hash:
        S_Out += hex(i)[2:]
        print(hex(i))
    return S_Out;
L_Primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
            107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
            227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331]
L_Hash,L_RoundConst,S_Salt,L_Bin_Message = PreProcessing("Helloa")
Hash = Sha_2(L_Hash,L_RoundConst,L_Primes,L_Bin_Message)
print(Hash)
