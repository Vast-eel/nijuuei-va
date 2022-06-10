# nijuuei-va
Voice patch for the PC version of 二重影.

A juryrigged port of the voices from the Dreamcast version. Barely tested, but it's gotten to the point where there aren't catastrophic failures on day 2, so I uploaded it.

Currently works well up until day 6 (017.ksd).

## How-to
**Please keep a backup of the original files and have separate save files for the start of each day so you can revert in case you can't progress!!**

Press the Code button and Download ZIP. Extract the Ksd folder to the game folder and overwrite when asked. Download [this](https://drive.google.com/drive/folders/1MMvA8k8tal3h6U4hwnW04e3lv066tYhq) and stick the Vo folder in the game folder as well. 

## Caveats
* If you load a save game for the second time in a session (first time works just fine) and get to a point where a voice line is supposed to play, the game may crash. I have NO fucking idea why this happens, it's inconsistent.
I came across an instruction that stops a looping sound effect, maybe it can be made to work for oneshot sfx too? Probably not, but it's worth testing eventually.

* Expect a bunch of mismatched lines. The matching script I wrote did not take nametags into account to make it easier for me so if multiple characters share a line written the exact same, mistakes are bound to happen. Work in progress.

* Similarly, there are bound to be unvoiced parts, too. For example, any lines with PIS (blue text) tags aren't voiced due to syntax differences at the moment.

* The nighttime part of day 4 (013.ksd) currently has a small desync where you get booted back to the mansion immediately after meeting Aya in the forest. You can progress just fine, you just skip an exploration screen or two.

* Picking anything other than the first choice in Fuurei's dialogue on day 5 (014.ksd) in front of the mansion causes the game to crash.

## FAQ
### HOW???
Hex editing and lots of patience. I'll document the process and some of the instructions I made sense of at some point. I'd like to upload the tools I made too, but currently my workflow is so messy if an experienced programmer saw it they'd strangle me with their bare hands immediately. I'd have to touch everything up a bit first.
### Dreamcast CGs/censored scenes when?
Sometime between the distant future and never. I have no idea how image formats work at all, let alone the one used in Nijuuei (aside from being able to figure out the header, at least), so the CGs are a no-go for the time being. I would definitely like to tackle them sometime, though.

The non-H Dreamcast scenes would require me to have a much better grasp of both the PC and Dreamcast script files than I currently have. It'd require much more time than I'm willing to invest right now. Maybe someday, when I have more free time and get all the main issues out of the way, but no promises.

## No-CD dxwnd preset
tbd
