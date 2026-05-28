VIRTUAL_W = 800
VIRTUAL_H = 600
FPS = 60
TITLE = "The Hunted"
FLOOR_Y = 490.0

# Physics
GRAVITY       = 0.5
JUMP_POWER    = -14.0   # negative = upward
MAX_FALL_SPEED = 14.0
ACCEL         = 1.5     # horizontal acceleration per frame
FRICTION      = 0.75    # horizontal deceleration multiplier
PLAYER_SPEED  = 5.0
VAMPIRE_SPEED = 6.5

# Combat
MAX_HP         = 100
BULLET_DAMAGE  = 10
CONTACT_DAMAGE = 1      # HP per frame while vampire overlaps peasant
SHOOT_COOLDOWN = 18     # frames between shots
BULLET_SPEED   = 5
BULLET_RADIUS  = 5
MAX_BULLETS    = 5

# Colors
RED        = (255,   0,   0)
BLUE       = (  0,   0, 255)
YELLOW     = (255, 255,   0)
MAROON     = (128,   0,   0)
GREEN      = (  0, 128,   0)
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
DARK_BG    = ( 15,  15,  25)
PANEL_BG   = ( 20,  20,  35)
HP_GREEN   = ( 50, 210,  80)
HP_YELLOW  = (230, 200,  30)
HP_RED     = (220,  40,  40)
LIGHT_GREY = (180, 180, 180)
MID_GREY   = ( 90,  90, 110)

# Levels  — platform y must end in 0 so velocity steps land cleanly
LEVELS = [
    {
        'name': 'Classic',
        'platforms': [
            ((  0, 400), 300, 50),
            ((500, 400), 300, 50),
            ((250, 250), 300, 50),
        ],
    },
    {
        'name': 'Towers',
        'platforms': [
            ((  0, 430), 220, 30),
            ((580, 430), 220, 30),
            ((150, 300), 220, 30),
            ((430, 300), 220, 30),
            ((310, 170), 180, 30),
        ],
    },
    {
        'name': 'Arena',
        'platforms': [
            (( 50, 480), 160, 20),
            ((590, 480), 160, 20),
            ((200, 370), 180, 20),
            ((420, 370), 180, 20),
            ((  0, 260), 200, 20),
            ((600, 260), 200, 20),
            ((300, 190), 200, 20),
        ],
    },
]

# Keep for backwards-compat during transition
PLATFORM_DEFS = LEVELS[0]['platforms']
