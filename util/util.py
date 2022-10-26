KNOWN_MOVES_FILE, KNOWN_ABILITIES_FILE = './data/known_moves.data', './data/known_abilities.data'
MOVES_FILE, ABILITIES_FILE, ITEMS_FILE = './data/moves.data', './data/abilities.data', './data/items.data'
LOG_ROOT = './logs'
STATS_FILE, BASE_LOG_FILE = './data/stats.data', './logs/battle_{}.log'

# Types
NORMAL = 'Normal'
FIGHT = 'Fighting'
FLYING = 'Flying'
POISON = 'Poison'
GROUND = 'Ground'
ROCK = 'Rock'
BUG = 'Bug'
GHOST = 'Ghost'
STEEL = 'Steel'
FIRE = 'Fire'
WATER = 'Water'
GRASS = 'Grass'
ELECTR = 'Electric'
PSYCHIC = 'Psychic'
ICE = 'Ice'
DRAGON = 'Dragon'
DARK = 'Dark'
FAIRY = 'Fairy'
UNKNOWN = '???'

# Move Type
STATUS = 'Status'
PHYSICAL = 'Physical'
SPECIAL = 'Special'

# Statuses
BRN = 'BRN'
PSN = 'PSN'
TOX = 'TOX'
SLP = 'SLP'
PAR = 'PAR'
FRZ = 'FRZ'
CONFUSED = 'Confused'
SLOW_START = 'Slow Start'

STATUS_LIST = [BRN, PSN, TOX, SLP, PAR, FRZ]

# Immune abilities
# TODO Soundproof
IMMUNE_ABILITIES = {
    'Dry Skin': WATER,
    'Flash Fire': FIRE,
    'Levitate': GROUND,
    'Lightning Rod': ELECTR,
    'Motor Drive': ELECTR,
    'Sap Sipper': GRASS,
    'Storm Drain': WATER,
    'Volt Absorb': ELECTR,
    'Water Absorb': WATER
}

# Stats
HP = 'HP'
ATK = 'Atk'
DEF = 'Def'
SPA = 'SpA'
SPD = 'SpD'
SPE = 'Spe'

STATS_LIST = [HP, ATK, DEF, SPA, SPD, SPE]

# Weather
W_RAIN = 'raindance'
W_HEAVY_RAIN = 'primordialsea'
W_SUN = 'sunnyday'
W_HARSH_SUN = 'desolateland'
W_HAIL = 'hail'
W_SANDSTORM = 'sandstorm'
W_PSYCHIC_TERRAIN = 'psychicterrain'
W_MISTY_TERRAIN = 'mistyterrain'
W_ELECTRIC_TERRAIN = 'electricterrain'
W_GRASSY_TERRRAIN = 'grassyterrain'
W_TRICK_ROOM = 'trickroom'
W_FOE_TAILWIND = 'foe_tailwind'
W_TAILWIND = 'tailwind'

WEATHER_LIST = [
    W_RAIN,
    W_HEAVY_RAIN,
    W_SUN,
    W_HARSH_SUN,
    W_HAIL,
    W_SANDSTORM
]

TERRAIN_LIST = [
    W_PSYCHIC_TERRAIN,
    W_MISTY_TERRAIN,
    W_ELECTRIC_TERRAIN,
    W_GRASSY_TERRRAIN
]

# Field Settings
FIELD_SPIKES = 'field_spikes'
FIELD_STONES = 'field_stones'
FIELD_POISON = 'field_poison'
FIELD_WEB = 'field_web'
FIELD_SCREEN = 'field_screen'
FIELD_REFLECT = 'field_reflect'
FIELD_SUBSTITUTE = 'field_substitute'
FIELD_AURORA_VEIL = 'field_auroraveil'

FIELD_LIST = [
    FIELD_SPIKES,
    FIELD_STONES,
    FIELD_POISON,
    FIELD_WEB,
    FIELD_SCREEN,
    FIELD_REFLECT,
    FIELD_AURORA_VEIL,
    FIELD_SUBSTITUTE
]

# Move Effects
PRIORITY = 'Priority'
CHANCE = 'Chance'
STAT_STEAL = 'StatSteal'
DISABLE = 'Disable'
ENCORE = 'Encore'
INFESTATION = 'Infestation'
FLINCH = 'Flinch'
CRIT = 'Crit'
SWITCH = 'Switch'
COUNTER = 'Counter'
DMG_HEAL = 'DmgHeal'
HEAL = 'Heal'
RECOIL = 'Recoil'
CURE = 'Cure'
PROTECT = 'Protect'
CHARGE = 'Charge'
RECHARGE = 'Recharge'
LEECH_SEED = 'LeechSeed'
TERRAIN_CLEAR = 'TerrainClear'
STATS_CLEAR = 'StatsClr'
FIELD_CLEAR = 'FieldClr'
SCREEN_CLEAR = 'ScreenClr'
ITEM_REMOVE = 'ItemRemove'
RDM_MOVE = 'RdmMove'
PAINSPLIT = 'PainSplit'
CONTACT_DMG = 'ContactDmg'
TRICK = 'Trick'
MOVE_LOCK = 'MoveLck'
LEVITATE = 'Levitate'
LVL_DMG = 'LvlDmg'
ENDEAVOR = 'Endeavor'
COPYCAT = 'Copycat'
TYPE_CHANGE = 'TypeChange'
PERISHSONG = 'PerishSong'
TRANSFORM = 'Transform'


def type_effectiveness(move_type, opponent_type):
    return {
        (NORMAL, ROCK): 0.5,
        (NORMAL, GHOST): 0.0,
        (NORMAL, STEEL): 0.5,
        (FIGHT, NORMAL): 2.0,
        (FIGHT, FLYING): 0.5,
        (FIGHT, POISON): 0.5,
        (FIGHT, ROCK): 2.0,
        (FIGHT, BUG): 0.5,
        (FIGHT, GHOST): 0.0,
        (FIGHT, STEEL): 2.0,
        (FIGHT, PSYCHIC): 0.5,
        (FIGHT, ICE): 2.0,
        (FIGHT, DARK): 2.0,
        (FIGHT, FAIRY): 0.5,
        (FLYING, FIGHT): 2.0,
        (FLYING, ROCK): 0.5,
        (FLYING, BUG): 2.0,
        (FLYING, STEEL): 0.5,
        (FLYING, GRASS): 2.0,
        (FLYING, ELECTR): 0.5,
        (POISON, POISON): 0.5,
        (POISON, GROUND): 0.5,
        (POISON, ROCK): 0.5,
        (POISON, GHOST): 0.5,
        (POISON, STEEL): 0.0,
        (POISON, GRASS): 2.0,
        (POISON, FAIRY): 2.0,
        (GROUND, FLYING): 0.0,
        (GROUND, POISON): 2.0,
        (GROUND, ROCK): 2.0,
        (GROUND, BUG): 0.5,
        (GROUND, STEEL): 2.0,
        (GROUND, FIRE): 2.0,
        (GROUND, GRASS): 0.5,
        (GROUND, ELECTR): 2.0,
        (ROCK, FIGHT): 0.5,
        (ROCK, FLYING): 2.0,
        (ROCK, GROUND): 0.5,
        (ROCK, BUG): 2.0,
        (ROCK, STEEL): 0.5,
        (ROCK, FIRE): 2.0,
        (ROCK, ICE): 2.0,
        (BUG, FIGHT): 0.5,
        (BUG, FLYING): 0.5,
        (BUG, POISON): 0.5,
        (BUG, FLYING): 0.5,
        (BUG, STEEL): 0.5,
        (BUG, FIRE): 0.5,
        (BUG, GRASS): 2.0,
        (BUG, PSYCHIC): 2.0,
        (BUG, DARK): 2.0,
        (BUG, FAIRY): 0.5,
        (GHOST, NORMAL): 0.0,
        (GHOST, GHOST): 2.0,
        (GHOST, PSYCHIC): 2.0,
        (GHOST, DARK): 0.5,
        (STEEL, ROCK): 2.0,
        (STEEL, STEEL): 0.5,
        (STEEL, FIRE): 0.5,
        (STEEL, WATER): 0.5,
        (STEEL, ELECTR): 0.5,
        (STEEL, ICE): 2.0,
        (STEEL, FAIRY): 2.0,
        (FIRE, ROCK): 0.5,
        (FIRE, BUG): 2.0,
        (FIRE, STEEL): 2.0,
        (FIRE, FIRE): 0.5,
        (FIRE, WATER): 0.5,
        (FIRE, GRASS): 2.0,
        (FIRE, ICE): 2.0,
        (FIRE, DRAGON): 0.5,
        (WATER, GROUND): 2.0,
        (WATER, ROCK): 2.0,
        (WATER, FIRE): 2.0,
        (WATER, WATER): 0.5,
        (WATER, GRASS): 0.5,
        (WATER, DRAGON): 0.5,
        (GRASS, FLYING): 0.5,
        (GRASS, POISON): 0.5,
        (GRASS, GROUND): 2.0,
        (GRASS, ROCK): 2.0,
        (GRASS, BUG): 0.5,
        (GRASS, STEEL): 0.5,
        (GRASS, FIRE): 0.5,
        (GRASS, WATER): 2.0,
        (GRASS, GRASS): 0.5,
        (GRASS, DRAGON): 0.5,
        (ELECTR, FLYING): 2.0,
        (ELECTR, GROUND): 0.0,
        (ELECTR, WATER): 2.0,
        (ELECTR, GRASS): 0.5,
        (ELECTR, ELECTR): 0.5,
        (ELECTR, DRAGON): 0.5,
        (PSYCHIC, FIGHT): 2.0,
        (PSYCHIC, POISON): 2.0,
        (PSYCHIC, STEEL): 0.5,
        (PSYCHIC, PSYCHIC): 0.5,
        (PSYCHIC, DARK): 0.0,
        (ICE, FLYING): 2.0,
        (ICE, GROUND): 2.0,
        (ICE, STEEL): 0.5,
        (ICE, FIRE): 0.5,
        (ICE, WATER): 0.5,
        (ICE, GRASS): 2.0,
        (ICE, ICE): 0.5,
        (ICE, DRAGON): 2.0,
        (DRAGON, STEEL): 0.5,
        (DRAGON, DRAGON): 2.0,
        (DRAGON, FAIRY): 0.0,
        (DARK, FIGHT): 0.5,
        (DARK, GHOST): 2.0,
        (DARK, PSYCHIC): 2.0,
        (DARK, DARK): 0.5,
        (DARK, FAIRY): 0.5,
        (FAIRY, FIGHT): 2.0,
        (FAIRY, POISON): 0.5,
        (FAIRY, STEEL): 0.5,
        (FAIRY, FIRE): 0.5,
        (FAIRY, DRAGON): 2.0,
        (FAIRY, DARK): 2.0
    }.get((move_type, opponent_type), 1.0)


