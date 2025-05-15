inp = open("input4.txt", "r")
outp = open("output4.txt", "w")

n, p = tuple(map(int, inp.readline().split(" ")))
arr = [(tuple(map(int, inp.readline().split(" ")))) for i in range(n)]

swap = True
while swap:
   swap = False
   for i in range(1, len(arr)):
      if arr[i-1][1] > arr[i][1]:
         arr[i-1], arr[i] = arr[i], arr[i-1]
         swap = True

work = [(0,0) for i in range(p)]
count = 0
for i in range(len(arr)):

   temp = None
   curr = 0
   for j in range(len(work)):

      if arr[i][0] >= work[j][1]:
         if not temp:
            temp = arr[i]
            curr = j
         elif work[j-1][1] < work[j][1]:
            curr = j

   if temp:
      work[curr] = temp
      count += 1

outp.write(str(count))