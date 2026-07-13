vim.g.mapleader = " "
vim.g.maplocalleader = " "

local opt = vim.opt

opt.number = true
opt.relativenumber = true
opt.signcolumn = "yes"
opt.cursorline = true

opt.tabstop = 2
opt.shiftwidth = 2
opt.expandtab = true
opt.smartindent = true

opt.ignorecase = true
opt.smartcase = true

opt.splitright = true
opt.splitbelow = true

opt.termguicolors = true
opt.scrolloff = 8
opt.updatetime = 250

opt.clipboard = "unnamedplus"
opt.undofile = true
opt.swapfile = false

-- leader is space, which also moves the cursor right in normal mode --
-- a short timeoutlen means only a fast, deliberate chord (space+letter
-- typed quickly) registers as a leader sequence; a space tapped during
-- normal navigation, followed by an unrelated keystroke a beat later,
-- just does two separate things instead of misfiring as <leader>x
opt.timeoutlen = 300

opt.wrap = false
