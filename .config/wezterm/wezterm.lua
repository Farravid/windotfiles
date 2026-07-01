-- Pull in the wezterm API
local wezterm = require 'wezterm'
local home = wezterm.home_dir
wezterm.add_to_config_reload_watch_list(home.."/windotfiles/.config/wezterm/winwal.toml");

-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices

config.font = wezterm.font('JetBrainsMono Nerd Font')
config.font_size = 13

config.automatically_reload_config = true
config.hide_tab_bar_if_only_one_tab = true

-- prettier tabs, colored from the live winwal palette (updated by `update-winwal`)
config.use_fancy_tab_bar = true
config.tab_bar_at_bottom = false
config.tab_max_width = 32

-- ponytail: hand-parse the fixed-format winwal.toml instead of wezterm.serde,
-- which this wezterm build predates. Handles scalar and array color lines.
local function winwal_colors()
  local f = io.open(home .. '/windotfiles/.config/wezterm/winwal.toml', 'r')
  if not f then return nil end
  local c = {}
  for line in f:lines() do
    local key, val = line:match('^%s*([%w_]+)%s*=%s*(.+)$')
    if key then
      local hexes = {}
      for h in val:gmatch('#%x+') do hexes[#hexes + 1] = h end
      if #hexes == 1 then c[key] = hexes[1]
      elseif #hexes > 1 then c[key] = hexes end
    end
  end
  f:close()
  return c.background and c or nil
end

local w = winwal_colors()
if w then
  local accent = w.ansi[4]     -- palette's orange/primary accent
  local hover  = w.brights[4]  -- brighter accent for hover
  config.colors = {
    foreground = w.foreground,
    background = w.background,
    cursor_bg = w.cursor_bg,
    cursor_border = w.cursor_border,
    cursor_fg = w.cursor_fg,
    selection_bg = w.selection_bg,
    selection_fg = w.selection_fg,
    ansi = w.ansi,
    brights = w.brights,
    tab_bar = {
      background = w.background,
      active_tab   = { bg_color = accent, fg_color = w.background, intensity = 'Bold' },
      inactive_tab = { bg_color = tostring(wezterm.color.parse(w.background):lighten(0.08)), fg_color = w.foreground },
      inactive_tab_hover = { bg_color = hover, fg_color = w.background },
      new_tab       = { bg_color = w.background, fg_color = accent },
      new_tab_hover = { bg_color = hover, fg_color = w.background },
    },
  }
  config.window_frame = {
    font = wezterm.font { family = 'JetBrainsMono Nerd Font', weight = 'Bold' },
    font_size = 12,
    active_titlebar_bg = w.background,
    inactive_titlebar_bg = w.background,
  }
end

config.color_scheme = 'winwal'
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

-- tmux-style leader: press Ctrl+a, release, then the command key
config.leader = { key = 'a', mods = 'CTRL', timeout_milliseconds = 1000 }

-- Ctrl+<n>: go to tab n, or create a new tab if it doesn't exist yet.
-- ponytail: spawns ONE tab when the index is missing (appends at end), so
-- jumping to 5 from 1 tab makes tab 2, not tabs 2-5. Fine for sequential use.
local function goto_or_create_tab(index)
  return wezterm.action_callback(function(win, pane)
    if win:mux_window():tabs()[index + 1] then
      win:perform_action(wezterm.action.ActivateTab(index), pane)
    else
      win:perform_action(wezterm.action.SpawnTab 'CurrentPaneDomain', pane)
    end
  end)
end

config.keys = {
  {
    key = 'v',
    mods = 'CTRL',
    action = wezterm.action.PasteFrom 'Clipboard',
  },

  -- close current tab
  { key = 'w', mods = 'CTRL', action = wezterm.action.CloseCurrentTab { confirm = true } },

  -- move between tabs, vim-style
  { key = 'h', mods = 'CTRL', action = wezterm.action.ActivateTabRelative(-1) },
  { key = 'l', mods = 'CTRL', action = wezterm.action.ActivateTabRelative(1) },

  -- Ctrl+<n>: switch to tab n, creating it if needed
  { key = '1', mods = 'CTRL', action = goto_or_create_tab(0) },
  { key = '2', mods = 'CTRL', action = goto_or_create_tab(1) },
  { key = '3', mods = 'CTRL', action = goto_or_create_tab(2) },
  { key = '4', mods = 'CTRL', action = goto_or_create_tab(3) },
  { key = '5', mods = 'CTRL', action = goto_or_create_tab(4) },
  { key = '6', mods = 'CTRL', action = goto_or_create_tab(5) },
  { key = '7', mods = 'CTRL', action = goto_or_create_tab(6) },
  { key = '8', mods = 'CTRL', action = goto_or_create_tab(7) },
  { key = '9', mods = 'CTRL', action = goto_or_create_tab(8) },
}

-- and finally, return the configuration to wezterm
return config