def bubble_sort(arr):

   flag = True
   while flag:
      flag = False
      for i in range(1, len(arr)):
         if arr[i-1] > arr[i]:
            flag = True
            arr[i-1], arr[i] = arr[i], arr[i-1]

   return arr

inp = open("input2.txt", "r")
outp = open("output2.txt", "w")

for count, line in enumerate(inp):

   if count % 2 == 0:
      continue
   
   arr = list(map(int, line.split(" ")))
   arr = bubble_sort(arr)
            
   outp.write(" ".join(map(str, arr)) + "\n")