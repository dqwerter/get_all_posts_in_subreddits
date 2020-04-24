import os
while(True):
    path = input("Enter the path")
    if(os.path.isdir(path)):
        break
    else:
        print("Entered path is wrong!")
for root,dirs,files in os.walk(path):
    for name in files:
        filename = os.path.join(root,name)
        if os.stat(filename).st_size == 0:
            print(" Removing ",filename)
            os.remove(filename)
