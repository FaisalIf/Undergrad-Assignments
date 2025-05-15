inp = open('input1a.txt','r')
outp = open('output1a.txt','w')

n = int(inp.readline())

for i in range(n):
  num = int(inp.readline())
  if num % 2 == 0:
    outp.write(f'{num} is an Even number.\n')
  else:
    outp.write(f'{num} is an Odd number.\n')