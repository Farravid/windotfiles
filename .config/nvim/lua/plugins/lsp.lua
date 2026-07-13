return {
  {
    "mason-org/mason.nvim",
    opts = {},
  },
  {
    "mason-org/mason-lspconfig.nvim",
    dependencies = {
      "mason-org/mason.nvim",
      "neovim/nvim-lspconfig",
    },
    opts = {
      -- languages actually used in this repo: lua (wezterm/glazewm/nvim
      -- config), python (scripts/), json/toml (configs), markdown (docs)
      ensure_installed = { "lua_ls", "pyright", "jsonls", "taplo", "marksman" },
    },
  },
  {
    -- provides the lsp/<server>.lua configs on the runtimepath that
    -- vim.lsp.config/vim.lsp.enable pick up (nvim 0.11+ API; the old
    -- require("lspconfig")[server].setup{} form is deprecated)
    "neovim/nvim-lspconfig",
    dependencies = { "saghen/blink.cmp" },
    config = function()
      vim.lsp.config("*", {
        capabilities = require("blink.cmp").get_lsp_capabilities(),
      })
      vim.lsp.enable({ "lua_ls", "pyright", "jsonls", "taplo", "marksman" })

      vim.keymap.set("n", "gd", vim.lsp.buf.definition, { desc = "Goto definition" })
      vim.keymap.set("n", "K", vim.lsp.buf.hover, { desc = "Hover docs" })
      vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, { desc = "Rename symbol" })
      vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, { desc = "Code action" })
      vim.keymap.set("n", "[d", vim.diagnostic.goto_prev, { desc = "Previous diagnostic" })
      vim.keymap.set("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })
    end,
  },
  {
    -- prebuilt Rust binary, no C toolchain needed on Windows
    "saghen/blink.cmp",
    version = "*",
    opts = {
      keymap = { preset = "default" },
      appearance = { nerd_font_variant = "mono" },
      sources = { default = { "lsp", "path", "buffer" } },
    },
  },
}
