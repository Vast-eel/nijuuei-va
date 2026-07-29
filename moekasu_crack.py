from pathlib import Path
from shutil import rmtree
from aod_tool import aod_extract

setup_file = Path("setup.sys")
sow_file = Path("SoW.aod")

if setup_file.exists() or sow_file.exists():
    if not sow_file.exists():
        setup_file.move(sow_file)
    aod_extract(sow_file)
    Path("SoW/SoW.exe").copy("SoW.exe")
    sow_file.move("aod/SoW.aod")
    rmtree("SoW")
    # if the save folder is missing the game silently crashes
    Path("save").mkdir(parents=True, exist_ok=True)