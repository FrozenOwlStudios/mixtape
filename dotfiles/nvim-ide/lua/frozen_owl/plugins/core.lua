return {
	{ "folke/which-key.nvim", event = "VeryLazy", opts = {} },
	{ "nvim-lua/plenary.nvim" },
	--[[
  --Colorscheme, I will probably delete this later on
  { 'folke/tokyonight.nvim', priority = 1000, config = function()
      vim.cmd.colorscheme('tokyonight-night')
    end
  },
  ]]
	{ "nvim-tree/nvim-web-devicons" },
	{
		"nvim-neo-tree/neo-tree.nvim",
		branch = "v3.x",
		dependencies = { "nvim-lua/plenary.nvim", "nvim-tree/nvim-web-devicons", "MunifTanjim/nui.nvim" },
		opts = { filesystem = { filtered_items = { visible = true, hide_dotfiles = false } } },
	},
	{
		"nvim-telescope/telescope.nvim",
		branch = "0.1.x",
		dependencies = { "nvim-lua/plenary.nvim" },
		opts = { defaults = { file_ignore_patterns = { ".venv/", "node_modules/", ".git/" } } },
	},
	{ "akinsho/toggleterm.nvim", version = "*", opts = { open_mapping = [[<c-\>]], direction = "float" } },
	{ "kdheepak/lazygit.nvim", cmd = "LazyGit", dependencies = { "nvim-lua/plenary.nvim" } },
	{ "folke/trouble.nvim", opts = {} },
}
