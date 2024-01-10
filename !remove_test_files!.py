import os

current_dir = os.getcwd()

dest1 = os.path.join(current_dir, "ticket_images")
dest2 = os.path.join(current_dir, "checkout_doc")
dest3 = os.path.join(current_dir, "parking_ticket_images")
dest4 = os.path.join(current_dir, "receipts")

dirs = [dest1, dest2, dest3, dest4]

for d in dirs:
    files = os.listdir(d)
    for file in files:
        f = os.path.join(d, file)
        os.remove(f)

files_dir = os.listdir()
for file in files_dir:
    if file.endswith(".json"):
        os.remove(file)
