vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.smartindent = true
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.termguicolors = true
vim.opt.splitbelow = true
vim.opt.splitright = true
vim.opt.clipboard = "unnamedplus"
vim.opt.cursorline = true
vim.opt.signcolumn = "yes"
vim.opt.colorcolumn = "80,100,120"

-- Bootstrap lazy.nvim plugin manager
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  -- Essentials
  { "nvim-lua/plenary.nvim" },
  { "nvim-telescope/telescope.nvim", dependencies = { "nvim-lua/plenary.nvim" } },
  { "nvim-lualine/lualine.nvim" },
  { "nvim-tree/nvim-tree.lua" },
  { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },

  -- LSP + Completion
  { "neovim/nvim-lspconfig" },
  { "williamboman/mason.nvim" },
  { "williamboman/mason-lspconfig.nvim" },
  { "hrsh7th/nvim-cmp" },
  { "hrsh7th/cmp-nvim-lsp" },
  { "hrsh7th/cmp-buffer" },
  { "L3MON4D3/LuaSnip" },
  { "saadparwaiz1/cmp_luasnip" },

  -- Language-specific
  { "Vimjas/vim-python-pep8-indent" },
  { "psf/black", branch = "stable" },

  -- Git
  { "lewis6991/gitsigns.nvim" },

  -- Theme
  { "gruvbox-community/gruvbox" },
  {"lmintmate/blue-mood-vim"},
})

-- Theme
vim.cmd("colorscheme gruvbox")

-- Treesitter setup
require("nvim-treesitter.configs").setup({
  ensure_installed = { "python", "go", "lua", "json", "yaml" },
  highlight = { enable = true },
  indent = { enable = true },
})

-- Lualine setup
require("lualine").setup({ options = { theme = "gruvbox" } })

-- Nvim-tree setup
require("nvim-tree").setup()

-- Gitsigns setup
require("gitsigns").setup()

-- Mason setup
require("mason").setup()
require("mason-lspconfig").setup({
  ensure_installed = { "pyright",},
 })
vim.lsp.config('*', {ensure_installed = { "pyright",}})

-- LSP setup
-- local lspconfig = require("lspconfig")
-- lspconfig.pyright.setup({})
-- lspconfig.gopls.setup({})

-- Autocomplete setup
local cmp = require("cmp")
cmp.setup({
  snippet = {
    expand = function(args) require("luasnip").lsp_expand(args.body) end,
  },
  mapping = cmp.mapping.preset.insert({
    ["<C-Space>"] = cmp.mapping.complete(),
    ["<CR>"] = cmp.mapping.confirm({ select = true }),
  }),
  sources = {
    { name = "nvim_lsp" },
    { name = "buffer" },
  },
})

-- Keymaps
vim.keymap.set("n", "<leader>ff", "<cmd>Telescope find_files<cr>", { desc = "Find files" })
vim.keymap.set("n", "<leader>fg", "<cmd>Telescope live_grep<cr>", { desc = "Live grep" })
vim.keymap.set("n", "<leader>fb", "<cmd>Telescope buffers<cr>", { desc = "Find buffers" })
vim.keymap.set("n", "<leader>e", "<cmd>NvimTreeToggle<cr>", { desc = "File explorer" })

for i = 1, 9 do
  vim.keymap.set("n", "<leader>" .. i, i .. "gt", { noremap = true, silent = true })
end

-- Autoformat on save (Python, Go)
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.py",
  command = "silent! execute ':Black'",
})

