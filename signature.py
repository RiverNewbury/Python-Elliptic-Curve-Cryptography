import points
from secrets import randbelow
from sha512 import sha_512
def gen_private_public_key(base_point):
    """
    INPUT   : Base point on the curve that is to be used
    PROCESS : Creates private and public key pair
    OUTPUT  : Tuple of public key (point object) and private key (integer)
    """
    #This just checks that inputs are in the correct form
    try:
        base_point.curve.name
    except:
        raise TypeError("base_point must be a point")

    public_key = base_point.copy()
    private_key = randbelow(base_point.order)
    public_key.mult(private_key)
    return (public_key, private_key);

def create_signature(input_base_point, private_key, bin_message):
    """
    INPUT   : Base point on the curve, private key and the message in binary
    PROCESS : Hashes message and then creates signature which can be used to autenticate sender
    OUTPUT  : Tuple of signature 2 integers
    """
    #This just checks that inputs are in the correct form
    try:
        input_base_point.curve.name
    except:
        raise TypeError("base_point must be a point")
    try:
        int(bin_message,2)
    except:
        raise TypeError("Bin_message must be a binary string")

    if not isinstance(private_key, int):
        raise TypeError("private key must be an int")

    base_point = input_base_point.copy()
    bits = len(bin(base_point.order)) - 2
    message_hash = int(bin(int(sha_512(bin_message),16))[2:bits+2],2)
    while True:
        point = base_point.copy()
        randint = randbelow(point.order)
        point.mult(randint)
        r = point.x%point.order
        if r == 0:
            continue;
        s = (message_hash + r*private_key)*points.inv(randint, point.order)%point.order
        if s == 0:
            continue;
        break;
    return (r,s);

def verify(input_base_point, input_public_key, bin_message, signature):
    """
    INPUT   : Base point, public key, the message in binary and the signature
    PROCESS : Check the signature using real hash of bin_message
    OUTPUT  : True, if signature is correct or False if it is not
    """
    #This just checks that inputs are in the correct form
    if not points.compatible(input_base_point,input_public_key):
        raise TypeError("Both base_point and public_key must be point objects")
    try:
        int(bin_message, 2)
    except:
        raise TypeError("Bin_message must be a binary string")
    if type(signature) is not tuple or len(signature) is not 2 or type(signature[0]) is not int or type(signature[1]) is not int:
        raise TypeError("Signature must be length 2 tuple of integers")

    base_point = input_base_point.copy()
    public_key = input_public_key.copy()
    r,s = signature
    Q = public_key.copy()
    Q.mult(Q.order)
    Q_co_ords = (Q.x, Q.y, Q.z)
    check =[(public_key.x, public_key.y, public_key.z) == public_key.zero, #these are the checks making sure that all the parameters are in the correct range
    Q_co_ords != Q.zero,
    public_key.find_y_squared() != public_key.y**2%public_key.curve.n,
    r >= base_point.order,
    s >= base_point.order]
    if check[0] or check[1] or check[2] or check[3] or check[4]:
        return False;

    bits = len(bin(base_point.order)) - 2
    message_hash = int(bin(int(sha_512(bin_message),16))[2:bits+2],2)
    w = points.inv(s,base_point.order)
    u = [message_hash*w%base_point.order,r*w%base_point.order]


    base_point.mult(u[0])
    public_key.mult(u[1])
    base_point.add(public_key)
    if ((base_point.x, base_point.y, base_point.z) == base_point.zero) or (r != base_point.x%base_point.order):
        return False;
    return True;
