import math
from functools import reduce
import decimal
#import pigpio

#pi = pigpio.pi()

chop_flag = False
decimal_flag = False

D = decimal.Decimal if use_decimal else float 

def chop_num(num):
    '''
    Takes in a single number as input and removes all digits after the fifteenth
    to avoid numerical errors from floating point arithmetic. Format is used to
    keep it from using scientific notation as otherwise important information
    would be chopped. It returns a float.
    '''
    num = format(num,'f')#still not working, apparently
    num = num[:15]
    return float(num)

def decorator(func):
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        if chop_flag:
            return chop_num(val)
        else:
            return val
    return wrapper

@decorator
def add(n1, n2, n3=0, n4=0, n5=0):
    '''
    Takes two to five numbers as input and returns the sum.
    '''
    return n1+n2+n3+n4+n5

@decorator
def multiply(n1, n2, n3=1, n4=1, n5=1):
    '''
    Takes two to five numbers as input and returns the product.
    '''
    return n1*n2*n3*n4*n5

@decorator
def subtract(n1, n2):
    '''
    Takes two numbers as input and returns the difference. Order matters in input;
    the second input is subtracted from the first.
    '''
    return n1 - n2

@decorator
def divide(n1, n2):
    '''
    Takes two numbers as input and returns the quotient. Order matters in input;
    the second input is the divisor and the first the dividend.
    '''
    return n1/n2

@decorator
def square(n1):
    '''
    Takes one number as input which is raised to the second power, or squared.
    '''
    return n1**2

@decorator
def power(n1, n2):
    '''Takes two numbers as input. Order matters in input; the second number is the
    power and the first the base.
    '''
    return n1**n2

@decorator
def sqroot(n1):
    '''
    Takes one number as input. The square root of that number is returned.
    '''
    return math.sqrt(abs(n1))

@decorator
def logalog(n1):
    '''
    Takes one number as input, and returns the common log of that input.
    '''
    return math.log10(n1)

@decorator
def summation(vals):
    '''
    Takes in one list of values as input and returns the sum of all values in that
    list.
    '''
    return sum(vals)

@decorator
def mult_summ(vals):
    '''
    Takes in one list of values as input and returns the product of all values in
    that list.
    '''
    return reduce(lambda x, y: x*y, vals)

'''
@decorator
def tvar_int_noy2(step, t_step, new_val, integral_val, typ, init_val):
    if step == 1:
        return t_step/4*(new_val[-2]+new_val[-1])+init_val
    elif step == 2:
        return t_step/6*(new_val[-3] + 4*new_val[-2] + new_val[-1]) + init_val
    elif step == 3:
        return t_step/12*(-1*new_val[-4]+8*new_val[-2]+5*new_val[-1]) + integral_val
    elif step == 4:
        return t_step/12*(-1*new_val[-3]+8*new_val[-2]+5*new_val[-1]) + integral_val
    else:
        return t_step/24*(new_val[-4] - 5*new_val[-3] + 19*new_val[-2] + 9*new_val[-1]) + integral_val

def tvar_int_3stage(step, t_step, new_val, integral_val, typ, init_val):
    if step == 1:
        return t_step/8*(new_val[-2]+new_val[-1])+init_val
    elif step == 2:
        return t_step/12*(new_val[-3] + 4*new_val[-2] + new_val[-1]) + init_val
    elif step == 3:
        return t_step/6*(new_val[-4] - 4*new_val[-3]+7*new_val[-2]+2*new_val[-1]) + integral_val
    elif step == 4:
        return
    elif step == 5:
        return
    elif step == 6:
        return
    else:
        return
'''

def trap(step, t_step, new_val, init_val):
    return t_step/2*(new_val[-2] + new_val[-1]) + init_val

def simp13(step, t_step, new_val, init_val):
    return t_step/3*(new_val[-3]+4*new_val[-2]+new_val[-1]) + init_val

def simp38(step, t_step, new_val, init_val):
    return 3*t_step/8*(new_val[-4] + 3*new_val[-3] + 3*new_val[-2] + new_val[-1]) + init_val

