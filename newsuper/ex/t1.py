

a = 2

d = [lambda : a>0, lambda : a<0]
print([x() for x in d])