opcodes_nijuuei = {
    # -- Text --
    0x0100: ('HH',  "line_set"),
    0x0200: ('H',  "name_set"),
    0x0300: ('',  "name_clear"),
    0x0400: ('HH',  "pis_set"),
    0x0500: ('',  "nvl_line_clear"),
    0x0600: ('IH',  "jump_choice"),
    0x0700: ('I',  "jump_auto"),
    0x0800: ('',  "nvl_on"),
    0x0900: ('',  "adv_on"),
    0x0A00: ('H',  "ksd_set"),
    0x0B00: ('',  "ecchi_end"),
    0x0C00: ('',  "game_over"),
    0x0D00: ('',  "ksd_end"),

    # -- Graphics --
    # Layer 1: Fullscreen backgrounds/CGs
    0x0E00: ('hh',  "kgd_layer1_set"),
    0x0F00: ('',  "kgd_layer1_display"),
    0x1000: ('',  "kgd_layer1_blackout"),
    0x1100: ('h',  "kgd_layer1_clear"),
    0x1200: ('',  "kgd_layer1_fadein"),

    # Layer 2: Smaller elements (island backgrounds, textbox, etc)
    0x1300: ('hh',  "kgd_layer2_set"),
    0x1400: ('',  "kgd_layer2_display"),
    0x1500: ('',  "kgd_layer2_clear"),
    0x1600: ('h',  "kgd_layer2_fade_unk"),
    0x1700: ('',  "kgd_layer2_fadein"),

    # Layer 3: Character sprites
    0x1800: ('hh',  "kgd_layer3_set"),
    0x1900: ('HiiiiII',  "kgd_layer3_param"),
    0x1A00: ('h',  "kgd_layer3_display"),
    0x1B00: ('h',  "kgd_layer3_fadeout"),
    0x1C00: ('h',  "kgd_layer3_clear"),

    # Blitting?
    # 002.ksd at 0x3330
    0x1D00: ('hh',  "kgd_layer1_blit"),
    0x1E00: ('hh',  "kgd_layer2_blit"),

    # -- Progression flags --
    # 0 = sae, 1 = fuurei, 4 = kikyou, 5 = mikoto
    0x1F00: ('h',  "section_jump_branch1"),
    0x2000: ('h',  "section_jump_branch2"),
    0x2100: ('h',  "gallery_unlock"),
    #0x2200: ('',  "unused?"),
    0x2300: ('IH',  "jump_branch1"),
    0x2400: ('IH',  "jump_branch2"),
    0x2500: ('h',  "affection_plus"),
    0x2600: ('h',  "affection_minus"),
    0x2700: ('h',  "affection_ecchi"), # used only in 036 for mikoto
    0x2800: ('hh',  "route_confirm"), # used only in 038
    0x2900: ('IH',  "jump_route_038"), # used only in 038
    #0x2A00: ('',  "unused?"),
    0x2B00: ('IHIH',  "jump_route_036"), # another mikoto-only flag
    #0x2C00: ('',  "unused?"),
    #0x2D00: ('',  "unused?"),
    #0x2E00: ('',  "unused?"),
    0x2F00: ('IHIH',  "jump_route"),

    # -- Audio --
    0x3000: ('h',  "music_play"),
    0x3100: ('',  "music_stop"),
    #0x3200: ('',  "unused?") - crash with a message about CD, music related?
    #0x3300: ('',  "unused?"),
    0x3400: ('hh',  "sfx_set"),
    0x3500: ('h',  "sfx_play"),
    0x3600: ('h',  "sfx_loop1"),
    0x3700: ('h',  "sfx_loop2"),
    0x3800: ('h',  "sfx_stop"),

    # -- Graphical effects --
    0x3900: ('h',  "kgd_layer1_crossfade"),
    0x3A00: ('h',  "kgd_layer2_crossfade"),
    0x3B00: ('h',  "kgd_layer3_crossfade"),
    0x3C00: ('h',  "kgd_layer1_fx"), # 5 = screenshake?

    # -- Other --
    0x3D00: ('',  "fight_end"), # enables saving
    0x3E00: ('',  "fight_start"), # disables saving
    0x3F00: ('I',  "jump_fight_failure"),
    0x4000: ('',  "op_play"),
    0x4100: ('h',  "anim_play"),
    0x4200: ('',  "ed_play"),
    0x4300: ('',  "force_save_menu"),
    0x4400: ('I',  "wait"),
}


