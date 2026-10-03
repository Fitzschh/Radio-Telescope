x = [5, 3, 4, 6]

def distance(x):
    x = [abs(i) for i in x]
    return sum(x)

print(distance(x))