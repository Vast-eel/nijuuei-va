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
    print("Unpacking archives...")
    subprocess.check_call([f"python dat_tool.py -e -m0 {moepath}/001.dat {temp}/001"], shell=True)
    subprocess.check_call([f"python dat_tool.py -e -m0 {moepath}/005.dat {temp}/005"], shell=True)
    subprocess.check_call([f"python dat_tool.py -e -m0 {moepath}/007.dat {temp}/007"], shell=True)

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
    subprocess.check_call([f"python dat_tool.py -i -m0 {temp}/001"], shell=True)
    subprocess.check_call([f"python dat_tool.py -i -m0 {temp}/005"], shell=True)
    subprocess.check_call([f"python dat_tool.py -i -m0 {temp}/007"], shell=True)

    print("Done! Check the Imported folder.")

# /home/vasteel/.src/.personal/nje/Moekan/Dat/