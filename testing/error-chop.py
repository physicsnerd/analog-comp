def error_chop(num):
    num = str(num)
    num = num[:15]
    return float(num)

step = 1
x = 2.353223423254354
y = 5.4234

while step <= 100:
    x = error_chop(x) + error_chop(y)
    y = error_chop(x) / error_chop(y)
    x = error_chop(x) * error_chop(y)
    y = error_chop(x) - error_chop(y)
    step+=1

print(x)
print(y)