def boole(step, t_step, new_val, init_val):
    return 2*t_step/45*(7*new_val[-5] + 32*new_val[-4] + 12*new_val[-3] + 32*new_val[-2] + 7*new_val[-1]) + init_val

def fifth(step, t_step, new_val, init_val):
    return 5*t_step/288*(19*new_val[-6] + 75*new_val[-5] + 50*new_val[-4] + 50*new_val[-3] + 75*new_val[-2] + 19*new_val[-1]) + init_val

def trapcum(step, t_step, new_val, integral_val):
    return t_step/2*(new_val[-2] + new_val[-1]) + integral_val

def simp13cum(step, t_step, new_val, integral_val):
    return t_step/12*(-1*new_val[-3]+8*new_val[-2]+5*new_val[-1]) + integral_val

def simp38cum(step, t_step, new_val, integral_val):
    return t_step/12*(-1*new_val[-3]+8*new_val[-2]+5*new_val[-1]) + integral_val

def boolecum(step, t_step, new_val, integral_val):
    return t_step/720*(-19*new_val[-5] + 106*new_val[-4] - 264*new_val[-3] + 646*new_val[-2] + 251*new_val[-1]) + integral_val

def fifthcum(step, t_step, new_val, integral_val):
    return t_step/1440*(27*new_val[-6] - 173*new_val[-5] + 482*new_val[-4] - 798*new_val[-3] + 1427*new_val[-2] + 475*new_val[-1]) + integral_val

@decorator
def integrate(step, t_step, new_val, integral_val, typ, init_val):
    '''
    See overall documentation for full explanation. Typ is an extra flag, short
    for type (type() is a built-in so that is not used), to indicate whether
    the user wants the simpson method ('simp'), the 3/8ths simpson method
    ('simp38'),the boole method ('boole'), or a 5th order Newton-Cotes ('5th')
    or the trapezoidal method ('trap').
    '''
    if typ == 'simp' or typ == 'simp13':
        if step == 1:
            #return t_step/2*(new_val[-2] + new_val[-1]) + init_val
            return trap(step, t_step, new_val, init_val)
        elif step == 2:
            #return t_step/3*(new_val[-3]+4*new_val[-2]+new_val[-1]) + init_val
            return simp13cum(step, t_step, new_val, integral_val)
        else:
            return t_step/12*(-1*new_val[-3]+8*new_val[-2]+5*new_val[-1]) + integral_val
    elif typ == 'simp38':
        if step == 1:
            #return t_step/2*(new_val[-2] + new_val[-1])+init_val
            return trap(step, t_step, new_val, init_val)
        elif step == 2:
            array_values = new_val[-3]+4*new_val[-2]+new_val[-1]
            return t_step/3*(array_values) + init_val
        elif step == 3:
            values1 = new_val[-4] + 3*new_val[-3]
            values2 = 3*new_val[-2] + new_val[-1]
            return 3*t_step/8*(values1 + values2) + init_val
        else:
            values1 = new_val[-4] - 5*new_val[-3]
            values2 = 19*new_val[-2] + 9*new_val[-1]
            return t_step/24*(values1 + values2) + integral_val
    elif typ == 'boole':
        if step == 1:
            #return t_step/2*(new_val[-2] + new_val[-1]) + init_val
            return trap(step, t_step, new_val, init_val)
        elif step == 2:
            array_values = new_val[-3]+4*new_val[-2]+new_val[-1]
            return t_step/3*(array_values) + init_val
        elif step == 3:
            return 3*t_step/8*(new_val[-4] + 3*new_val[-3] + 3*new_val[-2] + new_val[-1]) + init_val
        elif step == 4:
            return 2*t_step/45*(7*new_val[-5] + 32*new_val[-4] + 12*new_val[-3] + 32*new_val[-2] + 7*new_val[-1]) + init_val
        else:
            return t_step/720*(-19*new_val[-5] + 106*new_val[-4] - 264*new_val[-3] + 646*new_val[-2] + 251*new_val[-1]) + integral_val
    elif typ == '5th':
        if step == 1:
            #return t_step/2*(new_val[-2] + new_val[-1]) + init_val
            return trap(step, t_step, new_val, init_val)
        elif step == 2:
            array_values = new_val[-3]+4*new_val[-2]+new_val[-1]
            return t_step/3*(array_values) + init_val
        elif step == 3:
            return 3*t_step/8*(new_val[-4] + 3*new_val[-3] + 3*new_val[-2] + new_val[-1]) + init_val
        elif step == 4:
            return 2*t_step/45*(7*new_val[-5] + 32*new_val[-4] + 12*new_val[-3] + 32*new_val[-2] + 7*new_val[-1]) + init_val
        elif step == 5:
            return 5*t_step/288*(19*new_val[-6] + 75*new_val[-5] + 50*new_val[-4] + 50*new_val[-3] + 75*new_val[-2] + 19*new_val[-1]) + init_val
        else:
            return t_step/1440*(27*new_val[-6] - 173*new_val[-5] + 482*new_val[-4] - 798*new_val[-3] + 1427*new_val[-2] + 475*new_val[-1]) + integral_val
    elif typ == 'timevar':
        if step == 1:
            #return t_step/2*(new_val[-2]+new_val[-1])+init_val
            return trap(step, t_step, new_val, init_val)
        elif step == 2:
            return t_step/3*(new_val[-3] + 4*new_val[-2] + new_val[-1]) + init_val
        elif step == 3:
            return t_step/6*(new_val[-4] - 4*new_val[-3]+7*new_val[-2]+2*new_val[-1]) + integral_val
        elif step == 4:
            return t_step/12*(-1*new_val[-3]+8*new_val[-2]+5*new_val[-1]) + integral_val
        else:
            return t_step/24*(new_val[-4] - 5*new_val[-3] + 19*new_val[-2] + 9*new_val[-1]) + integral_val
    else:
        return t_step/2*(new_val[-2] + new_val[-1]) + integral_val


