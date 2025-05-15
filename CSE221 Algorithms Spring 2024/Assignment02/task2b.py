import numpy as np

inp = open("input2.txt", "r")
outp = open("output2.txt", "w")

n1 = int(inp.readline())
arr1 = np.array(list(map(int, inp.readline().split(" "))))
n2 = int(inp.readline())
arr2 = np.array(list(map(int, inp.readline().split(" "))))
n3 = n1+n2
arr3 = np.zeros(n3, dtype = int)
i1, i2, i3 = 0, 0, 0

while i1 < n1 and i2 < n2:
   if arr1[i1] <= arr2[i2]:
      arr3[i3] = arr1[i1]
      i1 += 1
   else:
      arr3[i3] = arr2[i2]
      i2 += 1
   i3 += 1

while i1 < n1:
   arr3[i3] = arr1[i1]
   i1 += 1
   i3 += 1

while i2 < n2:
   arr3[i3] = arr2[i2]
   i2 += 1
   i3 += 1

for i in arr3:
   outp.write(f"{i} ")