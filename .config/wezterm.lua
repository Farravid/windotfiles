-- Pull in the wezterm API
local wezterm = require 'wezterm'

-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices

config.font = wezterm.font('JetBrainsMonoNL NF')
config.font_size = 13

config.hide_tab_bar_if_only_one_tab = true

-- For example, changing the color scheme:
config.color_scheme = 'AdventureTime'

config.default_prog = {'nu'}
-- config.default_prog = { 'pwsh.exe', '-l' }

config.window_background_opacity = 0.9
config.window_decorations = "RESIZE"

config.window_padding = {
    left = 30,
    right = 30,
    top = 10,
    bottom = 0,
  }

-- and finally, return the configuration to wezterm
return config