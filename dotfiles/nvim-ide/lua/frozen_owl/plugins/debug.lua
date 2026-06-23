return {
  {
    'mfussenegger/nvim-dap',
    dependencies = {
      'rcarriga/nvim-dap-ui',
      'nvim-neotest/nvim-nio',
      'mfussenegger/nvim-dap-python',
    },
    config = function()
      local dap = require('dap')
      local dapui = require('dapui')
      dapui.setup()
      require('dap-python').setup(vim.fn.getcwd() .. '/.venv/bin/python')

      vim.keymap.set('n', '<F5>', dap.continue, { desc = 'Debug continue' })
      vim.keymap.set('n', '<F10>', dap.step_over, { desc = 'Debug step over' })
      vim.keymap.set('n', '<F11>', dap.step_into, { desc = 'Debug step into' })
      vim.keymap.set('n', '<F12>', dap.step_out, { desc = 'Debug step out' })
      vim.keymap.set('n', '<leader>b', dap.toggle_breakpoint, { desc = 'Toggle breakpoint' })
      vim.keymap.set('n', '<leader>du', dapui.toggle, { desc = 'Debug UI' })
    end,
  },
}
