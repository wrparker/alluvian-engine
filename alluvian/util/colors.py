class Colors:
    class fg:
        BLACK   = '\033[30m'
        RED     = '\033[31m'
        GREEN   = '\033[32m'
        YELLOW  = '\033[33m'
        BLUE    = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN    = '\033[36m'
        WHITE   = '\033[37m'
        RESET   = '\033[0m'

        BBLACK = '\033[1;30m'
        BRED = '\033[1;31m'
        BGREEN = '\033[1;32m'
        BYELLOW = '\033[1;33m'
        BBLUE = '\033[1;34m'
        BMAGENTA = '\033[1;35m'
        BCYAN = '\033[1;36m'
        BWHITE = '\033[1;37m'

    class bg:
        BLACK   = '\033[40m'
        RED     = '\033[41m'
        GREEN   = '\033[42m'
        YELLOW  = '\033[43m'
        BLUE    = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN    = '\033[46m'
        WHITE   = '\033[47m'
        RESET   = '\033[49m'

    class style:
        BRIGHT    = '\033[1m'
        DIM       = '\033[2m'
        NORMAL    = '\033[22m'
        RESET_ALL = '\033[0m'
        REVERSE   = '\033[7m'

    REGEX_MAP = [
        ('@n', fg.RESET),

        ('@d', fg.BLACK),
        ('@D', fg.BBLACK),
        ('@0', bg.BLACK),
        ('@b', fg.BLUE),
        ('@B', fg.BBLUE),
        ('@1', bg.BLUE),
        ('@g', fg.GREEN),
        ('@G', fg.BGREEN),
        ('@c', fg.CYAN),
        ('@C', fg.BCYAN),
        ('@3', bg.CYAN),
        ('@r', fg.RED),
        ('@R', fg.BRED),
        ('@4', bg.RED),
        ('@m', fg.MAGENTA),
        ('@M', fg.BMAGENTA),
        ('@5', bg.MAGENTA),
        ('@y', fg.YELLOW),
        ('@Y', fg.BYELLOW),
        ('@6', bg.YELLOW),
        ('@w', fg.WHITE),
        ('@W', fg.BWHITE),
        ('@7', bg.WHITE),

        #TODO: Add styles
    ]