@decorator
def derivative(val, t_step):
    '''
    Takes in an array of values (the function only uses two) and a float as inputs.
    Subtracts the the two most recent values in the array and divides by the float,
    or time step, to find a rough derivative. More accurate derivative functions
    require knowledge of the function, meaning they cannot be used.
    '''
    return (val[-1] - val[-2])/t_step

def pwm_map(val, mini, maxi, pwm_res):
    '''
    Takes in the value to be scaled, the minimum possible value for val, the
    maximum possible value for val, and the resolution of the pwm in use. "mini" and
    "maxi" are named as such due to the python built-ins min() and max(). Full
    description of this function is found in the overall documentation.
    '''
    scale_fac = (2**pwm_res)-1
    if mini < 0:
        x = val + (0 - mini)
        return round(x/(maxi-mini)*scale_fac)
    else:
        x = val - mini
        return round(x/(maxi-mini)*scale_fac)

def step_vary(xv_array, yv_array, xa_array, ya_array, tolerance):
    '''
    See overall documentation.
    '''
    t_step_type = 'normal'
    try:
        dxa = abs(xa_array[-1]/xa_array[-2])
        dya = abs(ya_array[-1]/ya_array[-2])
        dxv = abs(xv_array[-1]/xv_array[-2])
        dyv = abs(yv_array[-1]/yv_array[-2])
        if (dxv > (1 + tolerance)) or (dyv > (1+tolerance)) or (dxa > (1+tolerance)) or (dya > (1 + tolerance)):
            t_step_type = 'fine'
        elif dxv < (1-tolerance) or dyv < (1-tolerance) or dxa < (1-tolerance) or dya < (1-tolerance):
            t_step_type = 'fine'
        else:
            t_step_type = 'normal'
    except ZeroDivisionError:
        t_step_type = 'normal'
    if t_step_type == 'normal':
        return 10**(-12)
    else:
        return 10**(-15)
