import points
from secrets import randbelow

def gen_private_public_key(base_point):
    """
    INPUT   : Base point on curve that is to be used
    PROCESS : Generates private and public keys
    OUTPUT  : Tuple of public key (point object) and private key (int)
    """
    #This just checks that inputs are in the correct form
    try:
        base_point.curve.name
    except:
        raise TypeError("base_point must be a point")
    public_key = base_point.copy()
    private_key = randbelow(public_key.order)
    public_key.mult(private_key)
    return (public_key, private_key); # Public and private key pair


def encrypt(input_base_point, input_public_key, message):
    """
    INPUT   : Base point used, public key and message to be encrypted (integer)
    PROCESS : Encodes message to a point on the curve and then hides that in another object
    OUTPUT  : Tuple of 2 point objects which makes up the encrypted message
    """
    #This just makes sure that all inputs are in the correct from
    if not points.compatible(input_base_point,input_public_key):
        raise TypeError("Both base_point and public_key must be point objects")

    if type(message) is not int:
        raise TypeError("message must be an int")

    point = input_base_point.copy()
    public_key = input_public_key.copy()
    message *= 100
    if message>point.order:
        raise Error("This message can't be mapped onto the curve correctly "
            "please break it down into number less than the order of the "
            "curve/100 or {0}".format(point.order//100))

    B = randbelow(point.order) # This is the Users random Number
    message_point = point.copy()
    message_point.x = message
    point.mult(B)
    public_key.mult(B)
    for i in range (100):
        message_point.find_y()
        if message_point.y != "Has no y":
            break;
        message_point.x += 1
    else:
        raise Error("Looks like this message can't be mapped onto the curve, sorry")
    message_point.add(public_key)
    return (point,message_point);

def decrypt(private_key, input_base_point, input_message_point):
    """
    INPUT   : Private key and tuple of encrypted point
    PROCESS : Decodes the message out of the curve
    OUTPUT  : Message (integer)
    """
    #This just makes sure that all inputs are in the correct from
    if not points.compatible(input_base_point,input_message_point):
        raise TypeError("Both base_point and message_point must be point objects")
    if type(private_key) is not int:
        raise TypeError("private_key must be an int")
    message_point = input_message_point.copy()
    point = input_base_point.copy()
    point.mult(private_key)
    message_point.sub(point)
    return message_point.x//100;
