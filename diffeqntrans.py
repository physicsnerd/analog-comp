import basicfunctions as b
import matplotlib.pyplot as plt
import re

eqn = input('eqn: ')
#ex in: 5x' + 2x + 2
order = int(input('the first order: '))
#ex in: 2, so eqn actually x'' = 5x' + 2x + 2

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

x_spots = findOccurrences(eqn, 'x')

x_info = {}

for i in x_spots:
    #grab coefficient - back from i until space
    #grab order - forward from i until space, len() of -> order
    end_index = x_spots.find(' ',i)#does this work with end of line? (produces -1) -> if statement, find being weird, change to index?
    order = len(x_spots[i:end_index])
    if end_index == -1:
        order = len(x_spots[i:len(x_spots)-1])
    print(order)
    #add info to dict?
    #assign vars based on order

step = 0
t_step = 10**(int(input('pwr of t_step: ')))
max_steps = int(input('max step: '))
time = []

while step <= max_steps:
    time.append(t_step*step)
    #based upon order...

#plot output
#plt.plot(time, )
#plt.show()
