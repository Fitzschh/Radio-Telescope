x = [5, 3, 4, 6]

def distance(x):
    x = [abs(i) for i in x]
    return sum(x)

def avg_speed(x, t):
    return distance(x) / t

print(f"Average speed: {avg_speed(x, 10)}m/s")
