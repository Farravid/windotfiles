return {
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = {
      spec = {
        { "<leader>a", group = "agents (opencode/hermes)" },
        { "<leader>f", group = "find" },
        { "<leader>h", group = "git hunks" },
        { "<leader>s", group = "split" },
      },
    },
  },
  { "nvim-lua/plenary.nvim", lazy = true },
  { "windwp/nvim-autopairs", event = "InsertEnter", opts = {} },
  { "numToStr/Comment.nvim", event = "VeryLazy", opts = {} },
}
