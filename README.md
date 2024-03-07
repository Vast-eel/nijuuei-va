# nijuuei-va
Voice patch and rudimentary asset extraction tools for the PC version of 二重影.

Partially based on [gscScriptCompAndDecompiler](https://github.com/TesterTesterov/gscScriptCompAndDecompiler).

## Installing
### Voice patch
Save files from an unmodified version of the game may or may not crash depending on when you saved, so starting from the beginning is recommended.

Download [this](https://drive.google.com/drive/folders/1MMvA8k8tal3h6U4hwnW04e3lv066tYhq?usp=sharing) and put the Vox folder in the Nijuuei root folder.

Download script files from the Releases section and overwrite the files in the game's Ksd directory with the new files.

### QoL fixes
The game tends to crash or hang after animations on modern machines. To fix this, set the game to fullscreen (even if you want to play it windowed) then download [DxWnd](https://sourceforge.net/projects/dxwnd/) and [these](https://drive.google.com/drive/folders/1Nr5Qn2ZDqtreLOAUDnoEWtd0spksYvSF?usp=sharing) files.

Put the .exe file in the game's root folder and import the .dxw file in DxWnd.

Right click the preset, press Modify and change the path to the nocd .exe file where your game install is.

Go into the CDAudio tab and select the "Rip CD Audio" option and run the game once. After that, set it to "Use audio files". This way the game will use .wav files DxWnd puts in the root folder without needing to have the second disc inserted at all times.

Due to running the game in fullscreen and forcibly windowing it with DxWnd, the right click menu will be misaligned with your mouse cursor. If this bothers you, disable the options that force windowing in the preset's properties and change the screen mode to windowed in-game. This will make the game go fullscreen for animations, though.

If you're playing the game on Linux, the game won't have sprite transitions due to ddraw7 functionality not implemented in Wine. Disable the "Emulate Win9X heap" option in the Libs tab to prevent crashes.

## Editing
I've included the scripts written for the purposes of this patch. ksd_tool and kpd_tool are for the main scripts and Nijyuei.kpd, while dc_tool has two functions for getting voiced lines from the Dreamcast version's .BIN files and matching them with ksd_tool's decompiled scripts respectively. See the repo's wiki for technical details.

I've applied most of the Dreamcast version's script fixes to the PC version's files. The revised scripts are under Ksd\Decompiled\DC_Fixes. They're used as the base for the voice patch, the scripts of which you can see under Ksd/Voiced.

The game automatically linebreaks text after 23 characters in dialogue boxes and after 48 in PIS text.

PIS tags (clickable blue text) need to start and end on even offsets to display properly.
