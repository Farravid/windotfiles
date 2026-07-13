return {
  {
    -- reads ~/.cache/wal/colors directly, so it stays in sync with the
    -- winwal pipeline driving WezTerm/Zebar without touching the Python side
    "AlphaTechnolog/pywal.nvim",
    priority = 1000,
    config = function()
      require("pywal").setup()
      local ok = pcall(vim.cmd.colorscheme, "pywal")
      if not ok then
        vim.cmd.colorscheme("habamax") -- fallback if wal cache doesn't exist yet
      end
    end,
  },
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {},
  },
  {
    "lewis6991/gitsigns.nvim",
    opts = {
      on_attach = function(bufnr)
        local gs = require("gitsigns")
        local map = vim.keymap.set

        map("n", "]c", function() gs.nav_hunk("next") end, { buffer = bufnr, desc = "Next git hunk" })
        map("n", "[c", function() gs.nav_hunk("prev") end, { buffer = bufnr, desc = "Previous git hunk" })
        map("n", "<leader>hs", gs.stage_hunk, { buffer = bufnr, desc = "Stage hunk" })
        map("n", "<leader>hr", gs.reset_hunk, { buffer = bufnr, desc = "Reset hunk" })
        map("n", "<leader>hp", gs.preview_hunk, { buffer = bufnr, desc = "Preview hunk" })
        map("n", "<leader>hb", function() gs.blame_line({ full = true }) end, { buffer = bufnr, desc = "Blame line" })
      end,
    },
  },
}
