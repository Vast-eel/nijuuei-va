opcodes_nijuuei = {
    # -- Text --
    0x01: ('HH',  "line_set"),
    0x02: ('H',  "name_set"),
    0x03: ('',  "name_clear"),
    0x04: ('HH',  "pis_set"),
    0x05: ('',  "nvl_line_clear"),
    0x06: ('IH',  "jump_choice"),
    0x07: ('I',  "jump_auto"),
    0x08: ('',  "nvl_on"),
    0x09: ('',  "adv_on"),
    0x0A: ('H',  "ksd_set"),
    0x0B: ('',  "ecchi_end"),
    0x0C: ('',  "game_over"),
    0x0D: ('',  "ksd_end"),

    # -- Graphics --
    # Layer 1: Fullscreen backgrounds/CGs
    0x0E: ('hh',  "kgd_layer1_set"),
    0x0F: ('',  "kgd_layer1_display"),
    0x10: ('',  "kgd_layer1_blackout"),
    0x11: ('h',  "kgd_layer1_clear"),
    0x12: ('',  "kgd_layer1_fadein"),

    # Layer 2: Smaller elements (island backgrounds, textbox, etc)
    0x13: ('hh',  "kgd_layer2_set"),
    0x14: ('',  "kgd_layer2_display"),
    0x15: ('',  "kgd_layer2_clear"),
    0x16: ('h',  "kgd_layer2_fade_unk"),
    0x17: ('',  "kgd_layer2_fadein"),

    # Layer 3: Character sprites
    0x18: ('hh',  "kgd_layer3_set"),
    0x19: ('HiiiiII',  "kgd_layer3_param"),
    0x1A: ('h',  "kgd_layer3_display"),
    0x1B: ('h',  "kgd_layer3_fadeout"),
    0x1C: ('h',  "kgd_layer3_clear"),

    # Blitting?
    # 002.ksd at 0x3330
    0x1D: ('hh',  "kgd_layer1_blit"),
    0x1E: ('hh',  "kgd_layer2_blit"),

    # -- Progression flags --
    # 0 = sae, 1 = fuurei, 4 = kikyou, 5 = mikoto
    0x1F: ('h',  "section_jump_branch1"),
    0x20: ('h',  "section_jump_branch2"),
    0x21: ('h',  "gallery_unlock"),
    #0x22: ('',  "unused?"),
    0x23: ('IH',  "jump_branch1"),
    0x24: ('IH',  "jump_branch2"),
    0x25: ('h',  "affection_plus"),
    0x26: ('h',  "affection_minus"),
    0x27: ('h',  "affection_ecchi"), # used only in 036 for mikoto
    0x28: ('hh',  "route_confirm"), # used only in 038
    0x29: ('IH',  "jump_route_038"), # used only in 038
    #0x2A: ('',  "unused?"),
    0x2B: ('IHIH',  "jump_route_036"), # another mikoto-only flag
    #0x2C: ('',  "unused?"),
    #0x2D: ('',  "unused?"),
    #0x2E: ('',  "unused?"),
    0x2F: ('IHIH',  "jump_route"),

    # -- Audio --
    0x30: ('h',  "music_play"),
    0x31: ('',  "music_stop"),
    #0x32: ('',  "unused?") - crash with a message about CD, music related?
    #0x33: ('',  "unused?"),
    0x34: ('hh',  "sfx_set"),
    0x35: ('h',  "sfx_play"),
    0x36: ('h',  "sfx_loop1"),
    0x37: ('h',  "sfx_loop2"),
    0x38: ('h',  "sfx_stop"),

    # -- Graphical effects --
    0x39: ('h',  "kgd_layer1_crossfade"),
    0x3A: ('h',  "kgd_layer2_crossfade"),
    0x3B: ('h',  "kgd_layer3_crossfade"),
    0x3C: ('h',  "kgd_layer1_fx"), # 5 = screenshake?

    # -- Other --
    0x3D: ('',  "fight_end"), # enables saving
    0x3E: ('',  "fight_start"), # disables saving
    0x3F: ('I',  "jump_fight_failure"),
    0x40: ('',  "op_play"),
    0x41: ('h',  "anim_play"),
    0x42: ('',  "ed_play"),
    0x43: ('',  "force_save_menu"),
    0x44: ('I',  "wait"),
}


