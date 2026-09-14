-- Requires Neovim >= 0.10, git, ripgrep, fd, node/npm, uv, ruff, mypy

vim.g.mapleader = " "
vim.g.maplocalleader = " "

require("frozen_owl.options")
require("frozen_owl.keymaps")
require("frozen_owl.lazy")
