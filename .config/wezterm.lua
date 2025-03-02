-- Pull in the wezterm API
local wezterm = require 'wezterm'

-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices

config.font = wezterm.font('JetBrainsMonoNL NF', { weight = 'Bold', italic = true })
config.font_size = 11

-- For example, changing the color scheme:
config.color_scheme = 'AdventureTime'

-- IMPORTANT: Sets WSL2 UBUNTU-22.04 as the defualt when opening Wezterm
-- config.default_domain = 'WSL:Ubuntu-22.04'
-- Spawn a fish shell in login mode
config.default_prog = { 'nu'}
-- config.default_prog = { 'pwsh.exe', '-l' }

-- and finally, return the configuration to wezterm
return config