# Item messages
ITEM_KNOCKED_OFF = r'^None \((.*) was knocked off\)$'
ITEM_EATEN = r'^None \((.*) was eaten\)$'
ITEM_HARVESTED = r'^(.*) \(harvested; .* was eaten\)$'
ITEM_CONSUMED = r'^None \((.*) was consumed\)$'
ITEM_FRISKED = r'^(.*) \(frisked\)$'
ITEM_TRICKED = r'^(.*) \(tricked\)$'
ITEM_POPPED = r'^None \((.*) was popped\)$'

ITEM_GENERAL = r'^(?:None)?(.*) \(.*\)$'

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
OPPONENT_Z_BOOST = r'^The opposing (.*) boosted its (.*) using its Z-Power!$'
PLAYER_Z_BOOST = r'^(.*) boosted its (.*) using its Z-Power!$'
STATS_RESET = r'^All stat changes were eliminated!$'
OPPONENT_STAT_RESET = r'^The opposing (.*)\'s stat changes were removed!$'
PLAYER_STAT_RESET = r'^(.*)\'s stat changes were removed!$'
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
OPPONENT_LEFTOVERS = r'^The opposing (.*) restored a little HP using its .*!$'
PLAYER_LEFTOVERS = r'^(.*) restored a little HP using its (.*)!$'
OPPONENT_SET_SUB = r'^The opposing (.*) put in a substitute!$'
PLAYER_SET_SUB = r'^(.*) put in a substitute!$'
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
OPPONENT_WAKE = r'^The opposing (.*) woke up!$'
PLAYER_WAKE = r'^(.*) woke up!$'
OPPONENT_FROZE = r'^The opposing (.*) was frozen solid!$'
PLAYER_FROZE = r'^(.*) was frozen solid!$'
OPPONENT_FROZEN = r'^The opposing (.*) is frozen solid!$'
PLAYER_FROZEN = r'^(.*) is frozen solid!$'
OPPONENT_THAW = r'^The opposing (.*) thawed out!$'
PLAYER_THAW = r'^(.*) thawed out!$'
OPPONENT_MOVE_THAW = r'^The opposing (.*)\'s .* melted the ice!$'
PLAYER_MOVE_THAW = r'^(.*)\'s .* melted the ice!$'
OPPONENT_PARALYZE = r'^(?:\[.*\])?The opposing (.*) is paralyzed! It may be unable to move!$'
PLAYER_PARALYZE = r'^(?:\[The opposing .*\])?(.*) is paralyzed! It may be unable to move!$'
OPPONENT_PARALYZED = r'^The opposing (.*) is paralyzed! It can\'t move!$'
PLAYER_PARALYZED = r'^(.*) is paralyzed! It can\'t move!$'
OPPONENT_PARALYZE_HEAL = r'^The opposing (.*) was cured of paralysis!$'
PLAYER_PARALYZE_HEAL = r'^(.*) was cured of paralysis!$'
OPPONENT_CONFUSE = r'^The opposing (.*) became confused!$'
PLAYER_CONFUSE = r'^(.*) became confused!$'
OPPONENT_CONFUSE_2 = r'^The opposing (.*) became confused due to fatigue!$'
PLAYER_CONFUSE_2 = r'^(.*) became confused due to fatigue!$'
OPPONENT_CONFUSE_END = r'^The opposing (.*) snapped out of its confusion!$'
PLAYER_CONFUSE_END = r'^(.*) snapped out of its confusion!$'
OPPONENT_INFESTATION = r'^The opposing (.*) has been afflicted with an infestation by .*!$'
PLAYER_INFESTATION = r'^(.*) has been afflicted with an infestation by .*!$'
OPPONENT_INFESTATION_DMG = r'^The opposing (.*) is hurt by Infestation!$'
PLAYER_INFESTATION_DMG = r'^(.*) is hurt by Infestation!$'
OPPONENT_INFESTATION_END = r'^The opposing (.*) was freed from Infestation!$'
PLAYER_INFESTATION_END = r'^(.*) was freed from Infestation!$'
OPPONENT_STATUS_CURE = r'^\(The opposing (.*) is cured by its Natural Cure!\)'
PLAYER_STATUS_CURE = r'^\((.*) is cured by its Natural Cure!\)'
OPPONENT_KNOCKOFF = r'^The opposing (.*) knocked off (.*)\'s (.*)!$'
PLAYER_KNOCKOFF = r'^(.*) knocked off the opposing (.*)\'s (.*)!$'
OPPONENT_LIFEORB = r'^The opposing (.*) lost some of its HP!$'
PLAYER_LIFEORB = r'^(.*) lost some of its HP!$'
OPPONENT_IMMUNE = r'^(?:\[The opposing .*\])?It doesn\'t affect the opposing (.*)\.\.\.$'
PLAYER_IMMUNE = r'^(?:\[.*\])?It doesn\'t affect (.*)\.\.\.'
OPPONENT_PROTECT = r'^The opposing (.*) protected itself!$'
PLAYER_PROTECT = r'^(.*) protected itself!$'
OPPONENT_PROTECT_DMG = r'^The opposing (.*) couldn\'t fully protect itself and got hurt!$'
PLAYER_PROTECT_DMG = r'^(.*) couldn\'t fully protect itself and got hurt!$'
OPPONENT_SEEDED = r'^The opposing (.*) was seeded!$'
PLAYER_SEEDED = r'^(.*) was seeded!$'
OPPONENT_SEEDED_DMG = r'^The opposing (.*)\'s health is sapped by Leech Seed!$'
PLAYER_SEEDED_DMG = r'^(.*)\'s health is sapped by Leech Seed!$'
OPPONENT_HEAL = r'^(?:\[The opposing .*)?The opposing (.*) had its HP restored\.$'
PLAYER_HEAL = r'^(?:\[.*\])?(.*) had its HP restored\.$'
OPPONENT_FULL_HP = r'^The opposing (.*)\'s HP is full!$'
PLAYER_FULL_HP = r'^(.*)\'s HP is full!$'
OPPONENT_REST = r'^The opposing (.*) slept and became healthy!$'
PLAYER_REST = r'^(.*) slept and became healthy!$'
OPPONENT_BERRY = r'^The opposing (.*) restored HP using its .*!$'
PLAYER_BERRY = r'^(.*) restored HP using its .*!$'
OPPONENT_FASTER = r'^The opposing (.*) can act faster than normal, thanks to its (.*)!$'
PLAYER_FASTER = r'^(.*) can act faster than normal, thanks to its (.*)!$'
OPPONENT_LOSE_TYPE = r'^\(The opposing (.*) loses (.*) type this turn\.\)$'
PLAYER_LOSE_TYPE = r'^\((.*) loses (.*) type this turn\.\)$'
OPPONENT_CHANGE_TYPE = r'^The opposing (.*)\'s type changed to (.*)!$'
PLAYER_CHANGE_TYPE = r'^(.*)\'s type changed to (.*)!$'
OPPONENT_SET_WEB = r'^A sticky web has been laid out on the ground around your team!$'
PLAYER_SET_WEB = r'^A sticky web has been laid out on the ground around the opposing team!$'
OPPONENT_WEB_CLEAR = r'^The sticky web has disappeared from the ground around the opposing team!$'
PLAYER_WEB_CLEAR = r'^The sticky web has disappeared from the ground around your team!$'
OPPONENT_SET_STONE = r'^Pointed stones float in the air around your team!$'
PLAYER_SET_STONE = r'^Pointed stones float in the air around the opposing team!$'
OPPONENT_SET_SPIKE = r'^Spikes were scattered on the ground all around your team!$'
PLAYER_SET_SPIKE = r'^Spikes were scattered on the ground all around the opposing team!$'
OPPONENT_SET_POISON = r'^Poison spikes were scattered on the ground all around your team!$'
PLAYER_SET_POISON = r'^Poison spikes were scattered on the ground all around the opposing team!$'
OPPONENT_POISON_CLEAR = r'^The poison spikes disappeared from the ground around the opposing team!$'
PLAYER_POISON_CLEAR = r'^The poison spikes disappeared from the ground around your team!$'
OPPONENT_STONE_DMG = r'^Pointed stones dug into the opposing (.*)!$'
PLAYER_STONE_DMG = r'^Pointed stones dug into (.*)!$'
OPPONENT_STONE_CLEAR = r'^The pointed stones disappeared from around the opposing team!$'
PLAYER_STONE_CLEAR = r'^The pointed stones disappeared from around your team!$'
OPPONENT_SPIKE_DMG = r'^The opposing (.*) was hurt by the spikes!$'
PLAYER_SPIKE_DMG = r'^(.*) was hurt by the spikes!$'
OPPONENT_SPIKE_CLEAR = r'^The spikes disappeared from the ground around the opposing team!$'
PLAYER_SPIKE_CLEAR = r'^The spikes disappeared from the ground around your team!$'
OPPONENT_DRAGGED = r'^The opposing (.*) was dragged out!$'
PLAYER_DRAGGED = r'^(.*) was dragged out!$'
OPPONENT_NIMBLE = r'^The opposing (.*) became nimble!$'
PLAYER_NIMBLE = r'^(.*) became nimble!$'
OPPONENT_WEAKNESS_POLICY = r'^\(The opposing (.*) used its Weakness Policy!\)'
PLAYER_WEAKNESS_POLICY = r'^\((.*) used its Weakness Policy!\)'
OPPONENT_FOCUS_SASH = r'^The opposing (.*) hung on using its Focus Sash!$'
PLAYER_FOCUS_SASH = r'^(.*) hung on using its Focus Sash!$'
OPPONENT_TRACE = r'^.*The opposing (.*) traced (.*)\'s (.*)!$'
PLAYER_TRACE = r'^\[.*\](.*) traced the opposing (.*)\'s (.*)!$'
OPPONENT_TAUNT = r'^The opposing (.*) fell for the taunt!$'
PLAYER_TAUNT = r'^(.*) fell for the taunt!$'
OPPONENT_TAUNT_END = r'^The opposing (.*) shook off the taunt!$'
PLAYER_TAUNT_END = r'^(.*) shook off the taunt!$'
OPPONENT_ENCORE = r'^The opposing (.*) must do an encore!$'
PLAYER_ENCORE = r'^(.*) must do an encore!$'
OPPONENT_ENCORE_END = r'^The opposing (.*)\'s encore ended!$'
PLAYER_ENCORE_END = r'^(.*)\'s encore ended!$'
OPPONENT_FORM = r'^\[The opposing (.*)\'s Stance Change\]Changed to (.*)!$'
PLAYER_FORM = r'^\[(.*)\'s Stance Change\]Changed to (.*)!$'
OPPONENT_TRANSFORM = r'^The opposing (.*) transformed into its Complete Forme!$'
PLAYER_TRANSFORM = r'^(.*) transformed into its Complete Forme!$'
OPPONENT_TRANSFORM_2 = r'^The opposing (.*) transformed!$'
PLAYER_TRANSFORM_2 = r'^(.*) transformed!$'
OPPONENT_MAGIC_BOUNCE = r'^\[The opposing .*\'s Magic Bounce\]The opposing (.*) bounced the (.*) back!$'
PLAYER_MAGIC_BOUNCE = r'^\[.*\'s Magic Bounce\](.*) bounced the (.*) back!$'
OPPONENT_DITTO = r'^.*\]The opposing (.*) transformed into (.*)!$'
PLAYER_DITTO = r'^.*\](.*) transformed into (.*)!$'
OPPONENT_STURDY = r'^(?:\[The opposing.*\])?The opposing (.*) endured the hit!$'
PLAYER_STURDY = r'^(?:\[.*\])?(.*) endured the hit!$'
OPPONENT_WISH = r'^The opposing .*\'s wish came true!$'
PLAYER_WISH = r'^.*\'s wish came true!$'
OPPONENT_PROTEAN = r'^\[The opposing .*\]The opposing (.*)\'s type changed to (.*)!$'
PLAYER_PROTEAN = r'^\[.*\](.*)\'s type changed to (.*)!$'
OPPONENT_DISABLE = r'^(?:\[The opposing .*\])?(.*)\'s (.*) was disabled!$'
PLAYER_DISABLE = r'^(?:\[.*\])?The opposing (.*)\'s (.*) was disabled!$'
OPPONENT_DISABLE_END = r'^The opposing (.*)\'s move is no longer disabled!$'
PLAYER_DISABLE_END = r'^(.*)\'s move is no longer disabled!$'
OPPONENT_ULTRA_BURST = r'^The opposing (.*) regained its true power through Ultra Burst!$'
PLAYER_ULTRA_BURST = r'^(.*) regained its true power through Ultra Burst!$'
OPPONENT_PRIMAL = r'^The opposing (.*)\'s Primal Reversion! It reverted to its primal state!$'
PLAYER_PRIMAL = r'^(.*)\'s Primal Reversion! It reverted to its primal state!$'
OPPONENT_DISGUISE = r'^The opponent (.*)\'s disguise was busted!$'
PLAYER_DISGUISE = r'^(.*)\'s disguise was busted!$'
OPPONENT_BAD_DREAMS = r'^\[The opposing .*\'s Bad Dreams\](.*) is tormented!$'
PLAYER_BAD_DREAMS = r'^\[.*\'s Bad Dreams\]The opposing (.*) is tormented!$'
OPPONENT_FLASH_FIRE = r'^\[The opposing .*\'s Flash Fire\]The power of the opposing (.*)\'s Fire-type moves rose!$'
PLAYER_FLASH_FIRE = r'^\[.*\'s Flash Fire\]The power of (.*)\'s Fire-type moves rose!$'
OPPONENT_SCHOOL_END = r'^.*The opposing (.*) stopped schooling!$'
PLAYER_SCHOOL_END = r'^.*(.*) stopped schooling!$'
OPPONENT_AFTERMATH = r'^\[The opposing .*\'s Aftermath\](.*) was hurt!$'
PLAYER_AFTERMATH = r'^\[.*\'s Aftermath\]The opposing (.*) was hurt!$'
OPPONENT_CANNOT_USE = r'^.*The opposing (.*) cannot use (.*)!$'
PLAYER_CANNOT_USE = r'^.*(.*) cannot use (.*)!$'
OPPONENT_CONTACT = r'^\[The opposing .*\'s .*\](.*) was hurt!$'
PLAYER_CONTACT = r'^\[.*\'s .*\]The opposing (.*) was hurt!$'
OPPONENT_OOZE_DMG = r'\[.*\'s Liquid Ooze\]The opposing (.*) sucked up the liquid ooze!$'
PLAYER_OOZE_DMG = r'\[.*\'s Liquid Ooze\](.*) sucked up the liquid ooze!$'
OPPONENT_TAUNT_FAIL = r'^The opposing (.*) can\'t use .* after the taunt!$'
PLAYER_TAUNT_FAIL = r'^(.*) can\'t use .* after the taunt!$'
OPPONENT_HAIL_DMG = r'^The opposing (.*) is buffeted by the hail!$'
PLAYER_HAIL_DMG = r'^(.*) is buffeted by the hail!$'
OPPONENT_ABSORB = r'^The opposing (.*)(?: is)? absorb(?:ing|ed) (.*)!$'
PLAYER_ABSORB = r'^(.*)(?: is)? absorb(?:ing|ed) (.*)!$'
OPPONENT_HEAT_BEAK = r'^The opposing (.*) started heating up its beak!$'
PLAYER_HEAT_BEAK = r'^(.*) started heating up its beak!$'
OPPONENT_POWER_HERB = r'^The opposing (.*) became fully charged due to its Power Herb!$'
PLAYER_POWER_HERB = r'^(.*) became fully charged due to its Power Herb!$'
OPPONENT_WHITE_HERB = r'^The opposing (.*) returned its stats to normal using its White Herb!$'
PLAYER_WHITE_HERB = r'^(.*) returned its stats to normal using its White Herb!$'
OPPONENT_FLINCH = r'^The opposing (.*) flinched and couldn\'t move!$'
PLAYER_FLINCH = r'^(.*) flinched and couldn\'t move!$'
OPPONENT_BELLY_DRUM = r'^The opposing (.*) cut its own HP and maximized its Attack!$'
PLAYER_BELLY_DRUM = r'^(.*) cut its own HP and maximized its Attack!$'
OPPONENT_LIGHT_SCREEN = r'^Light Screen made the opposing team stronger against special moves!$'
PLAYER_LIGHT_SCREEN = r'^Light Screen made your team stronger against special moves!$'
OPPONENT_WORE_OFF = r'^The opposing team\'s (.*) wore off!$'
PLAYER_WORE_OFF = r'^Your team\'s (.*) wore off!$'
OPPONENT_REFLECT = r'^Reflect made the opposing team stronger against physical moves!$'
PLAYER_REFLECT = r'^Reflect made your team stronger against physical moves!$'
OPPONENT_VEIL = r'^Aurora Veil made the opposing team stronger against physical and special moves!$'
PLAYER_VEIL = r'^Aurora Veil made your team stronger against physical and special moves!$'
OPPONENT_TAILWIND = r'^The Tailwind blew from behind the opposing team!$'
PLAYER_TAILWIND = r'^The Tailwind blew from behind your team!$'
OPPONENT_TAILWIND_END = r'^The opposing team\'s Tailwind petered out!$'
PLAYER_TAILWIND_END = r'^Your team\'s Tailwind petered out!$'
OPPONENT_SLOW_END = r'^The opposing (.*) finally got its act together!$'
PLAYER_SLOW_END = r'^(.*) finally got its act together!$'
OPPONENT_GROUNDED = r'^The opposing (.*) fell straight down!$'
PLAYER_GROUNDED = r'^(.*) fell straight down!$'
OPPONENT_FLY = r'^The opposing (.*) flew up high!$'
PLAYER_FLY = r'^(.*) flew up high!$'
RAIN = r'^.*It started to rain!$'
RAIN_END = r'^The rain stopped\.$'
RAIN_HEAVY = r'^(?:.*)?A heavy rain began to fall!$'
RAIN_HEAVY_END = r'^The heavy rain has lifted!$'
HAIL = r'^.*It started to hail!$'
HAIL_STOP = r'^The hail stopped\.$'
SUN = r'^.*The sunlight turned harsh!$'
SUN_END = r'^The harsh sunlight faded\.'
SUN_EXTREME = r'^.*The sunlight turned extremely harsh!$'
SUN_EXTREME_END = r'^The extremely harsh sunlight faded\.$'
SANDSTORM = r'^.*A sandstorm kicked up!$'
SANDSTORM_END = r'^The sandstorm subsided\.$'
OPPONENT_WEATHER_DMG = r'^The opposing (.*) is buffeted by the (?:sandstorm)|(?:hail)!$'
PLAYER_WEATHER_DMG = r'^(.*) is buffeted by the (?:sandstorm)|(?:hail)!$'
WEATHER_CLEARED = r'.*The effects of the weather disappeared\.$'
PAIN_SPLIT = r'^The battlers shared their pain!$'
FAILED = r'^But it failed!$'
CONFUSE_HIT = r'^It hurt itself in its confusion!$'
ELECTRIC_TERRAIN = r'^.*An electric current ran across the battlefield!$'
ELECTRIC_TERRAIN_END = r'^The electricity disappeared from the battlefield.$'
PSYCHIC_TERRAIN = r'^.*The battlefield got weird!$'
PSYCHIC_TERRAIN_END = r'^The weirdness disappeared from the battlefield!$'
MISTY_TERRAIN = r'^.*Mist swirled around the battlefield!$'
MISTY_TERRAIN_END = r'^The mist disappeared from the battlefield\.$'
GRASSY_TERRAIN = r'^.*Grass grew to cover the battlefield!$'
GRASSY_TERRAIN_END = r'^The grass disappeared from the battlefield\.$'
OPPONENT_GRASSY_HEAL = r'^The opposing (.*)\'s HP was restored\.$'
PLAYER_GRASSY_HEAL = r'^(.*)\'s HP was restored\.$'
TRICK_ROOM = r'^.*twisted the dimensions!$'
TRICK_ROOM_END = r'^The twisted dimensions returned to normal!$'
ITEM_SWITCH = r'^.* switched items with its target!$'
OPPONENT_NO_SWITCH = r'^The opposing (.*) can no longer escape!$'
PLAYER_NO_SWITCH = r'^(.*) can no longer escape!$'
OPPONENT_ROCKY = r'^The opposing (.*) was hurt by the Rocky Helmet!$'
PLAYER_ROCKY = r'^(.*) was hurt by the Rocky Helmet!$'
OPPONENT_CRASH = r'^The opposing (.*) kept going and crashed!$'
PLAYER_CRASH = r'^(.*) kept going and crashed!$'
NORMAL_TO_ELECTRIC = r'^(A deluge of ions showers the battlefield!)|' \
                     r'(\(Normal-type moves become Electric-type after using Plasma Fists\.\))$'
