from analogpack import basicfunctions as b

#b.add tests
def add_tests_correct():
    basic = b.add(2, 2)
    long = b.add(2, 3, 5, 2, 2)
    float_add = b.add(1.2, 3.4)
    return [basic, long, float_add]

assert add_tests_correct() == [4, 14, 4.6]

errors = {'short':'n', 'long':'n', 'string':'n', 'list':'n'}

try:
    b.add(1)
except:
    errors['short'] = 'y'

try:
    b.add(1, 2, 3, 4, 5, 6)
except:
    errors['long'] = 'y'

try:
    b.add('a', 'b', 'c', 'd', 'e')
except:
    errors['string'] = 'y'

try:
    b.add([1], [2], [3], [4], [5])
except:
    errors['list'] = 'y'

print(errors)

#b.subtract tests
def subtract_tests_correct():
    basic = b.subtract(2, 2)
    float_sub = b.subtract(2.2, 1.2)
    negative = b.subtract(2, 3)
    return [basic, float_sub, negative]

assert subtract_tests_correct() == [0, 1, -1]

errors = {'short':'n', 'long':'n', 'string':'n', 'list':'n'}

try:
    b.subtract(1)
except:
    errors['short'] = 'y'

try:
    b.subtract(1, 2, 3)
except:
    errors['long'] = 'y'

try:
    b.subtract('hi', 'h')
except:
    errors['string'] = 'y'

try:
    b.subtract([1, 2], [1])
except:
    errors['list'] = 'y'

print(errors)

#b.multiply tests
def multiply_tests_correct():
    basic = b.multiply(2, 2)
    float_mult = b.multiply(2.4, 3.6)
    long = b.multiply(2, 3, 4, 5, 6)
    negative = b.multiply(2, -3)
    return [basic, float_mult, long, negative]

assert multiply_tests_correct() == [4, 8.64, 720, -6]

errors = {'short':'n', 'long':'n', 'string':'n', 'list':'n'}

try:
    b.multiply(1)
except:
    errors['short'] = 'y'

try:
    b.multiply(1, 2, 3, 4, 5, 6)
except:
    errors['long'] = 'y'

try:
    b.multiply('hi', 'bye')
except:
    errors['string'] = 'y'

try:
    b.multiply([1], [2])
except:
    errors['list'] = 'y'

print(errors)

#b.divide tests
def divide_tests_correct():
    basic = b.divide(4, 2)
    float_divide = b.divide(3.5, .51)
    fractional = b.divide(1, 2)
    return [basic, float_divide, fractional]

assert divide_tests_correct() == [2, 7, .5]

errors = {'short':'n', 'long':'n', 'string':'n', 'list':'n'}

try:
    b.divide(1)
except:
    errors['short'] = 'y'

try:
    b.divide(1, 2, 3)
except:
    errors['long'] = 'y'

try:
    b.divide('hi', 'bye')
except:
    errors['string'] = 'y'

try:
    b.divide([1], [2])
except:
    errors['list'] = 'y'

print(errors)
