import os

print("=================================")
print(os.getcwd())
print("=================================")

for root, dirs, files in os.walk(os.getcwd()):
    if root == os.getcwd():
        print("=================================")
        print(root)
        print("=================================")
        print(dirs)
        print("=================================")
        print(files)
        print("=================================")
