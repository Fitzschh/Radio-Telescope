x = [5, 3, 4, 6]
x_i = 2
x_f = -5

#Total length of the path traveled
def distance(x):
    x = [abs(i) for i in x]
    return sum(x)

#How far an object has moved from its initial position to its final position
def displacement(x_i, x_f):
    return x_f - x_i

#The rate of change of distance with respect to time
def avg_speed(x, t):
    return distance(x) / t

print("Displacement: ", displacement(x_i, x_f))
