def right_rotate(num, rotate, bits): # It dosen't think this should work
    """
    INPUT   : Number to be rotated, how many bits to be rotated, and maximum bits in answer
    PROCESS : Uses combination of left and right shifts
    OUTPUT  : Rotated number
    """
    return ((num<<(bits - rotate)) % 2**bits) + (num>>rotate);

def right_shift(num,shift):
    """
    INPUT   : Number to be shifted and how many bits to shift
    OUTPUT  : Shifted number
    """
    return num>>shift;

def to_binary(message):
    """
    INPUT   : Message (either integer or string of ascii characters)
    PROCESS : Will return error if not string or int
    OUTPUT  : Binary string
    """
    if isinstance(message, int):
        binary = bin(message)[2:]
    elif isinstance(message, str):
        binary = ''.join([bin(ord(i))[2:].fill(8) for i in message])
    else:
        raise TypeError("Message must be string or integer")    ;
    return binary;

def pre_processing(bin_message):
    """
    INPUT   : Binary string
    PROCESS : Converts it to the required form for sha 512
    OUTPUT  : An array of 1024 bit strings
    """
    length = len(bin_message)
    num_zeros = (-(length + 129))%1024
    bin_message += "1" + "0"*num_zeros
    bin_message += bin(length)[2:].zfill(128)
    length = len(bin_message)
    message_array = [bin_message[i*1024:(i+1)*1024] for i in range(length//1024)]
    return message_array;

def processing(message_array):
    """
    INPUT   : An array of 1024 bit strings
    PROCESS : This is the main part which actually calculates hash of message
    OUTPUT  : Hash as an hex string
    """
    hash_constants = [0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
        0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]
    round_constants = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
        0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
        0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
        0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
        0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
        0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
        0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
        0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
        0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
        0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
        0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
        0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
        0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
        0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
        0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
        0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
        0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
        0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
        0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
        0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]

    for chunk in message_array:
        schedule = [int(chunk[64*i:64*(i+1)],2) for i in range(16)]

        for i in range(16,80):
            p0 = right_rotate(schedule[i-15],1,64)^right_rotate(schedule[i-15],8,64)^right_shift(schedule[i-15],7)
            p1 = right_rotate(schedule[i-2],19,64)^right_rotate(schedule[i-2],61,64)^right_shift(schedule[i-2],6)
            #print(L_Schedule[i-2],p1,L_Schedule[i-7],p0,L_Schedule[i-16])
            schedule.append((schedule[i-16] + p0 + schedule[i-7] + p1)%(pow(2,64)))
        working = hash_constants[0:]
        for i in range (0,80):
            p0 = right_rotate(working[4],14,64)^right_rotate(working[4],18,64)^right_rotate(working[4],41,64)

            p1 = (working[4] & working[5])^((~working[4])&working[6])

            temp1 = (working[7] + p0 + p1 + round_constants[i] + schedule[i])%pow(2,64)

            p0 =right_rotate(working[0],28,64)^right_rotate(working[0],34,64)^right_rotate(working[0],39,64)

            p1 = (working[0]&working[1])^(working[0]&working[2])^(working[1]&working[2])

            temp2 = (p0+p1)%pow(2,64)

            working = [working[-1]] + working[:-1]

            #print (working)

            working[0] = (temp1+temp2)%pow(2,64)
            working[4] = (working[4]+temp1)%pow(2,64)
        for i in range (8):
            hash_constants[i] = (hash_constants[i] + working[i])%pow(2,64)
            #print (L_Hash)
    out = ''.join([hex(i)[2:].zfill(16) for i in hash_constants])
    return out;

def sha_512(bin_message):
    """
    INPUT   : A binary message
    PROCESS : Pre-processes the message then calculates the has
    OUTPUT  : Hash as hex string
    """
    return processing(pre_processing(bin_message))
