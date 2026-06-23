return {
  {
    'stevearc/conform.nvim',
    event = { 'BufWritePre' },
    cmd = { 'ConformInfo' },
    opts = {
      format_on_save = function(bufnr)
        local ft = vim.bo[bufnr].filetype
        if ft == 'python' then
          return { timeout_ms = 3000, lsp_fallback = true }
        end
        return { timeout_ms = 2000, lsp_fallback = true }
      end,
      formatters_by_ft = {
        python = { 'ruff_format', 'ruff_organize_imports' },
        javascript = { 'prettier' },
        typescript = { 'prettier' },
        html = { 'prettier' },
        css = { 'prettier' },
        json = { 'prettier' },
        markdown = { 'prettier' },
        lua = { 'stylua' },
      },
    },
  },
  {
    'mfussenegger/nvim-lint',
    event = { 'BufReadPost', 'BufWritePost', 'InsertLeave' },
    config = function()
      local lint = require('lint')
      lint.linters_by_ft = { python = { 'mypy' } }
      vim.api.nvim_create_autocmd({ 'BufWritePost', 'BufReadPost', 'InsertLeave' }, {
        callback = function()
          require('lint').try_lint()
        end,
      })
    end,
  },
}
