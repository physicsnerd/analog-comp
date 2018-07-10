from analogpack import basicfunctions as b

#b.add tests
def add_tests_correct():
    basic = b.add(2, 2)
    long = b.add(2, 3, 5, 2, 2)
    float_add = b.add(1.2, 3.4)
    return [basic, long, float_add]
    return [error_short, error_long, error_string, error_list]

assert add_tests_correct() == [4, 14, 4.6]

errors = {'short':'n', 'long':'n', 'string':'n', 'list':'n', 'mixed':'n'}

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

try:
    b.add(1, [2], 'c')
except:
    errors['mixed'] = 'y'

print(errors)