OPPONENT_SHIELDS_DOWN = r'^\[.*\'s Shields Down\]Shields Down deactivated!\((.*) shielded itself\.\)$'
PLAYER_SHIELDS_DOWN = r'^\[.*\'s Shields Down\]Shields Down deactivated!\(The opposing (.*) shielded itself\.\)$'
OPPONENT_HARVEST = r'^\[The opposing .*\'s Harvest\]The opposing (.*) harvested one (.*)!$'
PLAYER_HARVEST = r'^\[.*\'s Harvest\](.*) harvested one (.*)!$'
OPPONENT_MAGNET_RISE = r'^The opposing (.*) levitated with electromagnetism!$'
PLAYER_MAGNET_RISE = r'^(.*) levitated with electromagnetism!$'
OPPONENT_MAGNET_RISE_END = r'^The opposing (.*)\'s electromagnetism wore off!$'
PLAYER_MAGNET_RISE_END = r'^(.*)\'s electromagnetism wore off!$'
OPPONENT_HARSH_LIGHT = r'^The opposing (.*) became cloaked in a harsh light!$'
PLAYER_HARSH_LIGHT = r'^(.*) became cloaked in a harsh light!$'
OPPONENT_FOCUS = r'^The opposing (.*) is tightening its focus!$'
PLAYER_FOCUS = r'^(.*) is tightening its focus!$'
OPPONENT_HURT = r'^The opposing (.*) was hurt!$'
PLAYER_HURT = r'^(.*) was hurt!$'
OPPONENT_ITEM_STEAL = r'^.*The opposing (.*) stole (.*)\'s (.*)!$'
PLAYER_ITEM_STEAL = r'^.*(.*) stole the opposing (.*)\'s (.*)!$'
PERISH_SONG = r'^All Pokémon that heard the song will faint in three turns!$'
OPPONENT_PERISH_COUNT = r'^The opposing (.*)\'s perish count fell to (.*)\.$'
PLAYER_PERISH_COUNT = r'^(.*)\'s perish count fell to (.*)\.$'
OPPONENT_HEALING_WISH = r'^The healing wish came true for the opposing (.*)!$'
PLAYER_HEALING_WISH = r'^The healing wish came true for (.*)!$'
OPPONENT_MAGMA_STORM = r'^The opposing (.*) became trapped by swirling magma!$'
PLAYER_MAGMA_STORM = r'^(.*) became trapped by swirling magma!$'
OPPONENT_MAGMA_STORM_DMG = r'^The opposing (.*) is hurt by Magma Storm!$'
PLAYER_MAGMA_STORM_DMG = r'^(.*) is hurt by Magma Storm!$'
OPPONENT_DIG = r'^The opposing (.*) burrowed its way under the ground!$'
PLAYER_DIG = r'^(.*) burrowed its way under the ground!$'
OPPONENT_BOUNCE = r'^The opposing (.*) sprang up!$'
PLAYER_BOUNCE = r'^(.*) sprang up!$'
OPPONENT_BLACK_SLUDGE = r'^The opposing (.*) was hurt by its Black Sludge!$'
PLAYER_BLACK_SLUDGE = r'^(.*) was hurt by its Black Sludge!$'
OPPONENT_SOLAR_POWER = r'^\[The opposing .*\'s Solar Power\]\(The opposing (.*) was hurt!\)$'
PLAYER_SOLAR_POWER = r'^\[.*\'s Solar Power\]\((.*) was hurt!\)$'
OPPONENT_SHADOW_FORCE = r'^The opposing (.*) vanished instantly!$'
PLAYER_SHADOW_FORCE = r'^(.*) vanished instantly!$'
OPPONENT_DRY_SKIN_DMG = r'^\[The opposing .*\'s Dry Skin\]\(The opposing (.*) was hurt by its Dry Skin\.\)$'
PLAYER_DRY_SKIN_DMG = r'^\[.*\'s Dry Skin\]\((.*) was hurt by its Dry Skin\.\)$'

