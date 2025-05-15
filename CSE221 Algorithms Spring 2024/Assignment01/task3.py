def selection_sort(arr):

   for i in range(len(arr)):
      idx = i

      for j in range(i+1, len(arr)):
         id, number = arr[j]
         iid, inumber = arr[idx]

         if number == inumber and id < iid:
            idx = j
         elif number > inumber:
            idx = j

      if idx != i:
         arr[i], arr[idx] = arr[idx], arr[i]

   return arr

inp = open("input3.txt", "r")
outp = open("output3.txt", "w")
lines = inp.readlines()

for i in range(0, len(lines), 3):

   id_list = list(map(int, lines[i+1].split(" ")))
   number_list = list(map(int, lines[i+2].split(" ")))
   arr = []
   
   for j in range(len(id_list)):
      arr.append(((id_list[j]), number_list[j]))
   arr = selection_sort(arr)

   for key, val in arr:
      outp.write(f"ID: {key} Mark: {val}\n")
   
   outp.write("\n")