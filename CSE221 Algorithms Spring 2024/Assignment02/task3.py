inp = open("input3.txt", "r")
outp = open("output3.txt", "w")

n = int(inp.readline())
arr = []
for i in range(n):
   arr.append(tuple(map(int, inp.readline().split(" "))))

swap = True
while swap:
   swap = False
   for i in range(1, len(arr)):
      if arr[i-1][1] > arr[i][1]:
         arr[i-1], arr[i] = arr[i], arr[i-1]
         swap = True

work = [arr[0]]
c = 0
for i in range(1, len(arr)):
   if arr[i][0] >= work[c][1]:
      work.append(arr[i])
      c += 1

outp.write(str(c+1)+"\n")
for i, j in work:
   outp.write(f"{i} {j}\n")