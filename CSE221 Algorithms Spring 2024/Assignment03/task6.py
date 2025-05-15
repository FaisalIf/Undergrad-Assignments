inp = open('input6.txt', 'r')
outp = open('output6.txt', 'w')

n = int(inp.readline()[:1:])
arr = list(map(int, inp.readline().split(" ")))
query = int(inp.readline()[:1:])
q_list = [int(inp.readline()) for i in range(query)]

def partition(arr, p, r):

   x = arr[r]
   i = p-1
   for j in range(p, r):
      if arr[j] <= x:
         i += 1
         arr[i], arr[j] = arr[j], arr[i]

   arr[i+1], arr[r] = arr[r], arr[i+1]
   return i+1

def quicksearch(arr, p, r, k):

   if p < r:
      q = partition(arr, p, r)
      
      if k-1 == q:
         return arr[q]
      elif k-1 < q:
         quicksearch(arr, p, q-1, k)
      else:
         quicksearch(arr, q+1, r, k)

for i in range(query):
   j = q_list[i]
   quicksearch(arr, 0, len(arr)-1, j)
   outp.write(str(arr[j-1])+"\n")