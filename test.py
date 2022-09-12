
def split_im(s):
    a = []

    for i in range(0, len(s), 2):
        a.append(s[i:i+2])

    return a

print(split_im(split_im("sexbubjka")))

# print()