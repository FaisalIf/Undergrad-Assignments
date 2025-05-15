import numpy as np

inp = open("input2.txt", "r")
outp = open("output2.txt", "w")

n1 = int(inp.readline())
arr1 = np.array(list(map(int, inp.readline().split(" "))))
n2 = int(inp.readline())
arr2 = np.array(list(map(int, inp.readline().split(" "))))
n3 = n1+n2
arr3 = np.zeros(n3, dtype = int)

for i in range(n1):
   arr3[i] = arr1[i]
for i in range(n2):
   arr3[n1+i] = arr2[i]

arr3.sort()
for i in arr3:
   outp.write(f"{i} ")