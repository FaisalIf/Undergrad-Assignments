inp = open("input1b.txt", "r")
outp = open("output1b.txt", "w")

v, e = tuple(map(int, inp.readline().split(" ")))
di = {}

for i in range(v+1):
   di[i] = []

for i in range(e):
   a, b, c = tuple(map(int, inp.readline().split(" ")))
   if a in di:
      di[a].append((b, c))

for j, k in di.items():
   outp.write(f"{j}: ")
   
   if len(k) > 0:
      for i in range(len(k)):
         outp.write(f"{k[i]} ")
   outp.write("\n")