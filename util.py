MOVES_FILE, ABILITIES_FILE = './data/moves.data', './data/abilities.data'

# TODO Optimize opponent/player
# Regex Log Messages
OPPONENT_MOVE = r'^The opposing (.*) used (.*)!$'
PLAYER_MOVE = r'^(.*) used (.*)!$'
OPPONENT_Z_MOVE = r'^The opposing .* unleashes its full-force Z-Move!The opposing (.*) used (.*)!$'
PLAYER_Z_MOVE = r'^.* unleashes its full-force Z-Move!(.*) used (.*)!$'
OPPONENT_DAMAGE = r'^\(The opposing (.*) lost (.*) of its health!\)$'
PLAYER_DAMAGE = r'^\((.*) lost (.*) of its health!\)$'
OPPONENT_STAT_DROP = r'^The opposing (.*)\'s (.*) fell!$'
PLAYER_STAT_DROP = r'^(.*)\'s (.*) fell!$'
OPPONENT_STAT_DROP_HARSH = r'^The opposing (.*)\'s (.*) fell harshly!$'
PLAYER_STAT_DROP_HARSH = r'^(.*)\'s (.*) fell harshly!$'
OPPONENT_STAT_RAISE = r'^The opposing (.*)\'s (.*) rose!$'
PLAYER_STAT_RAISE = r'^(.*)\'s (.*) rose!$'
OPPONENT_STAT_RAISE_DRAST = r'^The opposing (.*)\'s (.*) rose drastically!$'
PLAYER_STAT_RAISE_DRAST = r'^(.*)\'s (.*) rose drastically!$'
OPPONENT_STAT_RAISE_SHARP = r'^The opposing (.*)\'s (.*) rose sharply!$'
PLAYER_STAT_RAISE_SHARP = r'^(.*)\'s (.*) rose sharply!$'
OPPONENT_STAT_RAISE_WEAKNESS = r'^The Weakness Policy sharply raised the opposing (.*)\'s (.*)!$'
PLAYER_STAT_RAISE_WEAKNESS = r'^The Weakness Policy sharply raised (.*)\'s (.*)!$'
OPPONENT_SWITCH_1 = r'^.*withdrew (.*)!$'
OPPONENT_SWITCH_2 = r'^The opposing (.*) went back to.*!$'
PLAYER_SWITCH = r'^(.*), come back!$'
OPPONENT_SELECT = r'^.*sent out (.*)!$'
PLAYER_SELECT = r'^Go! (.*)!$'
OPPONENT_MEGA = r'^The opposing .*\'s .* is reacting to the Key Stone!The opposing (.*) has Mega Evolved into (.*)!$'
PLAYER_MEGA = r'^.*\'s .* is reacting to the Key Stone!(.*) has Mega Evolved into (.*)!$'
OPPONENT_RECOIL = r'^The opposing (.*) was damaged by the recoil!$'
PLAYER_RECOIL = r'^(.*) was damaged by the recoil!$'
OPPONENT_FAINT = r'^The opposing (.*) fainted!$'
PLAYER_FAINT = r'^(.*) fainted!$'
OPPONENT_DODGE = r'^The opponent (.*) avoided the attack!$'
PLAYER_DODGE = r'^(.*) avoided the attack!$'
OPPONENT_LEFTOVERS = r'^The opposing (.*) restored a little HP using its (.*)!$'
PLAYER_LEFTOVERS = r'^(.*) restored a little HP using its (.*)!$'
OPPONENT_SUBSTITUTE = r'^The substitute took damage for the opposing (.*)!$'
PLAYER_SUBSTITUTE = r'^The substitute took damage for (.*)!$'
OPPOSING_SUBSTITUTE_FADED = r'^The opposing (.*)\'s substitute faded!$'
PLAYER_SUBSTITUTE_FADED = r'^(.*)\'s substitute faded!$'
PLAYER_FRISK = r'^\[.*\'s Frisk\](.*) frisked the opposing (.*) and found its (.*)!$'
OPPONENT_BURNED = r'^The opposing (.*) was burned!$'
PLAYER_BURNED = r'^(.*) was burned!$'
OPPONENT_BURN = r'^The opposing (.*) was hurt by its burn!$'
PLAYER_BURN = r'^(.*) was hurt by its burn!$'
OPPONENT_BURN_HEAL = r'^The opposing (.*)\'s burn was healed!$'
PLAYER_BURN_HEAL = r'^(.*)\'s burn was healed!$'
OPPONENT_POISONED = r'^The opposing (.*) was poisoned!$'
PLAYER_POISONED = r'^(.*) was poisoned!$'
OPPONENT_TOXIC = r'^The opposing (.*) was badly poisoned!$'
PLAYER_TOXIC = r'^(.*) was badly poisoned!$'
OPPONENT_POISON = r'^The opposing (.*) was hurt by poison!$'
PLAYER_POISON = r'^(.*) was hurt by poison!$'
OPPONENT_POISON_HEAL = r'^The opposing (.*) was cured of its poisoning!$'
PLAYER_POISON_HEAL = r'^(.*) was cured of its poisoning!$'
OPPONENT_DROWSY = r'^The opposing (.*) grew drowsy!$'
PLAYER_DROWSY = r'^(.*) grew drowsy!$'
OPPONENT_SLEEP = r'^The opposing (.*) fell asleep!$'
PLAYER_SLEEP = r'^(.*) fell asleep!$'
OPPONENT_ASLEEP = r'^The opposing (.*) is fast asleep\.$'
PLAYER_ASLEEP = r'^(.*) is fast asleep\.$'
OPPONENT_ALREADY_ASLEEP = r'^The opposing (.*) is already asleep!$'
PLAYER_ALREADY_ASLEEP = r'^(.*) is already asleep!$'
OPPONENT_WAKE = r'^The opposing (.*) woke up!$'
PLAYER_WAKE = r'^(.*) woke up!$'
OPPONENT_FROZE = r'^The opposing (.*) was frozen solid!$'
PLAYER_FROZE = r'^(.*) was frozen solid!$'
OPPONENT_FROZEN = r'^The opposing (.*) is frozen solid!$'
PLAYER_FROZEN = r'^(.*) is frozen solid!$'
OPPONENT_THAW = r'^The opposing (.*) thawed out!$'
PLAYER_THAW = r'^(.*) thawed out!$'
OPPONENT_PARALYZE = r'^(?:\[.*\'s Static\])?The opposing (.*) is paralyzed! It may be unable to move!$'
PLAYER_PARALYZE = r'^(?:\[The opposing .*\'s Static\])?(.*) is paralyzed! It may be unable to move!$'
OPPONENT_PARALYZED = r'^The opposing (.*) is paralyzed! It can\'t move!$'
PLAYER_PARALYZED = r'^(.*) is paralyzed! It can\'t move!$'
OPPONENT_PARALYZE_HEAL = r'^The opposing (.*) was cured of paralysis!$'
PLAYER_PARALYZE_HEAL = r'^(.*) was cured of paralysis!$'
OPPONENT_ALREADY_PARALYZE = r'^The opposing (.*) is already paralyzed!$'
PLAYER_ALREADY_PARALYZE = r'^(.*) is already paralyzed!$'
OPPONENT_CONFUSE = r'^The opposing (.*) became confused!$'
PLAYER_CONFUSE = r'^(.*) became confused!$'
OPPONENT_KNOCKOFF = r'^The opposing (.*) knocked off (.*)\'s (.*)!$'
PLAYER_KNOCKOFF = r'^(.*) knocked off the opposing (.*)\'s (.*)!$'
OPPONENT_LIFEORB = r'^The opposing (.*) lost some of its HP!$'
PLAYER_LIFEORB = r'^(.*) lost some of its HP!$'
OPPONENT_IMMUNE = r'^It doesn\'t affect the opposing (.*)\.\.\.$'
PLAYER_IMMUNE = r'^It doesn\'t affect (.*)\.\.\.'
OPPONENT_PROTECT = r'^The opposing (.*) protected itself!$'
PLAYER_PROTECT = r'^(.*) protected itself!$'
OPPONENT_SEEDED = r'^The opposing (.*) was seeded!$'
PLAYER_SEEDED = r'^(.*) was seeded!$'
OPPONENT_SEEDED_DMG = r'^The opposing (.*)\'s health is sapped by Leech Seed!$'
PLAYER_SEEDED_DMG = r'^(.*)\'s health is sapped by Leech Seed!$'
OPPONENT_HEAL = r'^(?:\[The opposing .*\'s Cheek Pouch\])?The opposing (.*) had its HP restored\.$'
PLAYER_HEAL = r'^(?:\[.*\'s Cheek Pouch\])?(.*) had its HP restored\.$'
OPPONENT_FULL_HP = r'The opposing (.*)\'s HP is full!$'
PLAYER_FULL_HP = r'(.*)\'s HP is full!$'
OPPONENT_REST = r'^The opposing (.*) slept and became healthy!$'
PLAYER_REST = r'^(.*) slept and became healthy!$'
OPPONENT_BERRY = r'^The opposing (.*) restored HP using its .*!$'
PLAYER_BERRY = r'^(.*) restored HP using its .*!$'
OPPONENT_LOSE_TYPE = r'^\(The opposing (.*) loses (.*) type this turn\.\)$'
PLAYER_LOSE_TYPE = r'^\((.*) loses (.*) type this turn\.\)$'
OPPONENT_SET_WEB = r'^A sticky web has been laid out on the ground around your team!$'
PLAYER_SET_WEB = r'^A sticky web has been laid out on the ground around the opposing team!$'
OPPONENT_SET_STONE = r'^Pointed stones float in the air around your team!$'
PLAYER_SET_STONE = r'^Pointed stones float in the air around the opposing team!$'
OPPONENT_SET_SPIKE = r'^Spikes were scattered on the ground all around your team!$'
PLAYER_SET_SPIKE = r'^Spikes were scattered on the ground all around the opposing team!$'
OPPONENT_SET_POISON = r'^Poison spikes were scattered on the ground all around your team!$'
PLAYER_SET_POISON = r'^Poison spikes were scattered on the ground all around the opposing team!$'
OPPONENT_POISON_CLEAR = r'^The poison spikes disappeared from the ground around the opposing team!$'
OPPONENT_STONE_DMG = r'^Pointed stones dug into the opposing (.*)!$'
PLAYER_STONE_DMG = r'^Pointed stones dug into (.*)!$'
OPPONENT_SPIKE_DMG = r'^The opposing (.*) was hurt by the spikes!$'
PLAYER_SPIKE_DMG = r'^(.*) was hurt by the spikes!$'
OPPONENT_DRAGGED = r'^The opposing (.*) was dragged out!$'
PLAYER_DRAGGED = r'^(.*) was dragged out!$'
OPPONENT_NIMBLE = r'^The opposing (.*) became nimble!$'
PLAYER_NIMBLE = r'^(.*) became nimble!$'
OPPONENT_WEAKNESS_POLICY = r'^\(The opposing (.*) used its Weakness Policy!\)'
PLAYER_WEAKNESS_POLICY = r'^\((.*) used its Weakness Policy!\)'
OPPONENT_FOCUS_SASH = r'^The opposing (.*) hung on using its Focus Sash!$'
PLAYER_FOCUS_SASH = r'^(.*) hung on using its Focus Sash!$'
OPPONENT_TRACE = r'^\[The opposing .*\'s .*\]\[The opposing .*\'s .*\]The opposing (.*) traced (.*)\'s (.*)!$'
PLAYER_TRACE = r'^\[.*\'s .*\]\[.*\'s .*\](.*) traced the opposing (.*)\'s (.*)!$'
OPPONENT_LEVITATE = r'^\[The opposing .*\'s Levitate\]It doesn\'t affect the opposing (.*)\.\.\.$'
PLAYER_LEVITATE = r'^\[.*\'s Levitate\]It doesn\'t affect (.*)\.\.\.$'
OPPONENT_TAUNT = r'^The opposing (.*) fell for the taunt!$'
PLAYER_TAUNT = r'^(.*) fell for the taunt!$'
OPPONENT_TAUNT_END = r'^The opposing (.*) shook off the taunt!$'
PLAYER_TAUNT_END = r'^(.*) shook off the taunt!$'
OPPONENT_ENCORE = r'^The opposing (.*) must do an encore!$'
PLAYER_ENCORE = r'^(.*) must do an encore!$'
OPPONENT_ENCORE_END = r'^The opposing (.*)\'s encore ended!$'
PLAYER_ENCORE_END = r'^(.*)\'s encore ended!$'
OPPONENT_FORM = r'^\[(.*)\'s Stance Change\]Changed to (.*)!$'
PLAYER_FORM = r'^\[(.*)\'s Stance Change\]Changed to (.*)!$'
OPPONENT_WATER_ABSORB = r'^\[.*\'s Water Absorb\]The opposing (.*) had its HP restored\.$'
PLAYER_WATER_ABSORB = r'^\[.*\'s Water Absorb\](.*) had its HP restored\.$'
OPPONENT_MOLD = r'^\[The opposing .*\'s Mold Breaker\]The opposing (.*) breaks the mold!$'
PLAYER_MOLD = r'^\[.*\'s Mold Breaker\](.*) breaks the mold!$'
OPPONENT_STURDY = r'^\[The opposing.*\'s Sturdy\]The opposing (.*) endured the hit!$'
PLAYER_STURDY = r'^\[.*\'s Sturdy\](.*) endured the hit!$'
OPPONENT_WISH = r'^The opposing .*\'s wish came true!$'
PLAYER_WISH = r'^.*\'s wish came true!$'
OPPONENT_PROTEAN = r'^\[The opposing .*\'s Protean\]The opposing (.*)\'s type changed to (.*)!$'
PLAYER_PROTEAN = r'^\[.*\'s Protean\](.*)\'s type changed to (.*)!$'
OPPONENT_CURSE_BODY = r'\[The opposing .*\'s Cursed Body\](.*)\'s (.*) was disabled!$'
PLAYER_CURSE_BODY = r'\[.*\'s Cursed Body\]The opposing (.*)\'s (.*) was disabled!$'
OPPONENT_TAUNT_FAIL = r'^The opposing (.*) can\'t use .* after the taunt!$'
PLAYER_TAUNT_FAIL = r'^(.*) can\'t use .* after the taunt!$'
OPPONENT_HAIL_DMG = r'^The opposing (.*) is buffeted by the hail!$'
PLAYER_HAIL_DMG = r'^(.*) is buffeted by the hail!$'
OPPONENT_ABSORB_POWER = r'^The opposing (.*) is absorbing power!$'
PLAYER_ABSORB_POWER = r'^(.*) is absorbing power!$'
OPPONENT_POWER_HERB = r'^The opposing (.*) became fully charged due to its Power Herb!$'
PLAYER_POWER_HERB = r'^(.*) became fully charged due to its Power Herb!$'
OPPONENT_WHITE_HERB = r'^The opposing (.*) returned its stats to normal using its White Herb!$'
PLAYER_WHITE_HERB = r'^(.*) returned its stats to normal using its White Herb!$'
OPPONENT_FLINCH = r'^The opposing (.*) flinched and couldn\'t move!$'
PLAYER_FLINCH = r'^(.*) flinched and couldn\'t move!$'
OPPONENT_BELLY_DRUM = r'^The opposing (.*) cut its own HP and maximized its Attack!$'
PLAYER_BELLY_DRUM = r'^(.*) cut its own HP and maximized its Attack!$'
PLAYER_LIGHT_SCREEN = r'^Light Screen made your team stronger against special moves!$'
PLAYER_REFLECT = r'^Reflect made your team stronger against physical moves!$'
RAIN = r'^.*It started to rain!$'
HAIL = r'^.*It started to hail!$'
HAIL_STOP = r'^The hail stopped\.$'
PAIN_SPLIT = r'^The battlers shared their pain!$'
FAILED = r'^But it failed!$'
SUBSTITUTE_FAILED = r'^But it does not have enough HP left to make a substitute!$'
SUBSTITUTE_FAILED_2 = r'^.* already has a substitute!'
CONFUSE_HIT = r'^It hurt itself in its confusion!$'
ELECTRIC_TERRAIN = r'^An electric current ran across the battlefield!$'
ELECTRIC_TERRAIN_END = r'^The electricity disappeared from the battlefield.$'
TRICK_ROOM = r'^.*twisted the dimensions!$'
TRICK_ROOM_END = r'^The twisted dimensions returned to normal!$'
ITEM_SWITCH = r'^.* switched items with its target!$'

