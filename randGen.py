import random

'''could change the name to generate_random'''

def genRandNum(rolls = 1, low = 1, high = 10):
    '''change name to random_int'''
    out = []
    for _ in range(rolls):
        num = random.randint(low, high)
        out.append(num)

    return out

def dice(rolls = 1, sides = 6):
    out = []
    for _ in range(rolls):
        num = random.randint(1, sides)
        out.append(num)

    return out

def coin(rolls = 1):
    out = []
    for _ in range(rolls):
        if round(random.random()):
            out.append("heads")
        else:
            out.append("tails")

    return out

if __name__ == "__main__":
    # print(GenRandNum())
    # print(GenRandNum(low=-9223372036854775807, high=9223372036854775807))
    # print(dice())
    print(coin(12))