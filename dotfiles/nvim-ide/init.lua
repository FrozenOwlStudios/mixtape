-- ~/.config/nvim/init.lua
-- Full IDE-style Neovim setup for Python, C, Perl, and full-stack web development.
-- Plugin manager: lazy.nvim

------------------------------------------------------------
-- What must be installed
--
-- sudo apt install git ripgrep fd-find build-essential clangd clang-format nodejs npm python3-pip python3-pynvim python3-debugpy
-- sudo npm install -g prettier eslint_d typescript typescript-language-server
-- curl -LsSf https://astral.sh/uv/install.sh | sh
-- uv tool install ruff@latest
-- uvx ty check
------------------------------------------------------------

------------------------------------------------------------
-- Basic options
------------------------------------------------------------
vim.g.mapleader = " "
vim.g.maplocalleader = " "

local opt = vim.opt
opt.number = true
opt.relativenumber = true
opt.mouse = "a"
opt.clipboard = "unnamedplus"
opt.expandtab = true
opt.shiftwidth = 4
opt.tabstop = 4
opt.smartindent = true
opt.wrap = false
opt.termguicolors = true
opt.signcolumn = "yes"
opt.updatetime = 250
opt.timeoutlen = 400
opt.splitright = true
opt.splitbelow = true
opt.ignorecase = true
opt.smartcase = true
opt.undofile = true
opt.completeopt = { "menu", "menuone", "noselect" }

-- Web files usually use 2 spaces.
vim.api.nvim_create_autocmd("FileType", {
	pattern = {
		"javascript",
		"typescript",
		"javascriptreact",
		"typescriptreact",
		"json",
		"html",
		"css",
		"scss",
		"yaml",
	},
	callback = function()
		vim.opt_local.shiftwidth = 2
		vim.opt_local.tabstop = 2
	end,
})

------------------------------------------------------------
-- Keymaps
------------------------------------------------------------
local keymap = vim.keymap.set
local opts = { noremap = true, silent = true }

keymap("n", "<leader>w", "<cmd>w<cr>", opts)
keymap("n", "<leader>q", "<cmd>q<cr>", opts)
keymap("n", "<leader>e", "<cmd>NvimTreeToggle<cr>", opts)
keymap("n", "<leader>ff", "<cmd>Telescope find_files<cr>", opts)
keymap("n", "<leader>fg", "<cmd>Telescope live_grep<cr>", opts)
keymap("n", "<leader>fb", "<cmd>Telescope buffers<cr>", opts)
keymap("n", "<leader>fh", "<cmd>Telescope help_tags<cr>", opts)
keymap("n", "<leader>xx", "<cmd>Trouble diagnostics toggle<cr>", opts)
keymap("n", "<leader>tt", "<cmd>ToggleTerm<cr>", opts)
keymap("n", "<leader>gg", "<cmd>LazyGit<cr>", opts)

------------------------------------------------------------
-- Bootstrap lazy.nvim
------------------------------------------------------------
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
	vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"--branch=stable",
		"https://github.com/folke/lazy.nvim.git",
		lazypath,
	})
end
vim.opt.rtp:prepend(lazypath)

