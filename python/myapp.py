# print("Program to sun two numbers")
# num1=int(input("Enter number 1"))
# num2=int(input("Enter number 2"))

# res=num1+num2

# print(f"Sum of two numbers are {res}")

# user_name = input("Enter your name to store in file or enter to proceed: ")
# if user_name:
#     with open('/myapp/user_info.txt', 'a') as file:
#         file.write(user_name + "\n")

# show_info = input("Do you want to see all user names? y/n: ")
# if show_info == 'y':
#     try:
#         with open('/myapp/user_info.txt', 'r') as file:
#             content = file.readlines()
#     except Exception as e:
#         print(e, type(e))
#     else:
#         for line in content:
#             print(f'{line.rstrip()}')

try:
    with open('server.txt', 'r') as file:
        content = file.readlines()
except Exception as e:
    print(e, type(e))
else:
    for line in content:
        print(f'{line.rstrip()}')