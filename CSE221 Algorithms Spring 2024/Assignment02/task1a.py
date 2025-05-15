inp = open("input1.txt", "r")
outp = open("output1.txt", "w")

n, s = tuple(map(int, inp.readline().split(" ")))
arr = list(map(int, inp.readline().split(" ")))
flag = False

for i in range(len(arr)):

   if flag == True:
      break

   for j in range(i+1, len(arr)):
      if arr[i]+arr[j] == s:
         outp.write(f"{i+1} {j+1}\n")
         flag = True
         break

if flag == False:
   outp.write(f"IMPOSSIBLE")