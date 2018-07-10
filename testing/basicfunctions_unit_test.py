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

#b.multiply tests
