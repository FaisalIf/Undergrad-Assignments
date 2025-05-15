import numpy as np

inp = open("input1a.txt", "r")
outp = open("output1a.txt", "w")

v, e = tuple(map(int, inp.readline().split(" ")))
arr = np.zeros((v+1, v+1), dtype = int)

for i in range(e):
  a, b, c = tuple(map(int, inp.readline().split(" ")))
  arr[a][b] = c

for i in range(v+1):
  for j in range(v+1):
    outp.write(str(arr[i][j])+" ")
  outp.write("\n")