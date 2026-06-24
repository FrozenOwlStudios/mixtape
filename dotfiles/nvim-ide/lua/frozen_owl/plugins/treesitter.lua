return {
  {
    'nvim-treesitter/nvim-treesitter',
    build = ':TSUpdate',
    opts = {
      ensure_installed = {
        'python', 'lua', 'vim', 'vimdoc', 'bash',
        'html', 'css', 'javascript', 'typescript', 'json', 'yaml',
        'toml', 'markdown', 'markdown_inline', 'regex', 'sql',
      },
      highlight = { enable = true },
      indent = { enable = true },
    },
    config = function(_, opts)
      require('nvim-treesitter.config').setup(opts)
    end,
  },
  { 'windwp/nvim-ts-autotag', ft = { 'html', 'javascript', 'typescript', 'jsx', 'tsx' }, opts = {} },
}
