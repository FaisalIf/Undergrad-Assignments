inp = open("input1b.txt", "r")
outp = open("output1b.txt", "w")

n = int(inp.readline())

for i in range(n):
  
  li = inp.readline().split(" ")
  if li[2] == "+":
    outp.write(f"The result of {li[1]} {li[2]} {li[3].strip()} is {int(li[1]) + int(li[3])}\n")
  elif li[2] == "-":
    outp.write(f"The result of {li[1]} {li[2]} {li[3].strip()} is {int(li[1]) - int(li[3])}\n")
  elif li[2] == "*":
    outp.write(f"The result of {li[1]} {li[2]} {li[3].strip()} is {int(li[1]) * int(li[3])}\n")
  elif li[2] == "/":
    outp.write(f"The result of {li[1]} {li[2]} {li[3].strip()} is {int(li[1]) / int(li[3])}\n")