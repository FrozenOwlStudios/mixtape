-- ============================================================
-- Simple Neovim config
-- Author: FrozenOwl
-- ============================================================

-- Leader key
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Basic options
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.mouse = "a"
vim.opt.termguicolors = true
vim.opt.updatetime = 200
vim.opt.signcolumn = "yes"
vim.opt.wrap = false

-- Indentation (good defaults for Python)
vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.smartindent = true

-- Search
vim.opt.ignorecase = true
vim.opt.smartcase = true

-- Clipboard
vim.opt.clipboard = "unnamedplus"

-- Better splits
vim.opt.splitright = true
vim.opt.splitbelow = true

-- Setting colorscheme
vim.cmd("colorscheme slate")

-- ============================================================
-- Keymaps (multi-file workflow)
-- ============================================================
local map = vim.keymap.set
local opts = { noremap = true, silent = true }

-- Save/quit
map("n", "<leader>w", "<cmd>w<cr>", opts)
map("n", "<leader>q", "<cmd>q<cr>", opts)

-- Buffer navigation (like "tabs" for files)
map("n", "<S-l>", "<cmd>bnext<cr>", opts)     -- Next buffer
map("n", "<S-h>", "<cmd>bprevious<cr>", opts) -- Previous buffer
map("n", "<leader>bd", "<cmd>bdelete<cr>", opts) -- Close buffer

-- Optional: show buffers list
map("n", "<leader>bl", "<cmd>ls<cr>", opts)

-- ============================================================
-- Bootstrap lazy.nvim (plugin manager)
-- ============================================================
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath
  })
end
vim.opt.rtp:prepend(lazypath)

-- ============================================================
-- Plugins
-- ============================================================
require("lazy").setup({
  -- File picker / search
  {
    "nvim-telescope/telescope.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
  },

  -- Nice "tabs" (buffer line)
  {
    "akinsho/bufferline.nvim",
    version = "*",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("bufferline").setup({
        options = {
          diagnostics = "nvim_lsp",
          separator_style = "slant",
          show_buffer_close_icons = false,
          show_close_icon = false,
        }
      })
    end
  },

  -- LSP
  { "neovim/nvim-lspconfig" },

  -- Completion engine (manual trigger only)
  { "hrsh7th/nvim-cmp" },
  { "hrsh7th/cmp-nvim-lsp" },
  { "L3MON4D3/LuaSnip" }, -- optional snippets, kept minimal

  -- Treesitter (better highlighting)
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
  },

  -- Formatting (optional but useful)
  { "stevearc/conform.nvim" },

  -- Terminal support
  {
    "akinsho/toggleterm.nvim",
    version = "*",
    keys = {
      { "<leader>tt", "<cmd>ToggleTerm direction=float<cr>", desc = "Toggle floating terminal" },
    },
    opts = {
      open_mapping = nil,      -- we bind ourselves (Normal mode)
      direction = "float",
      shade_terminals = false, -- keep minimal
      float_opts = {
        border = "rounded",
      },
    },
  },
})

-- ============================================================
-- Telescope keymaps
-- ============================================================
local telescope = require("telescope.builtin")
map("n", "<leader>ff", telescope.find_files, opts) -- Find files
map("n", "<leader>fg", telescope.live_grep, opts)  -- Grep in project
map("n", "<leader>fb", telescope.buffers, opts)    -- Switch open files
map("n", "<leader>fh", telescope.help_tags, opts)


-- ============================================================
-- LSP: Pyright
-- ============================================================

-- LSP keymaps (all manual)
map("n", "gd", vim.lsp.buf.definition, opts)
map("n", "gr", vim.lsp.buf.references, opts)
map("n", "K", vim.lsp.buf.hover, opts)             -- hover docs (manual)
map("n", "<leader>rn", vim.lsp.buf.rename, opts)
map("n", "<leader>ca", vim.lsp.buf.code_action, opts)
map("n", "<leader>e", vim.diagnostic.open_float, opts)
map("n", "[d", vim.diagnostic.goto_prev, opts)
map("n", "]d", vim.diagnostic.goto_next, opts)

-- ============================================================
-- nvim-cmp (manual completion ONLY)
-- ============================================================
local cmp = require("cmp")

cmp.setup({
  completion = {
    autocomplete = false, -- no automatic popup
  },
  snippet = {
    expand = function(args)
      require("luasnip").lsp_expand(args.body)
    end,
  },
  mapping = {
    -- Manual trigger
    ["<C-Space>"] = cmp.mapping.complete(),

    -- Confirm ONLY if menu is visible
    ["<CR>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.confirm({ select = false })
      else
        fallback() -- normal Enter behavior
      end
    end, { "i", "s" }),

    -- Navigation only when menu is open
    ["<C-n>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_next_item()
      else
        fallback()
      end
    end, { "i", "s" }),

    ["<C-p>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_prev_item()
      else
        fallback()
      end
    end, { "i", "s" }),

    -- Close menu explicitly
    ["<Esc>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.abort()
      else
        fallback()
      end
    end, { "i", "s" }),
  },
  sources = {
    { name = "nvim_lsp" },
  },
})

-- ============================================================
-- Formatting with conform.nvim (manual trigger)
-- ============================================================
require("conform").setup({
  formatters_by_ft = {
    python = { "black" },
  },
})

map("n", "<leader>f", function()
  require("conform").format({ lsp_fallback = true })
end, opts)

-- ============================================================
-- Bufferline keymaps (more intuitive "tabs")
-- ============================================================
map("n", "<leader>1", "<cmd>BufferLineGoToBuffer 1<cr>", opts)
map("n", "<leader>2", "<cmd>BufferLineGoToBuffer 2<cr>", opts)
map("n", "<leader>3", "<cmd>BufferLineGoToBuffer 3<cr>", opts)
map("n", "<leader>4", "<cmd>BufferLineGoToBuffer 4<cr>", opts)
map("n", "<leader>5", "<cmd>BufferLineGoToBuffer 5<cr>", opts)


-- ============================================================
-- Extra config for terminal
-- ============================================================
vim.api.nvim_create_autocmd("TermOpen", {
  pattern = "term://*",
  callback = function()
    vim.cmd("startinsert")
    vim.keymap.set("t", "<Esc>", [[<C-\><C-n>]], { buffer = true })
  end,
})
