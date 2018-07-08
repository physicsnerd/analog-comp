'''
Math for square root, reduce from functools for multiplication of every element
in list, decimal for floating point accuracy, and pigpio for if running on
Raspberry Pi and wishing to output on oscilloscope.
'''
import math
from functools import reduce
import decimal
#import pigpio

#pi = pigpio.pi()

CHOP_FLAG = False
DECIMAL_FLAG = False

D = decimal.Decimal if DECIMAL_FLAG else float

def chop_num(num):
    '''
    Takes in a single number as input and removes all digits after the fifteenth
    to avoid numerical errors from floating point arithmetic. Format is used to
    keep it from using scientific notation as otherwise important information
    would be chopped. It returns a float.
    '''
    num = format(num, 'f')#still not working, apparently
    num = num[:15]
    return float(num)

def decorator(func):
    '''
    Decorator which uses chop_num to try to reduce floating point error on output
    of every function. Not currently in use as chop_flag is set to False, as there
    is an error somewhere.
    '''
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        if CHOP_FLAG:
            return chop_num(val)
        else:
            return val
    return wrapper

@decorator
def add(n_1, n_2, n_3=0, n_4=0, n_5=0):
    '''
    Takes two to five numbers as input and returns the sum.
    '''
    return n_1 + n_2 + n_3 + n_4 + n_5

@decorator
def multiply(n_1, n_2, n_3=1, n_4=1, n_5=1):
    '''
    Takes two to five numbers as input and returns the product.
    '''
    return n_1 * n_2 * n_3 * n_4 * n_5

@decorator
def subtract(n_1, n_2):
    '''
    Takes two numbers as input and returns the difference. Order matters in input;
    the second input is subtracted from the first.
    '''
    return n_1 - n_2

@decorator
def divide(n_1, n_2):
    '''
    Takes two numbers as input and returns the quotient. Order matters in input;
    the second input is the divisor and the first the dividend.
    '''
    return n_1/n_2

@decorator
def square(n_1):
    '''
    Takes one number as input which is raised to the second power, or squared.
    '''
    return n_1**2

@decorator
def power(n_1, n_2):
    '''Takes two numbers as input. Order matters in input; the second number is the
    power and the first the base.
    '''
    return n_1**n_2

@decorator
def sqroot(n_1):
    '''
    Takes one number as input. The square root of that number is returned.
    '''
    return math.sqrt(abs(n_1))

@decorator
def logalog(n_1):
    '''
    Takes one number as input, and returns the common log of that input.
    '''
    return math.log10(n_1)

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

def trap(t_step, new_val, init_val):
    '''
    Performs the trapezoidal method on a given interval.
    '''
    return t_step/2*(new_val[-2] + new_val[-1]) + init_val

def simp13(t_step, new_val, init_val):
    '''
    Performs the standard simpson 1/3rd method on a given interval.
    '''
    return t_step/3*(new_val[-3]+4*new_val[-2]+new_val[-1]) + init_val

def simp38(t_step, new_val, init_val):
    '''
    Performs the standard simpson 3/8ths method on a given interval.
    '''
    return 3*t_step/8*(new_val[-4] + 3*new_val[-3] + 3*new_val[-2] + new_val[-1]) + init_val

def boole(t_step, new_val, init_val):
    '''
    Performs the standard 4th order Newton-Cotes, boole, on a given interval.
    '''
    vals = 7*new_val[-5] + 32*new_val[-4] + 12*new_val[-3] + 32*new_val[-2] + 7*new_val[-1]
    return 2*t_step/45*(vals) + init_val

def fifth(t_step, new_val, init_val):
    '''
    Performs the standard fifth order Newton-Cotes on a given interval.
    '''
    vals_1 = 75*new_val[-2] + 19*new_val[-1]
    vals = 19*new_val[-6] + 75*new_val[-5] + 50*new_val[-4] + 50*new_val[-3] + vals_1
    return 5*t_step/288*(vals) + init_val

def trapcum(t_step, new_val, integral_val):
    '''
    Performs trapezoidal method but adding the full set of previous vals, not just
    init val.
    '''
    return t_step/2*(new_val[-2] + new_val[-1]) + integral_val

def simp13cum(t_step, new_val, integral_val):
    '''
    Performs cumulative simpson method, also adds integral val as opposed to init.
    '''
    return t_step/12*(-1*new_val[-3]+8*new_val[-2]+5*new_val[-1]) + integral_val

def simp38cum(t_step, new_val, integral_val):
    '''
    Performs cumulative simpson 3/8ths method, also adds integral val as opposed to
    init.
    '''
    return t_step/12*(-1*new_val[-3]+8*new_val[-2]+5*new_val[-1]) + integral_val

def boolecum(t_step, new_val, integral_val):
    '''
    Performs cumulative boole method, also adds integral val as opposed to init.
    '''
    vals = -19*new_val[-5] + 106*new_val[-4] - 264*new_val[-3] + 646*new_val[-2] + 251*new_val[-1]
    return t_step/720*(vals) + integral_val

def fifthcum(t_step, new_val, integral_val):
    '''
    Peforms cumulative fifth order method, also adds integral val as opposed to init.
    '''
    vals_1 = 1427*new_val[-2] + 475*new_val[-1]
    vals = 27*new_val[-6] - 173*new_val[-5] + 482*new_val[-4] - 798*new_val[-3] + vals_1
    return t_step/1440*(vals) + integral_val

@decorator
def integrate(step, t_step, new_val, integral_val, typ, init_val, time):
    '''
    See overall documentation for full explanation. Typ is an extra flag, short
    for type (type() is a built-in so that is not used), to indicate whether
    the user wants the simpson method ('simp'), the 3/8ths simpson method
    ('simp38'),the boole method ('boole'), or a 5th order Newton-Cotes ('5th')
    or the trapezoidal method ('trap').
    '''
    if typ != 'timevar':
        time.append(t_step*step)
    else:
        if step == 1:
            time.append(t_step/2)
        elif step == 2:
            time.append(t_step/2 + time[-1])
        else:
            time.append(t_step + time[-1])
    command = {}
    command['trap'] = {1:trap}
    command['simp13'] = {1:trap, 2:simp13,}
    command['simp38'] = {1:trap, 2:simp13, 3:simp38}
    command['boole'] = {1:trap, 2:simp13, 3:simp38, 4:boole}
    command['5th'] = {1:trap, 2:simp13, 3:simp38, 4:boole, 5:fifth}
    default_command = {'trap':trapcum, 'simp13':simp13cum, 'simp38':simp38cum, 'boole':boolecum, 'fifth':fifthcum}
    if step in command[typ].keyValues():
        return command[typ][step](t_step, new_val, init_val)
    else:
        return default_command[typ](t_step, new_val, integral_val)

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
        range_spot = val + (0 - mini)
        return round(range_spot/(maxi-mini)*scale_fac)
    else:
        range_spot = val - mini
        return round(range_spot/(maxi-mini)*scale_fac)

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
