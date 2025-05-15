inp = open('input5.txt', 'r')
outp = open('output5.txt', 'w')

n = int(inp.readline())
arr = list(map(int, inp.readline().split(" ")))

def partition(arr, p, r):

   x = arr[p]
   i = p
   for j in range(i+1, r):
      if arr[j] <= x:
         i += 1
         arr[i], arr[j] = arr[j], arr[i]

   arr[p], arr[i] = arr[i], arr[p]
   return i

def quickSort(arr, p, r):

   if p >= r:
      return arr
   
   q = partition(arr, p, r)
   quickSort(arr, p, q)
   quickSort(arr, q+1, r)

p, r = 0, len(arr)-1
quickSort(arr, p, r)
for i in arr:
   outp.write(f"{i} ")