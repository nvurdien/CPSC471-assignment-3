import os

pid = os.fork()

if pid == 0:
    print("Hey, I am the child")
else:
    print("I a parent")
