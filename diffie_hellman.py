def start_step(point):
    from secrets import randbelow
    global __randnum
    #This just checks that inputs are in the correct form
    try:
        point.curve.name
    except:
        raise TypeError("base_point must be a point object")
    __randnum = randbelow(point.order)
    point.mult(__randnum)
def end_step(point):
    #This just checks that inputs are in the correct form
    try:
        point.curve.name
    except:
        raise TypeError("point must be a point object")
    point.mult(__randnum)
    del __randnum
