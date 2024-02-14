import shutil
import os


def move_files_to_dir():
    """Move the files made into their respective directory"""
    current_dir = os.getcwd()
    dest1 = os.path.join(current_dir, "ticket_images")
    dest2 = os.path.join(current_dir, "checkout_doc")
    dest3 = os.path.join(current_dir, "parking_ticket_images")
    dest4 = os.path.join(current_dir, "receipts")

    dirs = [dest1, dest2, dest3, dest4]

    for d in dirs:
        if os.path.isdir(d):
            pass
        else:
            os.mkdir(d)

    files = os.listdir()
    for f in files:
        if f.startswith("ticket"):
            shutil.move(f, dest1)
        if f.startswith("checkout"):
            shutil.move(f, dest2)
        if f.startswith("parking"):
            shutil.move(f, dest3)
        if f.startswith("receipt"):
            shutil.move(f, dest4)