------------------------------------------------------------
-- Plugins
------------------------------------------------------------
require("lazy").setup({
	----------------------------------------------------------
	-- UI
	----------------------------------------------------------
	{
		"folke/tokyonight.nvim",
		priority = 1000,
		config = function()
			vim.cmd.colorscheme("tokyonight-night")
		end,
	},
	{ "nvim-lualine/lualine.nvim", dependencies = { "nvim-tree/nvim-web-devicons" }, opts = {} },
	{ "nvim-tree/nvim-tree.lua", dependencies = { "nvim-tree/nvim-web-devicons" }, opts = {} },
	{ "akinsho/bufferline.nvim", dependencies = { "nvim-tree/nvim-web-devicons" }, opts = {} },
	{ "folke/which-key.nvim", opts = {} },
	{ "folke/trouble.nvim", dependencies = { "nvim-tree/nvim-web-devicons" }, opts = {} },
	{ "folke/todo-comments.nvim", dependencies = { "nvim-lua/plenary.nvim" }, opts = {} },
	{ "akinsho/toggleterm.nvim", version = "*", opts = { open_mapping = [[<c-\>]], direction = "float" } },

	----------------------------------------------------------
	-- Search/navigation
	----------------------------------------------------------
	{
		"nvim-telescope/telescope.nvim",
		branch = "0.1.x",
		dependencies = { "nvim-lua/plenary.nvim", "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
		config = function()
			require("telescope").setup({
				defaults = { file_ignore_patterns = { "node_modules", ".git/", "__pycache__", ".venv" } },
			})
			pcall(require("telescope").load_extension, "fzf")
		end,
	},

	----------------------------------------------------------
	-- Git
	----------------------------------------------------------
	{ "lewis6991/gitsigns.nvim", opts = {} },
	{ "kdheepak/lazygit.nvim", dependencies = { "nvim-lua/plenary.nvim" } },

	----------------------------------------------------------
	-- Syntax and code structure
	----------------------------------------------------------
	{
		"nvim-treesitter/nvim-treesitter",
		build = ":TSUpdate",
		config = function()
			require("nvim-treesitter.configs").setup({
				ensure_installed = {
					"python",
					"c",
					"cpp",
					"perl",
					"lua",
					"vim",
					"vimdoc",
					"javascript",
					"typescript",
					"tsx",
					"html",
					"css",
					"scss",
					"json",
					"yaml",
					"markdown",
					"markdown_inline",
					"regex",
					"bash",
					"sql",
				},
				highlight = { enable = true },
				indent = { enable = true },
			})
		end,
	},
	{ "nvim-treesitter/nvim-treesitter-textobjects" },
	{ "windwp/nvim-autopairs", opts = {} },
	{ "numToStr/Comment.nvim", opts = {} },

	----------------------------------------------------------
	-- LSP, completion, snippets
	----------------------------------------------------------
	{ "williamboman/mason.nvim", opts = {} },
	{
		"williamboman/mason-lspconfig.nvim",
		dependencies = { "williamboman/mason.nvim", "neovim/nvim-lspconfig" },
	},
	{
		"WhoIsSethDaniel/mason-tool-installer.nvim",
		dependencies = { "williamboman/mason.nvim" },
	},
	{
		"hrsh7th/nvim-cmp",
		dependencies = {
			"hrsh7th/cmp-nvim-lsp",
			"hrsh7th/cmp-buffer",
			"hrsh7th/cmp-path",
			"hrsh7th/cmp-cmdline",
			"L3MON4D3/LuaSnip",
			"saadparwaiz1/cmp_luasnip",
			"rafamadriz/friendly-snippets",
		},
		config = function()
			local cmp = require("cmp")
			local luasnip = require("luasnip")
			require("luasnip.loaders.from_vscode").lazy_load()

			cmp.setup({
				snippet = {
					expand = function(args)
						luasnip.lsp_expand(args.body)
					end,
				},
				mapping = cmp.mapping.preset.insert({
					["<C-b>"] = cmp.mapping.scroll_docs(-4),
					["<C-f>"] = cmp.mapping.scroll_docs(4),
					["<C-Space>"] = cmp.mapping.complete(),
					["<CR>"] = cmp.mapping.confirm({ select = false }),
					["<Tab>"] = cmp.mapping(function(fallback)
						if cmp.visible() then
							cmp.select_next_item()
						elseif luasnip.expand_or_jumpable() then
							luasnip.expand_or_jump()
						else
							fallback()
						end
					end, { "i", "s" }),
					["<S-Tab>"] = cmp.mapping(function(fallback)
						if cmp.visible() then
							cmp.select_prev_item()
						elseif luasnip.jumpable(-1) then
							luasnip.jump(-1)
						else
							fallback()
						end
					end, { "i", "s" }),
				}),
				sources = cmp.config.sources({
					{ name = "nvim_lsp" },
					{ name = "luasnip" },
					{ name = "path" },
					{ name = "buffer" },
				}),
			})
		end,
	},

	----------------------------------------------------------
	-- Formatting and linting
	----------------------------------------------------------
	{
		"stevearc/conform.nvim",
		opts = {
			format_on_save = { timeout_ms = 2000, lsp_fallback = true },
			formatters_by_ft = {
				python = { "ruff_format", "ruff_organize_imports" },
				c = { "clang_format" },
				cpp = { "clang_format" },
				perl = { "perltidy" },
				javascript = { "prettier" },
				typescript = { "prettier" },
				javascriptreact = { "prettier" },
				typescriptreact = { "prettier" },
				html = { "prettier" },
				css = { "prettier" },
				scss = { "prettier" },
				json = { "prettier" },
				yaml = { "prettier" },
				markdown = { "prettier" },
				lua = { "stylua" },
			},
		},
	},
	{
		"mfussenegger/nvim-lint",
		config = function()
			local lint = require("lint")
			lint.linters_by_ft = {
				python = { "ruff" },
				c = { "clangtidy" },
				cpp = { "clangtidy" },
				perl = { "perlcritic" },
				javascript = { "eslint_d" },
				typescript = { "eslint_d" },
				javascriptreact = { "eslint_d" },
				typescriptreact = { "eslint_d" },
			}
			vim.api.nvim_create_autocmd({ "BufEnter", "BufWritePost", "InsertLeave" }, {
				callback = function()
					require("lint").try_lint()
				end,
			})
		end,
	},

	----------------------------------------------------------
	-- Debugging
	----------------------------------------------------------
	{
		"mfussenegger/nvim-dap",
		dependencies = {
			"rcarriga/nvim-dap-ui",
			"nvim-neotest/nvim-nio",
			"mfussenegger/nvim-dap-python",
		},
		config = function()
			local dap = require("dap")
			local dapui = require("dapui")
			dapui.setup()

			require("dap-python").setup("python")

			dap.adapters.codelldb = {
				type = "server",
				port = "${port}",
				executable = { command = "codelldb", args = { "--port", "${port}" } },
			}
			dap.configurations.c = {
				{
					name = "Launch C executable",
					type = "codelldb",
					request = "launch",
					program = function()
						return vim.fn.input("Path to executable: ", vim.fn.getcwd() .. "/", "file")
					end,
					cwd = "${workspaceFolder}",
					stopOnEntry = false,
				},
			}
			dap.configurations.cpp = dap.configurations.c

			keymap("n", "<F5>", dap.continue, opts)
			keymap("n", "<F10>", dap.step_over, opts)
			keymap("n", "<F11>", dap.step_into, opts)
			keymap("n", "<F12>", dap.step_out, opts)
			keymap("n", "<leader>db", dap.toggle_breakpoint, opts)
			keymap("n", "<leader>du", dapui.toggle, opts)
		end,
	},

	----------------------------------------------------------
	-- Python/NLP workflow helpers
	----------------------------------------------------------
	{
		"kiyoon/jupynium.nvim",
		build = "pip3 install --user .",
		ft = { "python" },
	},
	{
		"quarto-dev/quarto-nvim",
		ft = { "quarto", "markdown" },
		dependencies = { "jmbuhr/otter.nvim", "nvim-treesitter/nvim-treesitter" },
		opts = {},
	},
	{ "Vigemus/iron.nvim", opts = { config = { repl_definition = { python = { command = { "python" } } } } } },
})

------------------------------------------------------------
-- LSP setup
------------------------------------------------------------
local capabilities = require("cmp_nvim_lsp").default_capabilities()
local lspconfig = require("lspconfig")

require("mason-lspconfig").setup({
	ensure_installed = {
		"pyright",
		--		"ruff",
		"clangd",
		"perlnavigator",
		"ts_ls",
		"html",
		"cssls",
		"jsonls",
		"yamlls",
		"lua_ls",
		"bashls",
	},
})

require("mason-tool-installer").setup({
	ensure_installed = {
		--		"black",
		--		"ruff",
		--		"debugpy",
		-- "clang-format",
		"clangd",
		"codelldb",
		"prettier",
		"eslint_d",
		"stylua",
	},
})

local on_attach = function(_, bufnr)
	local bopts = { noremap = true, silent = true, buffer = bufnr }
	keymap("n", "gd", vim.lsp.buf.definition, bopts)
	keymap("n", "gD", vim.lsp.buf.declaration, bopts)
	keymap("n", "gi", vim.lsp.buf.implementation, bopts)
	keymap("n", "gr", vim.lsp.buf.references, bopts)
	keymap("n", "K", vim.lsp.buf.hover, bopts)
	keymap("n", "<leader>rn", vim.lsp.buf.rename, bopts)
	keymap("n", "<leader>ca", vim.lsp.buf.code_action, bopts)
	keymap("n", "<leader>f", function()
		require("conform").format({ async = true, lsp_fallback = true })
	end, bopts)
end

local servers = {
	pyright = {},
	ruff = {},
	clangd = {},
	perlnavigator = {},
	ts_ls = {},
	html = {},
	cssls = {},
	jsonls = {},
	yamlls = {},
	bashls = {},
	lua_ls = {
		settings = {
			Lua = {
				diagnostics = { globals = { "vim" } },
				workspace = { checkThirdParty = false },
			},
		},
	},
}

for server, config in pairs(servers) do
	config.capabilities = capabilities
	config.on_attach = on_attach
	lspconfig[server].setup(config)
end

------------------------------------------------------------
-- Diagnostics display
------------------------------------------------------------
vim.diagnostic.config({
	virtual_text = true,
	signs = true,
	underline = true,
	update_in_insert = false,
	severity_sort = true,
})

------------------------------------------------------------
-- Project-local Python virtualenv detection
------------------------------------------------------------
vim.api.nvim_create_autocmd("VimEnter", {
	callback = function()
		local venv = vim.fn.getcwd() .. "/.venv/bin/python"
		if vim.fn.executable(venv) == 1 then
			vim.g.python3_host_prog = venv
		end
	end,
})
