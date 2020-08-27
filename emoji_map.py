from random import choice


EMOJI_MAP = {
    "a": [":a:", ":regional_indicator_a:"],
    "b": [":b:", ":regional_indicator_b:"],
    "c": [":star_and_crescent:", ":regional_indicator_c:"],
    "d": [":regional_indicator_d:"],
    "e": [":regional_indicator_e:"],
    "f": [":regional_indicator_f:"],
    "g": [":regional_indicator_g:"],
    "h": [":regional_indicator_h:"],
    "i": [":information_source:", ":regional_indicator_i:"],
    "j": [":regional_indicator_j:"],
    "k": [":regional_indicator_k:"],
    "l": [":regional_indicator_l:"],
    "m": [":m:", ":part_alternation_mark:", ":scorpius:", ":regional_indicator_m:"],
    "n": [":regional_indicator_n:"],
    "o": [":o2:", ":yin_yang:", ":globe_with_meridians:", ":regional_indicator_o:", ":cyclone:"],
    "p": [":parking:", ":regional_indicator_p:"],
    "q": [":regional_indicator_q:"],
    "r": [":regional_indicator_r:"],
    "s": [":regional_indicator_s:"],
    "t": [":cross:", ":regional_indicator_t:"],
    "u": [":regional_indicator_u:"],
    "v": [":aries:", ":regional_indicator_v:"],
    "w": [":regional_indicator_w:"],
    "x": [":x:", ":regional_indicator_x:", ":negative_squared_cross_mark:"],
    "y": [":regional_indicator_y:"],
    "z": [":regional_indicator_z:", ":zzz:"],
    "1": [":one:"],
    "2": [":two:"],
    "3": [":three:"],
    "4": [":four:"],
    "5": [":five:"],
    "6": [":six:"],
    "7": [":seven:"],
    "8": [":eight:"],
    "9": [":nine:"],
    "0": [":zero:"],
    "?": [":grey_question:", ":question:"],
    "!": [":grey_exclamation:", ":exclamation:"],
    "*": [":asterisk:"],
    "#": [":hash:"]
}

async def emojify_it(data):
    return "".join(
        [choice(EMOJI_MAP.get(i.lower(), " ")) for i in data]
        )


