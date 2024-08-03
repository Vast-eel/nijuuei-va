# nijuuei-va
Dreamcast content patches and rudimentary asset extraction tools for PC versions of KeroQ visual novels.

Vanilla save files may crash depending on where you saved, so starting from scratch after installing the patches is recommended.

Partially based on [gscScriptCompAndDecompiler](https://github.com/TesterTesterov/gscScriptCompAndDecompiler).

## Nijuuei
### Voice patch

Download [Dreamcast assets](https://drive.google.com/drive/folders/1-cwaKLra23hldfvhY3V4RxOwUHBt1RGB?usp=sharing) and put everything in Nijuuei's root folder.

Next, download the [latest patch release](https://github.com/Vast-eel/nijuuei-va/releases/latest) and overwrite the files in the game's Ksd directory with the new files.

### QoL fixes
The game tends to crash or hang after animations on modern machines. To fix this, set the game to fullscreen (even if you want to play it windowed) and download [DxWnd](https://sourceforge.net/projects/dxwnd/).

Import the Nijuuei.dxw file from the game's root folder. Right click the preset, press Modify and make sure the path points to 二重影.exe.

Mount the game's second disc then go into the CDAudio tab, select the "Rip CD Audio" option in the "Generic" section and run the game once. DxWnd should dump the BGM to a folder named "Music" in the game's directory.

After that, unmount the second disc, set the CDAudio option in DxWnd to "Use audio files" and change the path to point to the nocd exe. You should now be able to play the game without needing to have the second disc mounted at all times.

### Linux troubleshooting
If you're running Nijuuei through DxWnd, make sure to disable the "Emulate Win9X heap" option in the Libs tab of the preset to prevent crashes.

Other than that, it should run perfectly fine through Wine if you have Japanese fonts and locale properly set up (see [this](https://learnjapanese.moe/vn-linux/) guide). I last tested it on 9.4 in WoW64 mode.

By default the font rendering is a bit messed up (see wiki as to why). Use the nocd exe to fix this.

As Wine has yet to implement ddraw7's WaitForVerticalBlank function, the game will run too fast for sprite transitions to properly display. You *can* force it to slow down by changing DxWnd's vsync mode to Frequency, but I wouldn't recommend it. You can have working transitions by setting the DxWnd renderer to D3D9, but this will make the game crash on animations as usual.

The in-game volume sliders don't work. If you think the music's too loud compared to the voices, go into the CDAudio tab, tick Set emulated CD volume, then go into the Sound tab and change CD volume to your liking.

## Moekan
### Mikoto route + voice patch
Download [the main repo](https://github.com/Vast-eel/nijuuei-va/archive/refs/heads/main.zip) and extract it somewhere.

Download [Dreamcast assets](https://drive.google.com/drive/folders/1G2Le9os8uZhP1Gn_i5qpAwLGcpBzGVn2?usp=sharing) and the [latest patch release](https://github.com/Vast-eel/nijuuei-va/releases/latest). Put everything into a "Patch" folder inside the repo directory.

The final directory structure should look like this:
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