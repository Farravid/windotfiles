local langs = { "lua", "python", "json", "toml", "markdown", "markdown_inline", "bash", "yaml", "vim", "vimdoc" }

return {
  -- "master" was archived upstream; "main" is the actively maintained
  -- branch with a new API (install()/setup() split, no more
  -- nvim-treesitter.configs) and fixes for current Neovim (the old
  -- master pin here crashed on Neovim 0.12's conceal_line decoration
  -- provider).
  "nvim-treesitter/nvim-treesitter",
  branch = "main",
  build = ":TSUpdate",
  lazy = false,
  config = function()
    require("nvim-treesitter").install(langs)

    vim.api.nvim_create_autocmd("FileType", {
      pattern = langs,
      callback = function()
        vim.treesitter.start()
        vim.bo.indentexpr = "v:lua.require'nvim-treesitter'.indentexpr()"
      end,
    })
  end,
}
