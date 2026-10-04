x = [5, 3, 4, 6]
x_i = 2
x_f = -5

measured = 11.9
actual = 12.4

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

#The rate of change of position with respect to time
def avg_velocity(x_i, x_f, t):
    return displacement(x_i, x_f) / t

#The difference between the measured value and the actual value
def error(measured, actual):
    return measured - actual

#The difference between the measured value and the actual value divided by the actual value
def fractional_error(measured, actual):
    return error(measured, actual) / actual

#The difference between the measured value and the actual value divided by the actual value multiplied by 100
def percent_error(measured, actual):
    return (error(measured, actual) / actual) * 100

#The average of a list of numbers
def mean(x):
    return sum(x) / len(x)

#The difference between the maximum and minimum values in a list of numbers, or the range of the list. 
def spread(x):
    return max(x) - min(x)