# Ignore messages
IGNORE_1 = r'^.*put in a substitute!$'
IGNORE_2 = r'^\(Since gen 7, Dark is immune to Prankster moves.\)$'
IGNORE_3 = r'^The Pokémon was hit.*times!$'
IGNORE_4 = r'\[.*\'s Beast Boost\]$'
IGNORE_5 = r'^It\'s not very effective\.\.\.$'
IGNORE_6 = r'^\[.*\'s Pressure\]$'
IGNORE_7 = r'^The opposing (.*) surrounded itself with its Z-Power!$'
IGNORE_8 = r'\[.*\'s Speed Boost\]$'
IGNORE_9 = r'^A critical hit!$'
IGNORE_10 = r'^It\'s super effective!$'
IGNORE_11 = r'^\[.*\'s Stamina\]$'
IGNORE_12 = r'^.* had its energy drained!$'
IGNORE_13 = r'^Battle started between .* and .*!$'
IGNORE_14 = r'^\[.*\'s Pressure\].* is exerting its pressure!$'
IGNORE_15 = r'^\[The opposing .*\'s Unnerve\]$'
IGNORE_16 = r'^\[.*\'s Download\]$'
IGNORE_17 = r'^\(.* ate its Sitrus Berry!\)$'
IGNORE_18 = r'^\[.*\'s Emergency Exit\]'
IGNORE_19 = r'^\[The opposing .*\'s Frisk\]The opposing .* frisked .* and found its .*!$'
IGNORE_20 = r'^\[.*\'s Intimidate\]$'
IGNORE_21 = r'^A bell chimed!$'
IGNORE_22 = r'^\[The opposing .*\'s Unnerve\]Your team is too nervous to eat Berries!$'
IGNORE_23 = r'^.* is confused!$'
IGNORE_24 = r'^.* won the battle!$'
IGNORE_25 = r'^\(The hail is crashing down\.\)$'
IGNORE_26 = r'^\(Rain continues to fall\.\)'
IGNORE_27 = r'^A soothing aroma wafted through the area!$'
IGNORE_28 = r'^\(Fake Out only works on your first turn out\.\)$'
IGNORE_29 = r'^.* surrounded itself with its Z-Power!$'
IGNORE_30 = r'^.*returned its decreased stats to normal using its Z-Power!$'
IGNORE_31 = r'^\[.*\'s Moxie\]$'
IGNORE_32 = r'^\[.*\'s Fairy Aura\].* is radiating a fairy aura!$'
IGNORE_33 = r'^.* floats in the air with its Air Balloon!$'
IGNORE_34 = r'.*\'s Air Balloon popped!$'
IGNORE_35 = r'^.* lost due to inactivity\.$'
IGNORE_36 = r'^.* obtained one .*\.$'
IGNORE_37 = r'^.* forfeited\.$'
IGNORE_38 = r'^\(.* ate its .*!\)$'
IGNORE_39 = r'^.* is hoping to take its attacker down with it!$'
IGNORE_40 = r'^.*\'s .* won\'t go any higher!$'