WIN_MSG = r'^(.*) won the battle!$'

# Ignore messages
IGNORE_1 = r'^But it does not have enough HP left to make a substitute!$'
IGNORE_2 = r'^\(Since gen 7, Dark is immune to Prankster moves\.\)$'
IGNORE_3 = r'^The Pokémon was hit .* time(s)?!$'
IGNORE_4 = r'\[.*\'s Beast Boost\]$'
IGNORE_5 = r'^It\'s not very effective\.\.\.$'
IGNORE_6 = r'^\[.*\'s Pressure\].*$'
IGNORE_7 = r'^The opposing .* surrounded itself with its Z-Power!$'
IGNORE_8 = r'\[.*\'s Speed Boost\]$'
IGNORE_9 = r'^A critical hit!$'
IGNORE_10 = r'^It\'s super effective!$'
IGNORE_11 = r'^\[.*\'s Stamina\]$'
IGNORE_12 = r'^.* had its energy drained!$'
IGNORE_13 = r'^Battle started between .* and .*!$'
IGNORE_14 = r'^.* is already asleep!$'
IGNORE_15 = r'^.* is already paralyzed!$'
IGNORE_16 = r'^\[.*\'s Download\]$'
IGNORE_17 = r'^\(.* ate its .*!\)$'
IGNORE_18 = r'^\[.*\'s Emergency Exit\]'
IGNORE_19 = r'^\[The opposing .*\'s Frisk\]The opposing .* frisked .* and found its .*!$'
IGNORE_20 = r'^\[.*\'s Intimidate\]$'
IGNORE_21 = r'^A bell chimed!$'
IGNORE_22 = r'^\[.*\'s Unnerve\].* team is too nervous to eat Berries!$'
IGNORE_23 = r'^.* is confused!$'
IGNORE_25 = r'^\(The hail is crashing down\.\)$'
IGNORE_26 = r'^\(Rain continues to fall\.\)'
IGNORE_27 = r'^A soothing aroma wafted through the area!$'
IGNORE_28 = r'^\(.* only works on your first turn out\.\)$'
IGNORE_29 = r'^.* surrounded itself with its Z-Power!$'
IGNORE_30 = r'^.* returned its decreased stats to normal using its Z-Power!$'
IGNORE_31 = r'^\[.*\'s Moxie\]$'
IGNORE_32 = r'^\[.*\'s Fairy Aura\].* is radiating a fairy aura!$'
IGNORE_33 = r'^.* floats in the air with its Air Balloon!$'
IGNORE_34 = r'.*\'s Air Balloon popped!$'
IGNORE_35 = r'^.* lost due to inactivity\.$'
IGNORE_36 = r'^.* obtained one .*\.$'
IGNORE_37 = r'^.* forfeited\.$'
IGNORE_38 = r'^.* already has a substitute!'
IGNORE_39 = r'^.* is hoping to take its attacker down with it!$'
IGNORE_40 = r'^.*\'s .* won\'t go any higher!$'
IGNORE_41 = r'^\[.*\'s Turboblaze\].* is radiating a blazing aura!$'
IGNORE_42 = r'^.*\'s stats were not lowered!$'
IGNORE_43 = r'^\(The sandstorm is raging\.\)'
IGNORE_44 = r'^\[.*\'s Mold Breaker\].* breaks the mold!$'
IGNORE_45 = r'^\(The sunlight is strong\.\)$'
IGNORE_46 = r'^\[.*\'s Synchronize\]$'
IGNORE_47 = r'^\[.*\'s Justified\]$'
IGNORE_48 = r'^.* is already burned!$'
IGNORE_49 = r'^\[.*\'s Teravolt\].* is radiating a bursting aura!$'
IGNORE_50 = r'^\[.*\'s Power Construct\]You sense the presence of many!$'
IGNORE_51 = r'^.*\'s illusion wore off!$'
IGNORE_52 = r'^\[.*\'s Aura Break\].* reversed all other Pokémon\'s auras!$'
IGNORE_53 = r'^Bright light is about to burst out of .*!$'
IGNORE_54 = r'^.* was caught in a sticky web!$'
IGNORE_55 = r'^\[.*\'s Competitive\]$'
IGNORE_56 = r'^\[.*\'s Defiant\]'
IGNORE_57 = r'^\[.*\'s Truant\].* is loafing around!$'
IGNORE_58 = r'^\[.*\'s Soul-Heart\]'
IGNORE_59 = r'^\[.*\'s Slow Start\].* can\'t get it going!$'
IGNORE_60 = r'^The Fire-type attack fizzled out in the heavy rain!$'
IGNORE_61 = r'^\[.*\'s Schooling\].* formed a school!$'
IGNORE_62 = r'^\[.*\'s Dark Aura\].* is radiating a dark aura!$'
IGNORE_63 = r'^\[.*\'s Storm Drain\]$'
IGNORE_64 = r'^.* surrounds itself with a protective mist!$'
IGNORE_65 = r'^.* shrouded itself with Magic Coat!$'
IGNORE_66 = r'^.* took its attacker down with it!$'
IGNORE_67 = r'^Sleep Clause Mod activated\.$'
IGNORE_68 = r'^\[.*\'s Battle Bond\].*became fully charged due to its bond with its Trainer!$'
IGNORE_69 = r'^.* became Ash-Greninja!$'
IGNORE_70 = r'\[.*\'s Disguise\]Its disguise served it as a decoy!$'
IGNORE_71 = r'^.* must recharge!$'
IGNORE_72 = r'^\[.*\'s Shed Skin\]$'
IGNORE_73 = r'^\(.* is being withdrawn\.\.\.\)$'
IGNORE_74 = r'^\[.*\'s Tangling Hair\]'
IGNORE_75 = r'^.* is protected by the Psychic Terrain!$'
IGNORE_76 = r'^\[.*\'s Sap Sipper\]$'
IGNORE_77 = r'^\[.*\'s Shields Down\]$'
IGNORE_78 = r'.* has no moves left!$'
IGNORE_79 = r'\[.*\'s Motor Drive\]$'
IGNORE_80 = r'^.*There is no relief from this heavy rain!$'
IGNORE_81 = r'^\[.*\'s Weak Armor\]$'
IGNORE_82 = r'^\[.*\'s Lightning Rod]$'
IGNORE_83 = r'^.*\'s Ability became Mummy!$'
IGNORE_84 = r'^\[.*\'s Comatose\].* is drowsing!$'
IGNORE_85 = r'^\[.*\'s Dancer\]$'
IGNORE_86 = r'^The Water-type attack evaporated in the harsh sunlight!$'
IGNORE_87 = r'^.*The extremely harsh sunlight was not lessened at all!$'
IGNORE_88 = r'^\(A Pokemon can\'t switch between when it runs out of HP and when it faints\)$'
IGNORE_89 = r'^\[.*\'s Steadfast\]$'
IGNORE_90 = 'r^.* can\'t use .*!$'
IGNORE_91 = r'^.* is protected by an aromatic veil!$'
IGNORE_92 = r'^\[.*\'s Shields Down\]Shields Down activated!\(.* stopped shielding itself\.\)$'
IGNORE_93 = r'^.*\'s .* won\'t go any lower!$'
IGNORE_94 = r'^.* lost its focus and couldn\'t move!$'
IGNORE_95 = r'^\[.*\'s Hydration\]$'
IGNORE_96 = r'^\(Psychic Terrain doesn\'t affect Pokémon immune to Ground\.\)$'
IGNORE_97 = r'^.* is protected by the Electric Terrain!$'
IGNORE_98 = r'^.*\'s item cannot be removed!$'
IGNORE_99 = r'^\[.*\'s Water Compaction\]$'
IGNORE_100 = r'^.* can\'t use .*!$'

