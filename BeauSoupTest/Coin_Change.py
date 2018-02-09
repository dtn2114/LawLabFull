__author__ = 'bill'

def coin(S, m, n):
    if n == 0:
        return 1
    if m <= 0 or n < 0:
        return 0
    return (coin(S, m-1, n) + coin(S, m, n-S[m-1]))


if __name__ == '__main__':
    nums = raw_input()
    n = int(nums.split()[0])
    m = int(nums.split()[1])
    coins = raw_input()
    S = coins.split()
    S = list(map(int, S))
    sum = coin(S, m, n)
    print sum
    asf = sum+1
