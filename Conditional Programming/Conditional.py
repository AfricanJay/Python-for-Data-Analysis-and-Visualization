import random

r = random.randint(20,34)
print(r)
if r < 25:
    print('A small number!')
elif r < 30:
    print('A moderately high number.')
else:
    print('A large number!')

a = random.randint(1,12)
b = random.randint(1,16)

print('a:', a)
print('b:', b)

if a > 6:
    print("'a' is large")
    if b > a:
        print('Both numbers are large.')
        print('Result: b is larger than a.')

  for i in range(20): # Remember: 20 is not included in the range! 
    if i%2 == 0: # The 'modulo' operator returns the integer part left after an integer division.
        print('Number %d is even.'% i)
    else:
        print('Number %d is odd.'% i)
for word in ['Business', 'analytics', 'with', 'Python']:
    print(word, len(word)) # functions can also be print inputs
list_capitals = []
for i in range(65,91):
    list_capitals.append(chr(i))
print(list_capitals)


for k, v in enumerate(list_capitals):
    print(k, v)

i = 0 # the counter
while i < 20:
    if i%2 == 0:
        print('Number %d is even.'% i)
    else:
        print('Number %d is odd.'% i)
    i += 1 # increment in Python (same as i++ in Java)
print('\nDone.') # Indented so that it will only print at the end.


from IPython.display import clear_output
import time

i = 1
while True: # This syntax makes it run forever, or untill manual interruption. 
    print(i)
    i += 1
    time.sleep(1)
    clear_output()
To interrupt the script in a code