opcodes_moekan = {
    # -- Text --
    0x01: ('HH',  "line_set"),
    0x02: ('h',  "voice_play"),
    0x03: ('h',  "name_set"),
    0x04: ('',  "name_clear"),
    0x06: ('',  "nvl_line_clear"),
    0x07: ('h',  "story_progress"),
    0x08: ('IH',  "jump_choice"),
    0x09: ('I',  "jump_auto"),
    0x0A: ('',  "nvl_on"),
    0x0B: ('',  "adv_on"),
    0x0C: ('h',  "ksd_set"),
    0x0D: ('',  "ecchi_end"),
    0x0E: ('',  "route_end"),
    0x0F: ('',  "ksd_end"),
    0x10: ('i',  "wait"),

    # -- Graphics --
    # Layer 1: Fullscreen backgrounds/CGs
    0x16: ('hh',  "kgd_layer1_set"),
    0x17: ('',  "kgd_layer1_display"),
    0x19: ('h',  "kgd_layer1_clear"),
    0x1A: ('',  "kgd_layer1_unk1"),

    # Layer 2: Date in the upper right of the screen
    # Gets two opcodes later on. Would be more sensible to swap layers 2 and 3 naming-wise
    # but I wanted to keep it consistent between games

    # Layer 3: Character sprites
    0x1B: ('hh',  "kgd_layer3_set"),
    0x1C: ('HiiiiII',  "kgd_layer3_param"),
    0x1D: ('h',  "kgd_layer3_display"),
    0x1E: ('h',  "kgd_layer3_fadeout"),
    0x1F: ('h',  "kgd_layer3_clear"),
    0x20: ('hh',  "kgd_layer1_solidcolor"),
    0x21: ('hhhh',  "kgd_layer3_crossfade"),

    # -- Progression flags --
    0x23: ('h',  "unk2"),
    0x24: ('h',  "unk3"),
    0x25: ('h',  "gallery_unlock"),
    0x26: ('h',  "nijuubako_opcode01"),
    0x27: ('ih',  "jump_type1"),
    0x28: ('ih',  "jump_type2"),
    0x29: ('h',  "unk4"),
    0x2A: ('h',  "unk5"),
    0x2B: ('hhhh',  "unk6"),
    0x2D: ('ih',  "jump_type3"),
    # 00 - rinia
    # haven't tested the ones below
    # 01 - kazusa?
    # 02 - fuyuha?
    # 03 - suzuki?
    # 04 - kirishima?
    0x2F: ('ihhhh',  "jump_type4"),
    0x30: ('ihhhh',  "jump_type5"),
    0x31: ('ihhhh',  "jump_type6"),
    0x33: ('ihhhh',  "jump_type7"),

    # -- Audio --
    0x38: ('h',  "music_play_moekan"),
    0x39: ('',  "music_stop1"),
    0x3A: ('',  "music_stop2"),
    0x3B: ('hh',  "sfx_set"),
    0x3C: ('hh',  "sfx_play"),
    0x3D: ('h',  "sfx_loop"),
    0x3E: ('h',  "sfx_stop"),
    0x3F: ('h',  "sfx_unset"),

    # -- Graphical effects --
    0x41: ('hh',  "kgd_layer1_crossfade"),
    0x42: ('h',  "kgd_layer3_unk7"),
    0x43: ('h',  "kgd_layer1_fx"),

    # -- Other --
    0x44: ('h',  "kqd_display"),
    0x4A: ('',  "nijuubako_opcode02"),
    0x4C: ('',  "choice_dialog_end"),
    0x4D: ('h',  "kgd_layer2_set_moekan"),
    0x4E: ('',  "kgd_layer2_clear"),
    0x4F: ('H',  "movie_play"),
    0x50: ('',  "unk8"),
    0x52: ('ih',  "jump_rinia_bad_end"),
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