# config.nu
#
# Installed by:
# version = "0.102.0"
#
# This file is used to override default Nushell settings, define
# (or import) custom commands, or run any other startup tasks.
# See https://www.nushell.sh/book/configuration.html
#
# This file is loaded after env.nu and before login.nu
#
# You can open this file in your default editor using:
# config nu
#
# See `help config nu` for more options
#
# You can remove these comments if you want or leave
# them for future reference.

source ~/.oh-my-posh.nu

##########################################################
# CONFIG
##########################################################
$env.config.buffer_editor = "code"
$env.config.show_banner = false

##########################################################
# ALIASES
##########################################################

alias windotfiles = cd $"($env.USERPROFILE)/windotfiles/"
alias show_path = echo $env.PATH

def update-winwal [wallpaper : string] {
    python -- $"($env.USERPROFILE)/windotfiles/scripts/update_winwal_colors.py" $"($wallpaper)"
}

# Fix jumping when pressing any key
$env.config.shell_integration.osc133 = false

fastfetch
