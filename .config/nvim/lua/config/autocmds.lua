-- highlight yanked text briefly
vim.api.nvim_create_autocmd("TextYankPost", {
  desc = "Highlight yanked text",
  callback = function()
    vim.highlight.on_yank()
  end,
})

-- restore cursor position when reopening a file
vim.api.nvim_create_autocmd("BufReadPost", {
  desc = "Restore last cursor position",
  callback = function(args)
    local mark = vim.api.nvim_buf_get_mark(args.buf, '"')
    local line_count = vim.api.nvim_buf_line_count(args.buf)
    if mark[1] > 0 and mark[1] <= line_count then
      vim.api.nvim_win_set_cursor(0, mark)
    end
  end,
})

-- don't leave a bunch of terminals in insert-mode-exited state
vim.api.nvim_create_autocmd("TermOpen", {
  desc = "Open terminals in insert mode, no line numbers",
  callback = function()
    vim.opt_local.number = false
    vim.opt_local.relativenumber = false
    vim.cmd("startinsert")
  end,
})
