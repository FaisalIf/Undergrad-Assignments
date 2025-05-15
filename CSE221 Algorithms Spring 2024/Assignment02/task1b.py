inp = open("input1.txt", "r")
outp = open("output1.txt", "w")

n, s = tuple(map(int, inp.readline().split(" ")))
arr = list(map(int, inp.readline().split(" ")))
flag = False
p1, p2 = 0, len(arr)-1

while p1 < p2:

   if arr[p1]+arr[p2] == s:
      outp.write(f"{p1+1} {p2+1}\n")
      flag = True
      
   if arr[p1] < s:
      p1 += 1
   else:
      p2 -= 1

if flag == False:
   outp.write("IMPOSSIBLE")