inp = open('input1.txt', 'r')
outp = open('output1.txt', 'w')

n = int(inp.readline())
arr = list(map(int, inp.readline().split(" ")))

def merge(l, r):

   i, j, k = 0, 0, 0
   n1, n2, n3 = len(l), len(r), len(l)+len(r)
   q = [0]*n3

   while i<n1 and j<n2:
      if l[i] <= r[j]:
         q[k] = l[i]
         i += 1
      else:
         q[k] = r[j]
         j += 1
      k += 1

   while i<n1:
      q[k] = l[i]
      i += 1
      k += 1
   while j<n2:
      q[k] = r[j]
      j += 1
      k += 1
   
   return q

def mergeSort(arr):

   if len(arr) == 1:
      return arr
   
   mid = len(arr)//2
   left = mergeSort(arr[:mid:])
   right = mergeSort(arr[mid::])
   
   return merge(left, right)

arr1 = mergeSort(arr)
for i in arr1:
   outp.write(f"{i} ")