import os

# Create a directory named "Tests"
os.makedirs("Tests", exist_ok=True)

# Path for the new Python script
file_path = os.path.join("Tests", "test1.py")

# Write the Python script to generate the table of 5
with open(file_path, "w") as file:
    file.write("command=code\n")
    file.write("""\
for i in range(1, 11):
    print(f"5 x {i} = {5 * i}")
""")

# Execute the newly created Python script
os.system(f"python {file_path}")