ILLUSION_MSG = '(More than 4 moves is usually a sign of Illusion Zoroark/Zorua.)'

ITEM_REGEX = [
    ITEM_EATEN,
    ITEM_KNOCKED_OFF,
    ITEM_HARVESTED,
    ITEM_CONSUMED,
    ITEM_FRISKED,
    ITEM_TRICKED,
    ITEM_POPPED
]

VARIED_RESULT_LIST = [
    OPPONENT_POISON,
    PLAYER_POISON,
    OPPONENT_STONE_DMG,
    PLAYER_STONE_DMG,
    OPPONENT_SPIKE_DMG,
    PLAYER_SPIKE_DMG,
    OPPONENT_WISH,
    PLAYER_WISH,
]

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
    OPPONENT_Z_BOOST,
    PLAYER_Z_BOOST,
    STATS_RESET,
    OPPONENT_STAT_RESET,
    PLAYER_STAT_RESET,
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
    OPPONENT_SET_SUB,
    PLAYER_SET_SUB,
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
    OPPONENT_POISON_HEAL,
    PLAYER_POISON_HEAL,
    OPPONENT_DROWSY,
    PLAYER_DROWSY,
    OPPONENT_SLEEP,
    PLAYER_SLEEP,
    OPPONENT_ASLEEP,
    PLAYER_ASLEEP,
    OPPONENT_WAKE,
    PLAYER_WAKE,
    OPPONENT_FROZE,
    PLAYER_FROZE,
    OPPONENT_FROZEN,
    PLAYER_FROZEN,
    OPPONENT_THAW,
    PLAYER_THAW,
    OPPONENT_MOVE_THAW,
    PLAYER_MOVE_THAW,
    OPPONENT_PARALYZE,
    PLAYER_PARALYZE,
    OPPONENT_PARALYZED,
    PLAYER_PARALYZED,
    OPPONENT_PARALYZE_HEAL,
    PLAYER_PARALYZE_HEAL,
    OPPONENT_CONFUSE,
    PLAYER_CONFUSE,
    OPPONENT_CONFUSE_2,
    PLAYER_CONFUSE_2,
    OPPONENT_CONFUSE_END,
    PLAYER_CONFUSE_END,
    OPPONENT_INFESTATION,
    PLAYER_INFESTATION,
    OPPONENT_INFESTATION_DMG,
    PLAYER_INFESTATION_DMG,
    OPPONENT_INFESTATION_END,
    PLAYER_INFESTATION_END,
    OPPONENT_STATUS_CURE,
    PLAYER_STATUS_CURE,
    OPPONENT_KNOCKOFF,
    PLAYER_KNOCKOFF,
    OPPONENT_LIFEORB,
    PLAYER_LIFEORB,
    OPPONENT_IMMUNE,
    PLAYER_IMMUNE,
    OPPONENT_PROTECT,
    PLAYER_PROTECT,
    OPPONENT_PROTECT_DMG,
    PLAYER_PROTECT_DMG,
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
    OPPONENT_FASTER,
    PLAYER_FASTER,
    OPPONENT_REST,
    PLAYER_REST,
    OPPONENT_LOSE_TYPE,
    PLAYER_LOSE_TYPE,
    OPPONENT_CHANGE_TYPE,
    PLAYER_CHANGE_TYPE,
    OPPONENT_SET_WEB,
    PLAYER_SET_WEB,
    OPPONENT_WEB_CLEAR,
    PLAYER_WEB_CLEAR,
    OPPONENT_SET_STONE,
    PLAYER_SET_STONE,
    OPPONENT_STONE_CLEAR,
    PLAYER_STONE_CLEAR,
    OPPONENT_SET_SPIKE,
    PLAYER_SET_SPIKE,
    OPPONENT_SPIKE_CLEAR,
    PLAYER_SPIKE_CLEAR,
    OPPONENT_SET_POISON,
    PLAYER_SET_POISON,
    OPPONENT_POISON_CLEAR,
    PLAYER_POISON_CLEAR,
    OPPONENT_STONE_CLEAR,
    PLAYER_STONE_CLEAR,
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
    OPPONENT_TAUNT,
    PLAYER_TAUNT,
    OPPONENT_TAUNT_END,
    PLAYER_TAUNT_END,
    OPPONENT_ENCORE,
    PLAYER_ENCORE,
    OPPONENT_ENCORE_END,
    PLAYER_ENCORE_END,
    OPPONENT_STURDY,
    PLAYER_STURDY,
    PAIN_SPLIT,
    OPPONENT_FORM,
    PLAYER_FORM,
    OPPONENT_TRANSFORM,
    PLAYER_TRANSFORM,
    OPPONENT_TRANSFORM_2,
    PLAYER_TRANSFORM_2,
    OPPONENT_MAGIC_BOUNCE,
    PLAYER_MAGIC_BOUNCE,
    OPPONENT_DITTO,
    PLAYER_DITTO,
    OPPONENT_PROTEAN,
    PLAYER_PROTEAN,
    OPPONENT_DISABLE,
    PLAYER_DISABLE,
    OPPONENT_DISABLE_END,
    PLAYER_DISABLE_END,
    OPPONENT_ULTRA_BURST,
    PLAYER_ULTRA_BURST,
    OPPONENT_PRIMAL,
    PLAYER_PRIMAL,
    OPPONENT_DISGUISE,
    PLAYER_DISGUISE,
    OPPONENT_BAD_DREAMS,
    PLAYER_BAD_DREAMS,
    OPPONENT_FLASH_FIRE,
    PLAYER_FLASH_FIRE,
    OPPONENT_AFTERMATH,
    PLAYER_AFTERMATH,
    OPPONENT_SCHOOL_END,
    PLAYER_SCHOOL_END,
    OPPONENT_CANNOT_USE,
    PLAYER_CANNOT_USE,
    OPPONENT_CONTACT,
    PLAYER_CONTACT,
    OPPONENT_OOZE_DMG,
    PLAYER_OOZE_DMG,
    OPPONENT_TAUNT_FAIL,
    PLAYER_TAUNT_FAIL,
    OPPONENT_HAIL_DMG,
    PLAYER_HAIL_DMG,
    OPPONENT_ABSORB,
    PLAYER_ABSORB,
    OPPONENT_HEAT_BEAK,
    PLAYER_HEAT_BEAK,
    OPPONENT_POWER_HERB,
    PLAYER_POWER_HERB,
    OPPONENT_WHITE_HERB,
    PLAYER_WHITE_HERB,
    OPPONENT_FLINCH,
    PLAYER_FLINCH,
    OPPONENT_BELLY_DRUM,
    PLAYER_BELLY_DRUM,
    OPPONENT_LIGHT_SCREEN,
    PLAYER_LIGHT_SCREEN,
    OPPONENT_WORE_OFF,
    PLAYER_WORE_OFF,
    OPPONENT_REFLECT,
    PLAYER_REFLECT,
    OPPONENT_VEIL,
    PLAYER_VEIL,
    OPPONENT_TAILWIND,
    PLAYER_TAILWIND,
    OPPONENT_TAILWIND_END,
    PLAYER_TAILWIND_END,
    OPPONENT_SLOW_END,
    PLAYER_SLOW_END,
    OPPONENT_GROUNDED,
    PLAYER_GROUNDED,
    OPPONENT_FLY,
    PLAYER_FLY,
    RAIN,
    RAIN_END,
    RAIN_HEAVY,
    RAIN_HEAVY_END,
    HAIL,
    HAIL_STOP,
    SUN,
    SUN_EXTREME,
    SUN_EXTREME_END,
    SUN_END,
    SANDSTORM,
    SANDSTORM_END,
    OPPONENT_WEATHER_DMG,
    PLAYER_WEATHER_DMG,
    WEATHER_CLEARED,
    FAILED,
    CONFUSE_HIT,
    ELECTRIC_TERRAIN,
    ELECTRIC_TERRAIN_END,
    PSYCHIC_TERRAIN,
    PSYCHIC_TERRAIN_END,
    MISTY_TERRAIN,
    MISTY_TERRAIN_END,
    GRASSY_TERRAIN,
    GRASSY_TERRAIN_END,
    OPPONENT_GRASSY_HEAL,
    PLAYER_GRASSY_HEAL,
    TRICK_ROOM,
    TRICK_ROOM_END,
    ITEM_SWITCH,
    OPPONENT_NO_SWITCH,
    PLAYER_NO_SWITCH,
    OPPONENT_ROCKY,
    PLAYER_ROCKY,
    NORMAL_TO_ELECTRIC,
    OPPONENT_CRASH,
    PLAYER_CRASH,
    OPPONENT_SHIELDS_DOWN,
    PLAYER_SHIELDS_DOWN,
    OPPONENT_HARVEST,
    PLAYER_HARVEST,
    OPPONENT_MAGNET_RISE,
    PLAYER_MAGNET_RISE,
    OPPONENT_MAGNET_RISE_END,
    PLAYER_MAGNET_RISE_END,
    OPPONENT_HARSH_LIGHT,
    PLAYER_HARSH_LIGHT,
    OPPONENT_FOCUS,
    PLAYER_FOCUS,
    OPPONENT_HURT,
    PLAYER_HURT,
    OPPONENT_ITEM_STEAL,
    PLAYER_ITEM_STEAL,
    PERISH_SONG,
    OPPONENT_PERISH_COUNT,
    PLAYER_PERISH_COUNT,
    OPPONENT_HEALING_WISH,
    PLAYER_HEALING_WISH,
    OPPONENT_MAGMA_STORM,
    PLAYER_MAGMA_STORM,
    OPPONENT_MAGMA_STORM_DMG,
    PLAYER_MAGMA_STORM_DMG,
    OPPONENT_DIG,
    PLAYER_DIG,
    OPPONENT_BOUNCE,
    PLAYER_BOUNCE,
    OPPONENT_BLACK_SLUDGE,
    PLAYER_BLACK_SLUDGE,
    OPPONENT_SOLAR_POWER,
    PLAYER_SOLAR_POWER,
    OPPONENT_SHADOW_FORCE,
    PLAYER_SHADOW_FORCE,
    OPPONENT_DRY_SKIN_DMG,
    PLAYER_DRY_SKIN_DMG
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
    IGNORE_40,
    IGNORE_41,
    IGNORE_42,
    IGNORE_43,
    IGNORE_44,
    IGNORE_45,
    IGNORE_46,
    IGNORE_47,
    IGNORE_48,
    IGNORE_49,
    IGNORE_50,
    IGNORE_51,
    IGNORE_52,
    IGNORE_53,
    IGNORE_54,
    IGNORE_55,
    IGNORE_56,
    IGNORE_57,
    IGNORE_58,
    IGNORE_59,
    IGNORE_60,
    IGNORE_61,
    IGNORE_62,
    IGNORE_63,
    IGNORE_64,
    IGNORE_65,
    IGNORE_66,
    IGNORE_67,
    IGNORE_68,
    IGNORE_69,
    IGNORE_70,
    IGNORE_71,
    IGNORE_72,
    IGNORE_73,
    IGNORE_74,
    IGNORE_75,
    IGNORE_76,
    IGNORE_77,
    IGNORE_78,
    IGNORE_79,
    IGNORE_80,
    IGNORE_81,
    IGNORE_82,
    IGNORE_83,
    IGNORE_84,
    IGNORE_85,
    IGNORE_86,
    IGNORE_87,
    IGNORE_88,
    IGNORE_89,
    IGNORE_90,
    IGNORE_91,
    IGNORE_92,
    IGNORE_93,
    IGNORE_94,
    IGNORE_95,
    IGNORE_96,
    IGNORE_97,
    IGNORE_98,
    IGNORE_99,
    IGNORE_100
]

