-- opencode / hermes, kept alive in floating terminals and toggled independently.
-- See AGENTS.md / windotfiles plan: nvim's job here is launching + feeding
-- context to these CLIs, not reimplementing their agent behavior.

return {
  "akinsho/toggleterm.nvim",
  version = "*",
  opts = {
    size = 20,
    open_mapping = false,
    direction = "float",
    float_opts = { border = "curved" },
    start_in_insert = true,
    persist_size = true,
  },
  config = function(_, opts)
    require("toggleterm").setup(opts)

    local Terminal = require("toggleterm.terminal").Terminal

    local opencode = Terminal:new({ cmd = "opencode", direction = "float", hidden = true })
    local hermes = Terminal:new({ cmd = "hermes chat", direction = "float", hidden = true })
    -- run through nu (not the bare `claude` binary) so the
    -- claude-personal function in config.nu sets CLAUDE_CONFIG_DIR first;
    -- `-l` (login) is required for `-c` to source config.nu at all --
    -- `-i -c` runs the command without ever loading it, so the def is
    -- missing and nu errors with "not found"
    local claude = Terminal:new({ cmd = "nu -l -c claude-personal", direction = "float", hidden = true })
    -- plain nu shell for ad-hoc commands (git, tests, ls, ...) without
    -- leaving nvim; kept separate from last_agent since sending code
    -- selections to a bare shell doesn't make sense the same way
    local shell = Terminal:new({ cmd = "nu", direction = "float", hidden = true })

    local last_agent = opencode

    local function toggle(term)
      last_agent = term
      term:toggle()
    end

    -- send the current visual selection, or the current buffer's relative
    -- path if nothing is selected, to whichever agent terminal was last toggled
    local function send_context()
      local mode = vim.fn.mode()
      local text

      if mode == "v" or mode == "V" or mode == "\22" then
        vim.cmd('normal! "vy')
        text = vim.fn.getreg("v")
      else
        text = vim.fn.expand("%:.")
      end

      if not text or text == "" then
        vim.notify("Nothing to send to the agent", vim.log.levels.WARN)
        return
      end

      last_agent:open()
      last_agent:send(text, false)
    end

    -- leader-prefixed maps are normal-mode only: leader is space, and a
    -- terminal-mode mapping would intercept that keystroke before it
    -- reaches opencode/hermes -- every "space+t" you type while chatting
    -- (the, to, test, ...) would silently toggle a terminal instead of
    -- being sent as text. Use <C-\><C-n> to leave terminal-insert mode
    -- first, then these work normally.
    local map = vim.keymap.set
    map("n", "<leader>ao", function() toggle(opencode) end, { desc = "Toggle opencode" })
    map("n", "<leader>ah", function() toggle(hermes) end, { desc = "Toggle hermes" })
    map("n", "<leader>ac", function() toggle(claude) end, { desc = "Toggle claude code" })
    map({ "n", "v" }, "<leader>as", send_context, { desc = "Send selection/path to last agent" })
    map("n", "<leader>t", function() shell:toggle() end, { desc = "Toggle shell (nu)" })

    -- one-key close for whatever floating terminal currently has focus.
    -- <C-q> is a chord essentially never needed by interactive CLI
    -- programs (and not claimed by WezTerm or the shell here), so it's
    -- safe to claim, unlike plain <Esc> which opencode/hermes need for
    -- their own menus/prompts.
    map("t", "<C-q>", [[<C-\><C-n><cmd>close<cr>]], { desc = "Close floating terminal" })

    -- exposed so other plugins (e.g. the dashboard) can trigger the same
    -- toggle without re-simulating keypresses
    _G.WindotfilesAgents = {
      open_opencode = function() toggle(opencode) end,
      open_hermes = function() toggle(hermes) end,
      open_claude = function() toggle(claude) end,
    }
  end,
}
