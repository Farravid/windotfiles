return {
  "goolord/alpha-nvim",
  -- eager, not event = "VimEnter": lazy.nvim's own VimEnter listener can
  -- lose the race against Neovim's real (one-time) VimEnter, silently
  -- never loading the plugin. Loading eagerly lets alpha register its
  -- own internal VimEnter autocmd early enough to reliably catch it.
  lazy = false,
  dependencies = { "nvim-tree/nvim-web-devicons" },
  config = function()
    local alpha = require("alpha")
    local dashboard = require("alpha.themes.dashboard")

    dashboard.section.header.val = {
      "                                                     ",
      "  ██╗    ██╗██╗███╗   ██╗██████╗  ██████╗ ████████╗ ",
      "  ██║    ██║██║████╗  ██║██╔══██╗██╔═══██╗╚══██╔══╝ ",
      "  ██║ █╗ ██║██║██╔██╗ ██║██║  ██║██║   ██║   ██║    ",
      "  ██║███╗██║██║██║╚██╗██║██║  ██║██║   ██║   ██║    ",
      "  ╚███╔███╔╝██║██║ ╚████║██████╔╝╚██████╔╝   ██║    ",
      "   ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝    ╚═╝    ",
      "                                                     ",
      "              opencode · hermes · nvim               ",
      "                                                     ",
    }

    dashboard.section.buttons.val = {
      dashboard.button("f", "  Find file", "<cmd>lua require('fzf-lua').files()<cr>"),
      dashboard.button("g", "  Live grep", "<cmd>lua require('fzf-lua').live_grep()<cr>"),
      dashboard.button("r", "  Recent files", "<cmd>lua require('fzf-lua').oldfiles()<cr>"),
      dashboard.button("e", "  File tree", "<cmd>Neotree toggle reveal<cr>"),
      dashboard.button("o", "  opencode", "<cmd>lua WindotfilesAgents.open_opencode()<cr>"),
      dashboard.button("h", "  hermes", "<cmd>lua WindotfilesAgents.open_hermes()<cr>"),
      dashboard.button("q", "  Quit", "<cmd>qa<cr>"),
    }

    dashboard.section.header.opts.hl = "AlphaHeader"
    dashboard.section.buttons.opts.hl = "AlphaButtons"
    dashboard.section.footer.opts.hl = "AlphaFooter"

    local stats = require("lazy").stats()
    dashboard.section.footer.val = "⚡ " .. stats.count .. " plugins loaded in " .. math.floor(stats.startuptime) .. "ms"

    alpha.setup(dashboard.opts)

    -- :Alpha alone only swaps the dashboard into the current window,
    -- leaving other splits/buffers as-is; :only first gives a genuinely
    -- clean single-pane screen
    vim.keymap.set("n", "<leader>d", "<cmd>only<bar>Alpha<cr>", { desc = "Show dashboard" })
  end,
}
