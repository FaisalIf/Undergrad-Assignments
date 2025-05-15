inp = open('input4.txt', 'r')
outp = open('output4.txt', 'w')

n = int(inp.readline())
arr = list(map(int, inp.readline().split(" ")))

def max(a, b):
   if a >= b:
      return a
   return b
   
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


def merge_count(arr):

   if len(arr) == 1:
      return arr, 0
   
   mid = len(arr)//2
   left, leftmax = merge_count(arr[:mid:])
   right, rightmax = merge_count(arr[mid::])
   temp1 = left[-1]+right[0]*right[0]
   temp2 = left[-1]+right[-1]*right[-1]
   
   return merge(left, right), max(max(temp1, temp2), max(leftmax, rightmax))

sorted_arr, maximum = merge_count(arr)
outp.write(str(maximum))