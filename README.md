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

Import the Nijuuei.dxw file from the game's root folder. Right click the preset, press Modify and make sure the path points to `二重影.exe`.

Mount the game's second disc then go into the CDAudio tab, select the `Rip CD Audio` option in the `Generic` section and run the game once. DxWnd should dump the BGM to a folder named `Music` in the game's directory.

After that, unmount the second disc, set the CDAudio option in DxWnd to `Use audio files` and change the path to point to the nocd exe. You should now be able to play the game without needing to have the second disc mounted at all times.

### Linux troubleshooting
The game should run perfectly fine through Wine if you have Japanese fonts and locale properly set up (see [this](https://learnjapanese.moe/vn-linux/) guide). I last tested it on 10.0.

By default the font rendering is a bit messed up (see wiki as to why). Use the nocd exe to fix this.

As Wine has yet to implement ddraw7's WaitForVerticalBlank function, the game will run at an uncapped framerate, which is probably not something you want (see next section).

The in-game volume sliders don't work. If you think the music's too loud compared to the voices, go into the CDAudio tab, tick Set emulated CD volume, then go into the Sound tab and change CD volume to your liking.

### High refresh rates
Nijuuei's rendering is synced to your monitor's refresh rate. This is fine if you have a 60hz monitor, but it makes everything display way faster if your screen's refresh rate is higher than that. It leads to fading transitions between images being basically nonexistent, for example.

I don't use Windows all that much nowadays, so I wouldn't know what the best solution is to cap the framerate. Try your GPU's control panel or something like RivaTuner, I guess. If they don't budge, try going to the DirectX tab in the DxWnd preset's settings and changing the Renderer to D3D9, then go to the Video tab and lock the bit depth at 32bpp. This will make videos look weird, so preferably don't do it unless you absolutely have to.

If you're a Linux user and the way the graphics display bothers you, do the step mentioned just above with changing the renderer. Make a `dxvk.conf` file in Nijuuei's root directory, edit it and add `d3d9.maxFrameRate = 60` as the first line. If you have DXVK set up in your Wine prefix, this should properly cap the frame rate. Note that, much like this makes videos break on Windows, this is going to screw them up for Linux as well - the DirectX 9 renderer makes the screen go black when one plays and it stays that way until you restart.

As for why this happens, the videos use 8bpp images rather than the 32bpp color depth the rest of the game does. D3D9 doesn't play nice with that, for some reason. I should probably ask about that on the DxWnd support forum.


## Moekan
### Mikoto route + voice patch
Download [the main repo](https://github.com/Vast-eel/nijuuei-va/archive/refs/heads/main.zip) and extract it somewhere.

Download [Dreamcast assets](https://drive.google.com/drive/folders/1G2Le9os8uZhP1Gn_i5qpAwLGcpBzGVn2?usp=sharing) and the [latest patch release](https://github.com/Vast-eel/nijuuei-va/releases/latest). Put everything into a `Patch` folder inside the repo directory.

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