def selection_sort(arr):

   for i in range(len(arr)):
      idx = i
      
      for j in range(i+1, len(arr)):
         name, time, des = arr[j]
         iname, itime, ides = arr[idx]

         if name == iname and time == itime and des < ides:
            idx = j
         elif name == iname and time > itime:
            idx = j
         elif name < iname:
            idx = j

      if idx != i:
         arr[i], arr[idx] = arr[idx], arr[i]

   return arr

inp = open("input4.txt", "r")
outp = open("output4.txt", "w")
n = int(inp.readline())
arr = []

for i in range(n):
   temp = list(inp.readline().split(" "))
   arr.append((temp[0], temp[6], temp[4]))

arr = selection_sort(arr)
li = [" will departure for ", " at "]
for i in arr:
   outp.write(i[0]+li[0]+i[2]+li[1]+i[1])