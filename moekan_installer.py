from pathlib import Path
import subprocess
import shutil
import tempfile

if not Path("Patch").exists() or not any(Path("Patch").iterdir()):
    print("Extract everything into a folder named \"Patch\" and run the script again.")
    exit()

moepath = input("Enter the path to Moekan's Dat folder: ")
moepath = Path(moepath)

with tempfile.TemporaryDirectory() as temp:
    archives = ["001", "005", "007"]

    print("Unpacking archives...")
    for archive in archives:
        subprocess.run(["python"] + ["dat_tool.py", "-e", "-m0", f"{moepath}/{archive}.dat", f"{temp}/{archive}"])

    print("Importing console assets...")
    for file in Path("Patch/Ksd").iterdir():
        shutil.copy(file, f"{temp}/001/{file.name}")
    for file in Path("Patch/Kgd").iterdir():
        shutil.copy(file, f"{temp}/005/{file.name}")
    for file in Path("Patch/Sounds/Mikoto").iterdir():
        shutil.copy(file, f"{temp}/007/{file.name}")
    for file in Path("Patch/Sounds/Oyaji").iterdir():
        shutil.copy(file, f"{temp}/007/{file.name}")

    print("Packing archives...")
    for archive in archives:
        subprocess.run(["python"] + ["dat_tool.py", "-i", "-m0", f"{temp}/{archive}"])

    print("Done! Check the Imported folder.")