REGEX_LIST = [
    OPPONENT_Z_MOVE,
    PLAYER_Z_MOVE,
    OPPONENT_MOVE,
    PLAYER_MOVE,
    OPPONENT_DAMAGE,
    PLAYER_DAMAGE,
    OPPONENT_STAT_DROP,
    PLAYER_STAT_DROP,
    OPPONENT_STAT_DROP_HARSH,
    PLAYER_STAT_DROP_HARSH,
    OPPONENT_STAT_RAISE,
    PLAYER_STAT_RAISE,
    OPPONENT_STAT_RAISE_DRAST,
    PLAYER_STAT_RAISE_DRAST,
    OPPONENT_STAT_RAISE_SHARP,
    PLAYER_STAT_RAISE_SHARP,
    OPPONENT_STAT_RAISE_WEAKNESS,
    PLAYER_STAT_RAISE_WEAKNESS,
    OPPONENT_SWITCH_1,
    OPPONENT_SWITCH_2,
    PLAYER_SWITCH,
    OPPONENT_SELECT,
    PLAYER_SELECT,
    OPPONENT_MEGA,
    PLAYER_MEGA,
    OPPONENT_RECOIL,
    PLAYER_RECOIL,
    OPPONENT_FAINT,
    PLAYER_FAINT,
    OPPONENT_DODGE,
    PLAYER_DODGE,
    OPPONENT_LEFTOVERS,
    PLAYER_LEFTOVERS,
    OPPONENT_SUBSTITUTE,
    PLAYER_SUBSTITUTE,
    OPPOSING_SUBSTITUTE_FADED,
    PLAYER_SUBSTITUTE_FADED,
    PLAYER_FRISK,
    OPPONENT_BURNED,
    PLAYER_BURNED,
    OPPONENT_BURN,
    PLAYER_BURN,
    OPPONENT_BURN_HEAL,
    PLAYER_BURN_HEAL,
    OPPONENT_POISONED,
    PLAYER_POISONED,
    OPPONENT_TOXIC,
    PLAYER_TOXIC,
    OPPONENT_POISON,
    PLAYER_POISON,
    OPPONENT_POISON_HEAL,
    PLAYER_POISON_HEAL,
    OPPONENT_DROWSY,
    PLAYER_DROWSY,
    OPPONENT_SLEEP,
    PLAYER_SLEEP,
    OPPONENT_ASLEEP,
    PLAYER_ASLEEP,
    OPPONENT_ALREADY_ASLEEP,
    PLAYER_ALREADY_ASLEEP,
    OPPONENT_WAKE,
    PLAYER_WAKE,
    OPPONENT_FROZE,
    PLAYER_FROZE,
    OPPONENT_FROZEN,
    PLAYER_FROZEN,
    OPPONENT_THAW,
    PLAYER_THAW,
    OPPONENT_PARALYZE,
    PLAYER_PARALYZE,
    OPPONENT_PARALYZED,
    PLAYER_PARALYZED,
    OPPONENT_PARALYZE_HEAL,
    PLAYER_PARALYZE_HEAL,
    OPPONENT_ALREADY_PARALYZE,
    PLAYER_ALREADY_PARALYZE,
    OPPONENT_CONFUSE,
    PLAYER_CONFUSE,
    OPPONENT_KNOCKOFF,
    PLAYER_KNOCKOFF,
    OPPONENT_LIFEORB,
    PLAYER_LIFEORB,
    OPPONENT_IMMUNE,
    PLAYER_IMMUNE,
    OPPONENT_PROTECT,
    PLAYER_PROTECT,
    OPPONENT_SEEDED,
    PLAYER_SEEDED,
    OPPONENT_SEEDED_DMG,
    PLAYER_SEEDED_DMG,
    OPPONENT_HEAL,
    PLAYER_HEAL,
    OPPONENT_FULL_HP,
    PLAYER_FULL_HP,
    OPPONENT_BERRY,
    PLAYER_BERRY,
    OPPONENT_REST,
    PLAYER_REST,
    OPPONENT_LOSE_TYPE,
    PLAYER_LOSE_TYPE,
    OPPONENT_SET_WEB,
    PLAYER_SET_WEB,
    OPPONENT_SET_STONE,
    PLAYER_SET_STONE,
    OPPONENT_SET_SPIKE,
    PLAYER_SET_SPIKE,
    OPPONENT_SET_POISON,
    PLAYER_SET_POISON,
    OPPONENT_POISON_CLEAR,
    OPPONENT_STONE_DMG,
    PLAYER_STONE_DMG,
    OPPONENT_SPIKE_DMG,
    PLAYER_SPIKE_DMG,
    OPPONENT_DRAGGED,
    PLAYER_DRAGGED,
    OPPONENT_NIMBLE,
    PLAYER_NIMBLE,
    OPPONENT_WEAKNESS_POLICY,
    PLAYER_WEAKNESS_POLICY,
    OPPONENT_FOCUS_SASH,
    PLAYER_FOCUS_SASH,
    OPPONENT_TRACE,
    PLAYER_TRACE,
    OPPONENT_LEVITATE,
    PLAYER_LEVITATE,
    OPPONENT_TAUNT,
    PLAYER_TAUNT,
    OPPONENT_TAUNT_END,
    PLAYER_TAUNT_END,
    OPPONENT_ENCORE,
    PLAYER_ENCORE,
    OPPONENT_ENCORE_END,
    PLAYER_ENCORE_END,
    OPPONENT_WATER_ABSORB,
    PLAYER_WATER_ABSORB,
    OPPONENT_MOLD,
    PLAYER_MOLD,
    OPPONENT_STURDY,
    PLAYER_STURDY,
    OPPONENT_WISH,
    PLAYER_WISH,
    PAIN_SPLIT,
    OPPONENT_FORM,
    PLAYER_FORM,
    OPPONENT_PROTEAN,
    PLAYER_PROTEAN,
    OPPONENT_CURSE_BODY,
    PLAYER_CURSE_BODY,
    OPPONENT_TAUNT_FAIL,
    PLAYER_TAUNT_FAIL,
    OPPONENT_HAIL_DMG,
    PLAYER_HAIL_DMG,
    OPPONENT_ABSORB_POWER,
    PLAYER_ABSORB_POWER,
    OPPONENT_POWER_HERB,
    PLAYER_POWER_HERB,
    OPPONENT_FLINCH,
    PLAYER_FLINCH,
    OPPONENT_BELLY_DRUM,
    PLAYER_BELLY_DRUM,
    PLAYER_LIGHT_SCREEN,
    PLAYER_REFLECT,
    RAIN,
    HAIL,
    HAIL_STOP,
    FAILED,
    SUBSTITUTE_FAILED,
    SUBSTITUTE_FAILED_2,
    CONFUSE_HIT,
    ELECTRIC_TERRAIN,
    ELECTRIC_TERRAIN_END,
    TRICK_ROOM,
    TRICK_ROOM_END,
    ITEM_SWITCH
]

