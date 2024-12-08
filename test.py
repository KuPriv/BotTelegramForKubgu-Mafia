a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

for i in range(int(len(a) / 5) + 1):
    s = ''
    if len(a) - (i * 5) >= 5:
        for j in range(5):
            s += str(a[(i * 5) + j])
    else:
        for j in range(len(a) - (i * 5)):
            s += str(a[(i * 5) + j])
    print(s)