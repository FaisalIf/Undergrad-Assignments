inp = open('input3.txt', 'r')
outp = open('output3.txt', 'w')

n = int(inp.readline())
arr = list(map(int, inp.readline().split(" ")))

def merge(l, r):

   i, j, k = 0, 0, 0
   n1, n2, n3 = len(l), len(r), len(l)+len(r)
   q = [0]*n3
   count = 0

   while i<n1 and j<n2:
      if l[i] <= r[j]:
         q[k] = l[i]
         i += 1
      else:
         q[k] = r[j]
         j += 1
         count += n1-i
      k += 1
   
   while i<n1:
      q[k] = l[i]
      i += 1
      k += 1
   while j<n2:
      q[k] = r[j]
      j += 1
      k += 1
   
   return q, count

def merge_count(arr):

   if len(arr) == 1:
      return arr, 0
   
   mid = len(arr)//2
   left, left_count = merge_count(arr[:mid:])
   right, right_count = merge_count(arr[mid::])
   cross, cross_count = merge(left, right)

   return cross, left_count + right_count + cross_count

sorted_arr, inverse_count = (merge_count(arr))
outp.write(str(inverse_count))