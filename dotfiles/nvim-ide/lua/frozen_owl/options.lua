local opt = vim.opt

opt.number = true
opt.relativenumber = true
opt.mouse = 'a'
opt.clipboard = 'unnamedplus'
opt.breakindent = true
opt.undofile = true
opt.ignorecase = true
opt.smartcase = true
opt.signcolumn = 'yes'
opt.updatetime = 250
opt.timeoutlen = 400
opt.splitright = true
opt.splitbelow = true
opt.termguicolors = true
opt.cursorline = true
opt.scrolloff = 8
opt.sidescrolloff = 8
opt.expandtab = true
opt.shiftwidth = 4
opt.tabstop = 4
opt.softtabstop = 4
opt.wrap = false
opt.completeopt = { 'menu', 'menuone', 'noselect' }
opt.inccommand = 'split'

vim.diagnostic.config({
  virtual_text = { spacing = 2, source = 'if_many' },
  severity_sort = true,
  float = { border = 'rounded', source = true },
})
