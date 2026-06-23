return {
  {
    'williamboman/mason.nvim',
    build = ':MasonUpdate',
    opts = {},
  },
  {
    'williamboman/mason-lspconfig.nvim',
    dependencies = { 'williamboman/mason.nvim', 'neovim/nvim-lspconfig' },
    opts = {
      ensure_installed = {
        'pyright', 'html', 'cssls', 'ts_ls', 'jsonls', 'lua_ls', 'emmet_language_server',
      },
    },
  },
  {
    'neovim/nvim-lspconfig',
    dependencies = { 'hrsh7th/cmp-nvim-lsp' },
    config = function()
      local lspconfig = require('lspconfig')
      local capabilities = require('cmp_nvim_lsp').default_capabilities()

      local on_attach = function(_, bufnr)
        local map = function(mode, lhs, rhs, desc)
          vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = desc })
        end
        map('n', 'gd', vim.lsp.buf.definition, 'Go to definition')
        map('n', 'gD', vim.lsp.buf.declaration, 'Go to declaration')
        map('n', 'gi', vim.lsp.buf.implementation, 'Go to implementation')
        map('n', 'gr', vim.lsp.buf.references, 'References')
        map('n', 'K', vim.lsp.buf.hover, 'Hover documentation')
        map('n', '<leader>rn', vim.lsp.buf.rename, 'Rename')
        map({ 'n', 'v' }, '<leader>ca', vim.lsp.buf.code_action, 'Code action')
        map('n', '<leader>f', function() require('conform').format({ async = true, lsp_fallback = true }) end, 'Format')
      end

      -- Python: Pyright for type/navigation/completion; Ruff for lint/imports/format actions.
      lspconfig.pyright.setup({
        capabilities = capabilities,
        on_attach = on_attach,
        settings = {
          python = {
            analysis = {
              typeCheckingMode = 'basic',
              autoSearchPaths = true,
              useLibraryCodeForTypes = true,
              diagnosticMode = 'workspace',
            },
          },
        },
      })

      lspconfig.ruff.setup({
        capabilities = capabilities,
        on_attach = function(client, bufnr)
          -- Let Pyright handle hover so NLP package docs/types are better surfaced.
          client.server_capabilities.hoverProvider = false
          on_attach(client, bufnr)
        end,
      })

      for _, server in ipairs({ 'html', 'cssls', 'ts_ls', 'jsonls', 'emmet_language_server' }) do
        lspconfig[server].setup({ capabilities = capabilities, on_attach = on_attach })
      end

      lspconfig.lua_ls.setup({
        capabilities = capabilities,
        on_attach = on_attach,
        settings = { Lua = { diagnostics = { globals = { 'vim' } } } },
      })
    end,
  },
}