IGNORE_LIST = [
    IGNORE_1,
    IGNORE_2,
    IGNORE_3,
    IGNORE_4,
    IGNORE_5,
    IGNORE_6,
    IGNORE_7,
    IGNORE_8,
    IGNORE_9,
    IGNORE_10,
    IGNORE_11,
    IGNORE_12,
    IGNORE_13,
    IGNORE_14,
    IGNORE_15,
    IGNORE_16,
    IGNORE_17,
    IGNORE_18,
    IGNORE_19,
    IGNORE_20,
    IGNORE_21,
    IGNORE_22,
    IGNORE_23,
    IGNORE_24,
    IGNORE_25,
    IGNORE_26,
    IGNORE_27,
    IGNORE_28,
    IGNORE_29,
    IGNORE_30,
    IGNORE_31,
    IGNORE_32,
    IGNORE_33,
    IGNORE_34,
    IGNORE_35,
    IGNORE_36,
    IGNORE_37,
    IGNORE_38,
    IGNORE_39,
    IGNORE_40
]

MSG_DICT = {
    OPPONENT_MOVE: 'Opponent {} used {}',
    OPPONENT_Z_MOVE: 'Opponent {} used {} Z-move',
    PLAYER_Z_MOVE: 'Player {} used {} Z-move',
    PLAYER_MOVE: 'Player {} used {}',
    OPPONENT_DAMAGE: 'Opponent {} lost {} health',
    PLAYER_DAMAGE: 'Player {} lost {} health',
    OPPONENT_STAT_DROP: 'Opponent {} {} -1',
    PLAYER_STAT_DROP: 'Player {} {} -1',
    OPPONENT_STAT_DROP_HARSH: 'Opponent {} {} -2',
    PLAYER_STAT_DROP_HARSH: 'Player {} {} -2',
    OPPONENT_STAT_RAISE: 'Opponent {} {} +1',
    OPPONENT_STAT_RAISE_DRAST: 'Opponent {} {} +3',
    PLAYER_STAT_RAISE_DRAST: 'Player {} {} +3',
    PLAYER_STAT_RAISE: 'Player {} {} +1',
    OPPONENT_STAT_RAISE_SHARP: 'Opponent {} {} +2',
    PLAYER_STAT_RAISE_SHARP: 'Player {} {} +2',
    PLAYER_STAT_RAISE_WEAKNESS: 'Player {} {} +2',
    PLAYER_SWITCH: 'Player withdrew {}',
    OPPONENT_SWITCH_1: 'Opponent withdrew {}',
    OPPONENT_SWITCH_2: 'Opponent withdrew {}',
    OPPONENT_SELECT: 'Opponent chose {}',
    PLAYER_SELECT: 'Player chose {}',
    OPPONENT_MEGA: 'Opponent {} mega evolved to {}',
    PLAYER_MEGA: 'Player {} mega evolved to {}',
    OPPONENT_RECOIL: 'Opponent {} recoiled',
    PLAYER_RECOIL: 'Player {} recoiled',
    OPPONENT_FAINT: 'Opponent {} fainted',
    PLAYER_FAINT: 'Player {} fainted',
    OPPONENT_DODGE: 'Opponent {} lost 0% health',
    PLAYER_DODGE: 'Player {} lost 0% health',
    OPPONENT_LEFTOVERS: 'Opponent {} 6.25% health with {}',
    PLAYER_LEFTOVERS: 'Player {} restored 6.25% health with {}',
    OPPONENT_SUBSTITUTE: 'Substitute protected Opponent {}',
    PLAYER_SUBSTITUTE: 'Substitute protected Player {}',
    OPPOSING_SUBSTITUTE_FADED: 'Opponent {} substitute faded',
    PLAYER_SUBSTITUTE_FADED: 'Player {} substitute faded',
    PLAYER_FRISK: 'Player {} found {} {}',
    OPPONENT_BURNED: 'Opponent {} burned',
    PLAYER_BURNED: 'Player {} burned',
    OPPONENT_BURN: 'Opponent {} lost 6.25% health',
    PLAYER_BURN: 'Player {} lost 6.25% health',
    OPPONENT_BURN_HEAL: 'Opponent {} burn heal',
    PLAYER_BURN_HEAL: 'Player {} burn heal',
    OPPONENT_POISONED: 'Opponent {} poisoned',
    PLAYER_POISONED: 'Player {} poisoned',
    OPPONENT_TOXIC: 'Opponent {} badly poisoned',
    PLAYER_TOXIC: 'Player {} badly poisoned',
    OPPONENT_POISON: 'Opponent {} poison dmg',
    PLAYER_POISON: 'Player {} poison dmg',
    OPPONENT_POISON_HEAL: 'Opponent {} poison heal',
    PLAYER_POISON_HEAL: 'Player {} poison heal',
    OPPONENT_DROWSY: 'Opponent {} drowsy',
    PLAYER_DROWSY: 'Player {} drowsy',
    OPPONENT_SLEEP: 'Opponent {} sleep',
    OPPONENT_ASLEEP: 'Opponent {} sleeping',
    OPPONENT_ALREADY_ASLEEP: 'Opponent {} already asleep',
    PLAYER_ALREADY_ASLEEP: 'Player {} already alseep',
    OPPONENT_FOCUS_SASH: 'Opponent {} focus sash',
    PLAYER_FOCUS_SASH: 'Player {} focus sash',
    OPPONENT_WAKE: 'Opponent {} woke',
    PLAYER_WAKE: 'Player {} woke',
    PLAYER_SLEEP: 'Player {} sleep',
    PLAYER_ASLEEP: 'Player {} sleeping',
    OPPONENT_FROZE: 'Opponent {} froze',
    PLAYER_FROZE: 'Player {} froze',
    OPPONENT_FROZEN: 'Opponent {} frozen',
    PLAYER_FROZEN: 'Player {} frozen',
    OPPONENT_THAW: 'Opponent {} thawed',
    PLAYER_THAW: 'Player {} thawed',
    OPPONENT_PARALYZE: 'Opponent {} paralyze',
    PLAYER_PARALYZE: 'Player {} paralyze',
    OPPONENT_PARALYZED: 'Opponent {} paralyzed',
    PLAYER_PARALYZED: 'Player {} paralyzed',
    OPPONENT_PARALYZE_HEAL: 'Opponent {} paralyze heal',
    PLAYER_PARALYZE_HEAL: 'Player {} paralyze heal',
    OPPONENT_ALREADY_PARALYZE: 'Opponent {} already paralyzed',
    PLAYER_ALREADY_PARALYZE: 'Player {} already paralyzed',
    OPPONENT_CONFUSE: 'Opponent {} confused',
    PLAYER_CONFUSE: 'Player {} confused',
    OPPONENT_KNOCKOFF: 'Opponent {} knocked off Player {} {}',
    PLAYER_KNOCKOFF: 'Player {} knocked off Opponent {} {}',
    OPPONENT_LIFEORB: 'Opponent {} lost 10% health',
    PLAYER_LIFEORB: 'Player {} lost 10% health',
    OPPONENT_IMMUNE: 'Opponent {} lost 0% health',
    PLAYER_IMMUNE: 'Player {} lost 0% health',
    OPPONENT_PROTECT: 'Opponent {} lost 0% health',
    PLAYER_PROTECT: 'Player {} lost 0% health',
    OPPONENT_SEEDED: 'Opponent {} seeded',
    PLAYER_SEEDED: 'Player {} seeded',
    OPPONENT_SEEDED_DMG: 'Opponent {} lost 12.5% health',
    PLAYER_SEEDED_DMG: 'Player {} lost 12.5% health',
    OPPONENT_HEAL: 'Opponent {} healed',
    PLAYER_HEAL: 'Player {} healed',
    OPPONENT_FULL_HP: 'Opponent {} full HP',
    PLAYER_FULL_HP: 'Player {} full HP',
    OPPONENT_BERRY: 'Opponent {} 25% healed',
    PLAYER_BERRY: 'Player {} 25% healed',
    OPPONENT_REST: 'Opponent {} rested',
    PLAYER_REST: 'Player {} rested',
    OPPONENT_LOSE_TYPE: 'Opponent {} lost {}',
    PLAYER_LOSE_TYPE: 'Player {} lost {}',
    OPPONENT_SET_WEB: 'Opponent set web',
    PLAYER_SET_WEB: 'Player set web',
    OPPONENT_SET_STONE: 'Opponent set stone',
    PLAYER_SET_STONE: 'Player set stone',
    OPPONENT_SET_SPIKE: 'Opponent set spike',
    PLAYER_SET_SPIKE: 'Player set spike',
    OPPONENT_SET_POISON: 'Opponent set poison',
    PLAYER_SET_POISON: 'Player set poison',
    OPPONENT_POISON_CLEAR: 'Opponent cleared poison',
    OPPONENT_STONE_DMG: 'Opponent {} stone dmg',
    PLAYER_STONE_DMG: 'Player {} stone dmg',
    OPPONENT_SPIKE_DMG: 'Opponent {} spike dmg',
    PLAYER_SPIKE_DMG: 'Player {} spike dmg',
    OPPONENT_DRAGGED: 'Opponent {} dragged in',
    PLAYER_DRAGGED: 'Player {} dragged in',
    OPPONENT_NIMBLE: 'Opponent {} nimble',
    PLAYER_NIMBLE: 'Player {} nimble',
    OPPONENT_WEAKNESS_POLICY: 'Opponent {} Weakness Policy',
    PLAYER_WEAKNESS_POLICY: 'Player {} Weakness Policy',
    OPPONENT_TRACE: 'Opponent {} took Player {} {}',
    PLAYER_TRACE: 'Player {} took Opponent {} {}',
    OPPONENT_LEVITATE: 'Opponent {} lost 0% health',
    PLAYER_LEVITATE: 'Player {} lost 0% health',
    OPPONENT_TAUNT: 'Opponent {} taunted',
    PLAYER_TAUNT: 'Player {} taunted',
    OPPONENT_TAUNT_END: 'Opponent {} taunt end',
    PLAYER_TAUNT_END: 'Player {} taunt end',
    OPPONENT_ENCORE: 'Opponent {} encore',
    PLAYER_ENCORE: 'Player {} encore',
    OPPONENT_ENCORE_END: 'Opponent {} encore end',
    PLAYER_ENCORE_END: 'Player {} encore end',
    OPPONENT_FORM: 'Opponent {} changed to {}',
    PLAYER_FORM: 'Player {} changed to {}',
    OPPONENT_WATER_ABSORB: 'Opponent {} healed',
    PLAYER_WATER_ABSORB: 'Player {} healed',
    OPPONENT_MOLD: 'Opponent {} breaks mold',
    PLAYER_MOLD: 'Player {} breaks mold',
    OPPONENT_STURDY: 'Opponent {} sturdy',
    PLAYER_STURDY: 'Player {} sturdy',
    OPPONENT_WISH: 'Opponent active healed',  # TODO get percent
    PLAYER_WISH: 'Player active healed',
    OPPONENT_PROTEAN: 'Opponent {} changed to {}',
    PLAYER_PROTEAN: 'Player {} changed to {}',
    OPPONENT_CURSE_BODY: 'Player {} {} disabled',
    PLAYER_CURSE_BODY: 'Opponent {} {} disabled',
    OPPONENT_TAUNT_FAIL: 'Opponent {} move failed to taunt',
    PLAYER_TAUNT_FAIL: 'Player {} move failed to taunt',
    OPPONENT_HAIL_DMG: 'Opponent {} lost % health',  # TODO get percent
    PLAYER_HAIL_DMG: 'PLAYER {} lost % health',
    OPPONENT_ABSORB_POWER: 'Opponent {} absorb power',
    PLAYER_ABSORB_POWER: 'Player {} absorb power',
    OPPONENT_POWER_HERB: 'Opponent {} Power Herb',
    PLAYER_POWER_HERB: 'Player {} Power Herb',
    OPPONENT_FLINCH: 'Opponent {} flinch',
    PLAYER_FLINCH: 'Player {} flinch',
    OPPONENT_BELLY_DRUM: 'Opponent {} lost 50% health, attack +6',
    PLAYER_BELLY_DRUM: 'Player {} lost 50% health, attack +6',
    PLAYER_LIGHT_SCREEN: 'Player Light Screen',
    PLAYER_REFLECT: 'Player Reflect',
    PAIN_SPLIT: 'Pain split',
    RAIN: 'Rain',
    HAIL: 'Hail',
    HAIL_STOP: 'Hail stop',
    FAILED: 'Move failed',
    SUBSTITUTE_FAILED: 'Unable to substitute',
    SUBSTITUTE_FAILED_2: 'Unable to substitute',
    CONFUSE_HIT: 'Confuse hit',
    ELECTRIC_TERRAIN: 'Electric terrain',
    ELECTRIC_TERRAIN_END: 'Electric terrain end',
    TRICK_ROOM: 'Trick room',
    TRICK_ROOM_END: 'Trick room end',
    ITEM_SWITCH: 'Item swap'
}
# TODO NOTES
'''
Bright light is about to burst out of the opposing Necrozma!
The opposing Necrozma regained its true power through Ultra Burst!
All stat changes were eliminated!
Your team's Light Screen wore off!
[Tapu Lele's Psychic Surge]The battlefield got weird!
Your team's Reflect wore off!
[The opposing Kyurem's Turboblaze]The opposing Kyurem is radiating a blazing aura!
[Registeel's Clear Body]Registeel's stats were not lowered!
[The opposing Ninetales's Drought]The sunlight turned harsh!
[Hippowdon's Sand Stream]A sandstorm kicked up!
(The sandstorm is raging.)
The opposing Ninetales is buffeted by the sandstorm!
The sandstorm subsided.
(The sunlight is strong.)
The harsh sunlight faded.
'''