opcodes_moekan = {
    # -- Text --
    0x0100: ('HH',  "line_set"),
    0x0200: ('h',  "voice_play"),
    0x0300: ('h',  "name_set"),
    0x0400: ('',  "name_clear"),
    0x0600: ('',  "nvl_line_clear"),
    0x0700: ('h',  "story_progress"),
    0x0800: ('IH',  "jump_choice"),
    0x0900: ('I',  "jump_auto"),
    0x0A00: ('',  "nvl_on"),
    0x0B00: ('',  "adv_on"),
    0x0C00: ('h',  "ksd_set"),
    0x0D00: ('',  "ecchi_end"),
    0x0E00: ('',  "route_end"),
    0x0F00: ('',  "ksd_end"),
    0x1000: ('i',  "wait"),

    # -- Graphics --
    # Layer 1: Fullscreen backgrounds/CGs
    0x1600: ('hh',  "kgd_layer1_set"),
    0x1700: ('',  "kgd_layer1_display"),
    0x1900: ('h',  "kgd_layer1_clear"),
    0x1A00: ('',  "kgd_layer1_unk1"),

    # Layer 2: Date in the upper right of the screen
    # Gets two opcodes later on. Would be more sensible to swap layers 2 and 3 naming-wise
    # but I wanted to keep it consistent between games

    # Layer 3: Character sprites
    0x1B00: ('hh',  "kgd_layer3_set"),
    0x1C00: ('HiiiiII',  "kgd_layer3_param"),
    0x1D00: ('h',  "kgd_layer3_display"),
    0x1E00: ('h',  "kgd_layer3_fadeout"),
    0x1F00: ('h',  "kgd_layer3_clear"),
    0x2000: ('hh',  "kgd_layer1_solidcolor"),
    0x2100: ('hhhh',  "kgd_layer3_crossfade"),

    # -- Progression flags --
    0x2300: ('h',  "unk2"),
    0x2400: ('h',  "unk3"),
    0x2500: ('h',  "gallery_unlock"),
    0x2600: ('h',  "nijuubako_opcode01"),
    0x2700: ('ih',  "jump_type1"),
    0x2800: ('ih',  "jump_type2"),
    0x2900: ('h',  "unk4"),
    0x2A00: ('h',  "unk5"),
    0x2B00: ('hhhh',  "unk6"),
    0x2D00: ('ih',  "jump_type3"),
    # 00 - rinia
    # haven't tested the ones below
    # 01 - kazusa?
    # 02 - fuyuha?
    # 03 - suzuki?
    # 04 - kirishima?
    0x2F00: ('ihhhh',  "jump_type4"),
    0x3000: ('ihhhh',  "jump_type5"),
    0x3100: ('ihhhh',  "jump_type6"),
    0x3300: ('ihhhh',  "jump_type7"),

    # -- Audio --
    0x3800: ('h',  "music_play_moekan"),
    0x3900: ('',  "music_stop1"),
    0x3A00: ('',  "music_stop2"),
    0x3B00: ('hh',  "sfx_set"),
    0x3C00: ('hh',  "sfx_play"),
    0x3D00: ('h',  "sfx_loop"),
    0x3E00: ('h',  "sfx_stop"),
    0x3F00: ('h',  "sfx_unset"),

    # -- Graphical effects --
    0x4100: ('hh',  "kgd_layer1_crossfade"),
    0x4200: ('h',  "kgd_layer3_unk7"),
    0x4300: ('h',  "kgd_layer1_fx"),

    # -- Other --
    0x4400: ('h',  "kqd_display"),
    0x4A00: ('',  "nijuubako_opcode02"),
    0x4C00: ('',  "choice_dialog_end"),
    0x4D00: ('h',  "kgd_layer2_set_moekan"),
    0x4E00: ('',  "kgd_layer2_clear"),
    0x4F00: ('H',  "movie_play"),
    0x5000: ('',  "unk8"),
    0x5200: ('ih',  "jump_rinia_bad_end"),
}


jump_opcodes = (
    "jump_choice",
    "jump_auto",
    "jump_branch1",
    "jump_branch2",
    "jump_route_038",
    "jump_route_036",
    "jump_route",
    "jump_fight_failure",

    "jump_type1",
    "jump_type2",
    "jump_type3",
    "jump_type4",
    "jump_type5",
    "jump_type6",
    "jump_type7",
    "jump_rinia_bad_end"
)


string_opcodes = (
    "line_set",
    "name_set",
    "jump_choice",
    "ksd_set",
    "kgd_layer1_set",
    "kgd_layer2_set",
    "kgd_layer3_set",
    "sfx_set",
    "anim_play",

    "kqd_display",

    "voice_play",
    "music_play_moekan",
    "kgd_layer2_set_moekan",
    "movie_play"
)