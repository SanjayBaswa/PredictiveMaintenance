import numpy as np

data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1, 22, 2, 2, 2, 2, 2, 2
    , 2, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1]

an = []

for i in data:
    if i > 4:
        an.append(-1)
    else:
        an.append(1)

data = np.array(data)
an = np.array(an)

k = data[an == -1]
print(k , type(list(k)))

print(data)
print(an)
