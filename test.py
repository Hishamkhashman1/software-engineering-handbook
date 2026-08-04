import copy

a = [[1,2,3],[4,5]]
#b = a
#b = a.copy()
b = copy.deepcopy(a)

b[0].append(4)

print (b)
print (a)
