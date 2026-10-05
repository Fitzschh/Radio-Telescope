x = [25.2, 25.4, 25.6, 26.1]
x_i = 2
x_f = -5

measured = 11.9
actual = 12.4

v_i = 2.5
v_f = 5.0
t = 3.0
m = 20.0

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

#The uncertainty of a measurement is half the spread of the measurements. To account for the fact that the uncertainty is a measure of how much the measurements vary, we divide the spread by 2.
def uncertainty_val(x):
    return spread(x) / 2

#The uncertainty range is the range of values that the true value of a measurement is likely to fall within. It is calculated by taking the mean of the measurements and adding and subtracting the uncertainty value.
def uncertainty_range(x):
    return (mean(x) - uncertainty_val(x), mean(x) + uncertainty_val(x))

#The fractional uncertainty is the uncertainty value divided by the mean of the measurements. It is a measure of how much the measurements vary relative to the mean.
def fractional_uncertainty(x):
    return uncertainty_val(x) / mean(x)

#The uncertainty percent is the uncertainty value divided by the mean of the measurements multiplied by 100. It is a measure of how much the measurements vary relative to the mean.
def uncertainty_percent(x):
    return (uncertainty_val(x) / mean(x)) * 100 

#The acceleration mostly defines the change in velocity over time. 
def acceleration(v_i, v_f, t):
    return (v_f - v_i) / t

# Introducing Newton's Laws of Motion

#Newton's Second Law states that the acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. It can be expressed mathematically as F = m * a, where F is the net force, m is the mass of the object, and a is the acceleration.
def force(m, a):
    return m * a

print(f"Force: {force(m, acceleration(v_i, v_f, t)):.2f} N")




