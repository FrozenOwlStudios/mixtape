local map = vim.keymap.set

map('n', '<Esc>', '<cmd>nohlsearch<CR>')
map('n', '<leader>w', '<cmd>w<CR>', { desc = 'Save file' })
map('n', '<leader>q', '<cmd>q<CR>', { desc = 'Quit window' })
map('n', '<leader>e', '<cmd>Neotree toggle<CR>', { desc = 'File explorer' })
map('n', '<leader>ff', '<cmd>Telescope find_files<CR>', { desc = 'Find files' })
map('n', '<leader>fg', '<cmd>Telescope live_grep<CR>', { desc = 'Live grep' })
map('n', '<leader>fb', '<cmd>Telescope buffers<CR>', { desc = 'Buffers' })
map('n', '<leader>fh', '<cmd>Telescope help_tags<CR>', { desc = 'Help' })
map('n', '<leader>tt', '<cmd>ToggleTerm<CR>', { desc = 'Terminal' })
map('n', '<leader>gg', '<cmd>LazyGit<CR>', { desc = 'LazyGit' })
map('n', '<leader>xx', '<cmd>Trouble diagnostics toggle<CR>', { desc = 'Diagnostics' })
map('n', '<leader>cs', '<cmd>Telescope lsp_document_symbols<CR>', { desc = 'Document symbols' })

-- uv / Python project helpers
map('n', '<leader>us', '<cmd>terminal uv sync<CR>', { desc = 'uv sync' })
map('n', '<leader>ur', '<cmd>terminal uv run python %<CR>', { desc = 'uv run current Python file' })
map('n', '<leader>ut', '<cmd>terminal uv run pytest<CR>', { desc = 'uv run pytest' })
map('n', '<leader>um', '<cmd>terminal uv run mypy .<CR>', { desc = 'uv run mypy .' })
map('n', '<leader>uf', '<cmd>terminal uv run flask run<CR>', { desc = 'uv run flask run' })
