inp = open('input2.txt', 'r')
outp = open('output2.txt', 'w')

n = int(inp.readline())
arr = list(map(int, inp.readline().split(" ")))

def findmax(a, b):
   if a >= b:
      return a
   return b

def maximum(arr, start, end):

   if start == end:
      return arr[start]
   
   mid = (start+end)//2
   left = maximum(arr, start, mid)
   right = maximum(arr, mid+1, end)
   
   return findmax(left, right)

start = 0
end = len(arr)-1
outp.write(str(maximum(arr, start, end)))