MSG_DICT = {
    OPPONENT_MOVE: 'Opponent {} used {}',
    OPPONENT_Z_MOVE: 'Opponent {} used {} Z-move',
    PLAYER_Z_MOVE: 'Player {} used {} Z-move',
    PLAYER_MOVE: 'Player {} used {}',
    OPPONENT_DAMAGE: 'Opponent {} -{} health',
    PLAYER_DAMAGE: 'Player {} -{} health',
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
    OPPONENT_STAT_RAISE_WEAKNESS: 'Opponent {} {} +2',
    PLAYER_STAT_RAISE_WEAKNESS: 'Player {} {} +2',
    OPPONENT_Z_BOOST: 'Opponent {} {} +1',
    PLAYER_Z_BOOST: 'Player {} {} +1',
    STATS_RESET: 'Stats reset',
    OPPONENT_STAT_RESET: 'Opponent {} stats reset',
    PLAYER_STAT_RESET: 'Player {} stats reset',
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
    OPPONENT_DODGE: 'Opponent {} -0% health',
    PLAYER_DODGE: 'Player {} -0% health',
    OPPONENT_LEFTOVERS: 'Opponent {} +6.25% health',
    PLAYER_LEFTOVERS: 'Player {} +6.25% health',
    OPPONENT_SET_SUB: 'Opponent {} set substitute',
    PLAYER_SET_SUB: 'Player {} set substitute',
    OPPONENT_SUBSTITUTE: 'Substitute protected Opponent {}',
    PLAYER_SUBSTITUTE: 'Substitute protected Player {}',
    OPPOSING_SUBSTITUTE_FADED: 'Opponent {} substitute faded',
    PLAYER_SUBSTITUTE_FADED: 'Player {} substitute faded',
    PLAYER_FRISK: 'Player {} found {} {}',
    OPPONENT_BURNED: 'Opponent {} burned',
    PLAYER_BURNED: 'Player {} burned',
    OPPONENT_BURN: 'Opponent {} -6.25% health',
    PLAYER_BURN: 'Player {} -6.25% health',
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
    OPPONENT_MOVE_THAW: 'Opponent {} thawed',
    PLAYER_MOVE_THAW: 'Player {} thawed',
    OPPONENT_PARALYZE: 'Opponent {} paralyze',
    PLAYER_PARALYZE: 'Player {} paralyze',
    OPPONENT_PARALYZED: 'Opponent {} paralyzed',
    PLAYER_PARALYZED: 'Player {} paralyzed',
    OPPONENT_PARALYZE_HEAL: 'Opponent {} paralyze heal',
    PLAYER_PARALYZE_HEAL: 'Player {} paralyze heal',
    OPPONENT_CONFUSE: 'Opponent {} confused',
    OPPONENT_CONFUSE_2: 'Opponent {} confused',
    PLAYER_CONFUSE_2: 'Player {} confused',
    PLAYER_CONFUSE: 'Player {} confused',
    OPPONENT_CONFUSE_END: 'Opponent {} confuse end',
    PLAYER_CONFUSE_END: 'Player {} confuse end',
    OPPONENT_INFESTATION: 'Opponent {} infestation',
    PLAYER_INFESTATION: 'Player {} infestation',
    OPPONENT_INFESTATION_DMG: 'Opponent {} -12.5% health',
    PLAYER_INFESTATION_DMG: 'Player {} -12.5% health',
    OPPONENT_INFESTATION_END: 'Opponent {} infestation end',
    PLAYER_INFESTATION_END: 'Player {} infestation end',
    OPPONENT_STATUS_CURE: 'Opponent {} status cured',
    PLAYER_STATUS_CURE: 'Player {} status cured',
    OPPONENT_KNOCKOFF: 'Opponent {} knocked off Player {} {}',
    PLAYER_KNOCKOFF: 'Player {} knocked off Opponent {} {}',
    OPPONENT_LIFEORB: 'Opponent {} -10% health',
    PLAYER_LIFEORB: 'Player {} -10% health',
    OPPONENT_IMMUNE: 'Opponent {} -0% health',
    PLAYER_IMMUNE: 'Player {} -0% health',
    OPPONENT_PROTECT: 'Opponent {} -0% health',
    PLAYER_PROTECT: 'Player {} -0% health',
    OPPONENT_PROTECT_DMG: 'Opponent {} protect dmg',
    PLAYER_PROTECT_DMG: 'Player {} protect dmg',
    OPPONENT_SEEDED: 'Opponent {} seeded',
    PLAYER_SEEDED: 'Player {} seeded',
    OPPONENT_SEEDED_DMG: 'Opponent {} -12.5% health',
    PLAYER_SEEDED_DMG: 'Player {} -12.5% health',
    OPPONENT_HEAL: 'Opponent {} healed',
    PLAYER_HEAL: 'Player {} healed',
    OPPONENT_FULL_HP: 'Opponent {} full HP',
    PLAYER_FULL_HP: 'Player {} full HP',
    OPPONENT_BERRY: 'Opponent {} +25% health',
    PLAYER_BERRY: 'Player {} +25% health',
    OPPONENT_FASTER: 'Opponent {} moved faster due to {}',
    PLAYER_FASTER: 'Player {} moved faster due to {}',
    OPPONENT_REST: 'Opponent {} rested',
    PLAYER_REST: 'Player {} rested',
    OPPONENT_LOSE_TYPE: 'Opponent {} lost {}',
    PLAYER_LOSE_TYPE: 'Player {} lost {}',
    OPPONENT_CHANGE_TYPE: 'Opponent {} changed to {}',
    PLAYER_CHANGE_TYPE: 'Player {} changed to {}',
    OPPONENT_SET_WEB: 'Opponent set web',
    PLAYER_SET_WEB: 'Player set web',
    OPPONENT_WEB_CLEAR: 'Opponent clear web',
    PLAYER_WEB_CLEAR: 'Player clear web',
    OPPONENT_SET_STONE: 'Opponent set stone',
    PLAYER_SET_STONE: 'Player set stone',
    OPPONENT_SET_SPIKE: 'Opponent set spike',
    PLAYER_SET_SPIKE: 'Player set spike',
    OPPONENT_SET_POISON: 'Opponent set poison',
    PLAYER_SET_POISON: 'Player set poison',
    OPPONENT_POISON_CLEAR: 'Opponent cleared poison',
    PLAYER_POISON_CLEAR: 'Player cleared poison',
    OPPONENT_STONE_DMG: 'Opponent {} stone dmg',
    PLAYER_STONE_DMG: 'Player {} stone dmg',
    OPPONENT_STONE_CLEAR: 'Opponent cleared stone',
    PLAYER_STONE_CLEAR: 'Player cleared stone',
    OPPONENT_SPIKE_DMG: 'Opponent {} spike dmg',
    PLAYER_SPIKE_DMG: 'Player {} spike dmg',
    OPPONENT_SPIKE_CLEAR: 'Opponent cleared spike',
    PLAYER_SPIKE_CLEAR: 'Player cleared spike',
    OPPONENT_DRAGGED: 'Opponent {} dragged in',
    PLAYER_DRAGGED: 'Player {} dragged in',
    OPPONENT_NIMBLE: 'Opponent {} nimble',
    PLAYER_NIMBLE: 'Player {} nimble',
    OPPONENT_WEAKNESS_POLICY: 'Opponent {} Weakness Policy',
    PLAYER_WEAKNESS_POLICY: 'Player {} Weakness Policy',
    OPPONENT_TRACE: 'Opponent {} took Player {} {}',
    PLAYER_TRACE: 'Player {} took Opponent {} {}',
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
    OPPONENT_TRANSFORM: 'Opponent {} changed to Complete Forme',
    PLAYER_TRANSFORM: 'Player {} changed to Complete Forme',
    OPPONENT_TRANSFORM_2: 'Opponent {} transformed',
    PLAYER_TRANSFORM_2: 'Player {} transformed',
    OPPONENT_DITTO: 'Opponent {} transformed into {}',
    PLAYER_DITTO: 'Player {} transformed into {}',
    OPPONENT_MAGIC_BOUNCE: 'Opponent {} bounced {} back',
    PLAYER_MAGIC_BOUNCE: 'Player {} bounced {} back',
    OPPONENT_STURDY: 'Opponent {} sturdy',
    PLAYER_STURDY: 'Player {} sturdy',
    OPPONENT_WISH: 'Opponent active +50% health',
    PLAYER_WISH: 'Player active +50% health',
    OPPONENT_PROTEAN: 'Opponent {} changed to {}',
    PLAYER_PROTEAN: 'Player {} changed to {}',
    OPPONENT_DISABLE: 'Player {} {} disabled',
    PLAYER_DISABLE: 'Opponent {} {} disabled',
    OPPONENT_DISABLE_END: 'Opponent {} not disabled',
    PLAYER_DISABLE_END: 'Player {} not disabled',
    OPPONENT_ULTRA_BURST: 'Opponent {} ultra burst',
    PLAYER_ULTRA_BURST: 'Player {} ultra burst',
    OPPONENT_PRIMAL: 'Opponent {} primal',
    PLAYER_PRIMAL: 'Player {} primal',
    OPPONENT_AFTERMATH: 'Player {} hurt by aftermath',
    PLAYER_AFTERMATH: 'Opponent {} hurt by aftermath',
    OPPONENT_DISGUISE: 'Opponent {} disguise broke',
    PLAYER_DISGUISE: 'Player {} disguise broke',
    OPPONENT_BAD_DREAMS: 'Player {} -12.5% health',
    PLAYER_BAD_DREAMS: 'Opponent {} -12.5% health',
    OPPONENT_FLASH_FIRE: 'Opponent {} Flash Fire',
    PLAYER_FLASH_FIRE: 'Player {} Flash Fire',
    OPPONENT_SCHOOL_END: 'Opponent {} school end',
    PLAYER_SCHOOL_END: 'Player {} school end',
    OPPONENT_CANNOT_USE: 'Opponent {} cannot use {}',
    PLAYER_CANNOT_USE: 'Player {} cannot use {}',
    OPPONENT_CONTACT: 'Player {} -12.5% health',
    PLAYER_CONTACT: 'Opponent {} -12.5% health',
    OPPONENT_OOZE_DMG: 'Opponent {} ooze dmg',
    PLAYER_OOZE_DMG: 'Player {} ooze dmg',
    OPPONENT_TAUNT_FAIL: 'Opponent {} move failed to taunt',
    PLAYER_TAUNT_FAIL: 'Player {} move failed to taunt',
    OPPONENT_HAIL_DMG: 'Opponent {} -6.25% health',
    PLAYER_HAIL_DMG: 'Player {} -6.25% health',
    OPPONENT_ABSORB: 'Opponent {} absorb {}',
    PLAYER_ABSORB: 'Player {} absorb {}',
    OPPONENT_HEAT_BEAK: 'Opponent {} heat beak',
    PLAYER_HEAT_BEAK: 'Player {} heat beak',
    OPPONENT_POWER_HERB: 'Opponent {} Power Herb',
    PLAYER_POWER_HERB: 'Player {} Power Herb',
    OPPONENT_WHITE_HERB: 'Opponent {} stats reset',
    PLAYER_WHITE_HERB: 'Player {} stats reset',
    OPPONENT_FLINCH: 'Opponent {} flinch',
    PLAYER_FLINCH: 'Player {} flinch',
    OPPONENT_BELLY_DRUM: 'Opponent {} -50% health, Attack +6',
    PLAYER_BELLY_DRUM: 'Player {} -50% health, attack +6',
    OPPONENT_LIGHT_SCREEN: 'Opponent Light Screen',
    PLAYER_LIGHT_SCREEN: 'Player Light Screen',
    OPPONENT_WORE_OFF: 'Opponent {} end',
    PLAYER_WORE_OFF: 'Player {} end',
    OPPONENT_REFLECT: 'Opponent Reflect',
    PLAYER_REFLECT: 'Player Reflect',
    OPPONENT_VEIL: 'Opponent Aurora Veil',
    PLAYER_VEIL: 'Player Aurora Veil',
    OPPONENT_TAILWIND: 'Opponent Tailwind',
    PLAYER_TAILWIND: 'Player Tailwind',
    OPPONENT_TAILWIND_END: 'Opponent Tailwind end',
    PLAYER_TAILWIND_END: 'Player Tailwind end',
    OPPONENT_SLOW_END: 'Opponent {} slow end',
    PLAYER_SLOW_END: 'Player {} slow end',
    OPPONENT_GROUNDED: 'Opponent {} grounded',
    PLAYER_GROUNDED: 'Player {} grounded',
    OPPONENT_FLY: 'Opponent {} fly',
    PLAYER_FLY: 'Player {} fly',
    PAIN_SPLIT: 'Pain split',
    RAIN: 'Rain',
    RAIN_END: 'Rain end',
    RAIN_HEAVY: 'Heavy Rain',
    RAIN_HEAVY_END: 'Heavy Rain end',
    HAIL: 'Hail',
    HAIL_STOP: 'Hail stop',
    SUN: 'Harsh sun',
    SUN_EXTREME: 'Extreme sun',
    SUN_EXTREME_END: 'Extreme sun end',
    SUN_END: 'Sun end',
    SANDSTORM: 'Sandstorm',
    SANDSTORM_END: 'Sandstorm end',
    OPPONENT_WEATHER_DMG: 'Opponent {} -6.25% health',
    PLAYER_WEATHER_DMG: 'Player {} -6.25% health',
    WEATHER_CLEARED: 'Weather cleared',
    FAILED: 'Move failed',
    CONFUSE_HIT: 'Confuse hit',
    ELECTRIC_TERRAIN: 'Electric terrain',
    ELECTRIC_TERRAIN_END: 'Electric terrain end',
    PSYCHIC_TERRAIN: 'Psychic terrain',
    PSYCHIC_TERRAIN_END: 'Psychic terrain end',
    MISTY_TERRAIN: 'Misty terrain',
    MISTY_TERRAIN_END: 'Misty terrain end',
    GRASSY_TERRAIN: 'Grassy terrain',
    GRASSY_TERRAIN_END: 'Grassy terrain end',
    OPPONENT_GRASSY_HEAL: 'Opponent {} +6.25% health',
    PLAYER_GRASSY_HEAL: 'Player {} +6.25% health',
    TRICK_ROOM: 'Trick room',
    TRICK_ROOM_END: 'Trick room end',
    ITEM_SWITCH: 'Item swap',
    OPPONENT_NO_SWITCH: 'Opponent {} cannot switch',
    PLAYER_NO_SWITCH: 'Player {} cannot switch',
    OPPONENT_ROCKY: 'Opponent {} -16.7% health',
    PLAYER_ROCKY: 'Player {} -16.7% health',
    OPPONENT_CRASH: 'Opponent {} -50% health',
    PLAYER_CRASH: 'Player {} -50% health',
    NORMAL_TO_ELECTRIC: 'Normal moves became Electric',
    OPPONENT_SHIELDS_DOWN: 'Opponent {} Shields Down deactivate',
    PLAYER_SHIELDS_DOWN: 'Player {} Shields Down deactivate',
    OPPONENT_HARVEST: 'Opponent {} harvest {}',
    PLAYER_HARVEST: 'Player {} harvest {}',
    OPPONENT_MAGNET_RISE: 'Opponent {} magnet rise',
    PLAYER_MAGNET_RISE: 'Player {} magnet rise',
    OPPONENT_MAGNET_RISE_END: 'Opponent {} magnet rise end',
    PLAYER_MAGNET_RISE_END: 'Player {} magnet rise end',
    OPPONENT_HARSH_LIGHT: 'Opponent {} harsh light',
    PLAYER_HARSH_LIGHT: 'Player {} harsh light',
    OPPONENT_FOCUS: 'Opponent {} tighten focus',
    PLAYER_FOCUS: 'Player {} tighten focus',
    OPPONENT_HURT: 'Opponent {} hurt',
    PLAYER_HURT: 'Player {} hurt',
    OPPONENT_ITEM_STEAL: 'Opponent {} stole Player {} {}',
    PLAYER_ITEM_STEAL: 'Player {} stole Opponent {} {}',
    PERISH_SONG: 'Perish song began',
    OPPONENT_PERISH_COUNT: 'Opponent {} perish count {}',
    PLAYER_PERISH_COUNT: 'Player {} perish count {}',
    OPPONENT_HEALING_WISH: 'Opponent {} +100% health, status cured',
    PLAYER_HEALING_WISH: 'Player {} +100% health, status cured',
    OPPONENT_MAGMA_STORM: 'Opponent {} Magma Storm',
    PLAYER_MAGMA_STORM: 'Player {} Magma Storm',
    OPPONENT_MAGMA_STORM_DMG: 'Opponent {} -6.25% health',
    PLAYER_MAGMA_STORM_DMG: 'Player {} -6.25% health',
    OPPONENT_DIG: 'Opponent {} dig',
    PLAYER_DIG: 'Player {} dig',
    OPPONENT_BOUNCE: 'Opponent {} bounce',
    PLAYER_BOUNCE: 'Player {} bounce',
    OPPONENT_BLACK_SLUDGE: 'Opponent {} -12.5% health',
    PLAYER_BLACK_SLUDGE: 'Player {} -12.5% health',
    OPPONENT_SOLAR_POWER: 'Opponent {} -12.5% health',
    PLAYER_SOLAR_POWER: 'Player {} -12.5% health',
    OPPONENT_SHADOW_FORCE: 'Opponent {} shadow force',
    PLAYER_SHADOW_FORCE: 'Player {} shadow force',
    OPPONENT_DRY_SKIN_DMG: 'Opponent {} -12.5% health',
    PLAYER_DRY_SKIN_DMG: 'Player {} -12.5% health'
}
