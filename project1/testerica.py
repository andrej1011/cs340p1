def malifunc(broj):
    return broj+1, broj+2,broj+3

if __name__ == '__main__':
    a,b,c = malifunc(12)
    print(f"{a},{b},{c}")