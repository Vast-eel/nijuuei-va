# nijuuei-va
Dreamcast content patches and rudimentary asset extraction tools for PC versions of KeroQ visual novels.

Partially based on [gscScriptCompAndDecompiler](https://github.com/TesterTesterov/gscScriptCompAndDecompiler).

## Nijuuei
### Voice patch
Save files from an unmodified version of the game may or may not crash depending on when you saved, so starting from the beginning is recommended.

Download [the voice files](https://drive.google.com/drive/folders/1MMvA8k8tal3h6U4hwnW04e3lv066tYhq?usp=sharing) and [new CGs](https://drive.google.com/drive/folders/1BjcOJ1DyLqLQnqyrM4gnU0PocGN4yKh8?usp=sharing) then put the folders in the Nijuuei root folder.

Download the script files from the Releases section and overwrite the files in the game's Ksd directory with the new files.

### QoL fixes
The game tends to crash or hang after animations on modern machines. To fix this, set the game to fullscreen (even if you want to play it windowed) then download [DxWnd](https://sourceforge.net/projects/dxwnd/) and [these](https://drive.google.com/drive/folders/1Nr5Qn2ZDqtreLOAUDnoEWtd0spksYvSF?usp=sharing) files.

Put the .exe file in the game's root folder and import the .dxw file in DxWnd.

Right click the preset, press Modify and change the path to the nocd .exe file where your game install is.

Go into the CDAudio tab and select the "Rip CD Audio" option and run the game once. After that, set it to "Use audio files". This way the game will use .wav files DxWnd puts in the root folder without needing to have the second disc inserted at all times.

### Linux troubleshooting
If you're running Nijuuei through DxWnd, make sure to disable the "Emulate Win9X heap" option in the Libs tab of the preset to prevent crashes.

Other than that, it should run perfectly fine through Wine if you have Japanese fonts and locale properly set up (see [this](https://learnjapanese.moe/vn-linux/) guide). I last tested it on 9.4 in WoW64 mode.

By default the font rendering is a bit messed up (see wiki as to why). Use the nocd exe to fix this.

As Wine has yet to implement ddraw7's WaitForVerticalBlank function, the game will run too fast for sprite transitions to properly display. You *can* force it to slow down by changing DxWnd's vsync mode to Frequency, but I wouldn't recommend it. You can have working transitions by setting the DxWnd renderer to D3D9, but this will make the game crash on animations as usual.

The in-game volume sliders don't work. If you think the music's too loud compared to the voices, go into the CDAudio tab, tick Set emulated CD volume, then go into the Sound tab and change CD volume to your liking.

## Moekan
### Mikoto route + voice patch
Download [the Python scripts](https://github.com/Vast-eel/nijuuei-va/archive/refs/heads/main.zip) from this repo and extract them somewhere.

Download the Dreamcast assets from [here](https://drive.google.com/drive/folders/1G2Le9os8uZhP1Gn_i5qpAwLGcpBzGVn2?usp=sharing) and the .zip file from the Releases section. Put everything into a "Patch" folder inside the python scripts directory.

The final directory structure should look like:
```
nijuuei-va-main
└── Patch
    ├── Kgd
    ├── Ksd
    └── Sounds
        ├── Mikoto
        └── Oyaji
```

Run the moekan_installer script and follow what it says.


## Editing
I've included the scripts written for the purposes of this patch. ksd_tool and kpd_tool are for the main scripts and Nijyuei.kpd, while dc_tool has two functions for getting voiced lines from the Dreamcast version's .BIN files and matching them with ksd_tool's decompiled scripts respectively. See the repo's wiki for technical details.

I've applied most of the Dreamcast version's script fixes to the PC version's files. The revised scripts are under Exported/Ksd/Base_Fixes. They're used as the base for the voice patch, the scripts of which you can see under Exported/Ksd/New_Content.