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

oh-my-posh init nu --config $"($env.USERPROFILE)/.cache/wal/posh-wal-atomic.omp.json"

##########################################################
# CONFIG
##########################################################
$env.config.buffer_editor = "nvim"
$env.EDITOR = "nvim"
$env.config.show_banner = false

##########################################################
# ALIASES
##########################################################

alias dot = cd $"($env.USERPROFILE)/windotfiles/"
alias dot-update = python -- $"($env.USERPROFILE)/windotfiles/scripts/update.py"
alias dot-winwal = python -- $"($env.USERPROFILE)/windotfiles/scripts/update_winwal_colors.py"
alias dot-setups = python -- $"($env.USERPROFILE)/windotfiles/scripts/setup_editor.py"
alias doc = cd $"($env.USERPROFILE)/Documents/"
alias repos = cd $"($env.USERPROFILE)/Documents/Github/"
alias down = cd $"($env.USERPROFILE)/Downloads/"
alias appd = cd $env.APPDATA
alias appdl = cd $env.LOCALAPPDATA
alias show_path = echo $env.PATH

def --env unreal-claude [] {
    cd W:\Carousel\
    claude
}

def --env dot-oc [] {
    dot
    ^opencode
}

def --env volumen-oc [] {
    volumen
    ^opencode
}

def --env dot-nv [] {
    dot
    ^nvim
}

def --env volumen-nv [] {
    volumen
    ^nvim
}

# yazi: quit with `q` changes the shell's cwd to where you browsed
def --env y [...args] {
    let tmp = (mktemp -t "yazi-cwd.XXXXXX")
    yazi ...$args --cwd-file $tmp
    let cwd = (open $tmp)
    if $cwd != "" and $cwd != $env.PWD { cd $cwd }
    rm -fp $tmp
}

##########################################################
# OTHER
##########################################################

# Fix jumping when pressing any key
$env.config.shell_integration.osc133 = false

sleep 200ms
fastfetch
