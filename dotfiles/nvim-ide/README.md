# Neovim IDE config

## Install

```bash
cp -r nvim-ide-config ~/.config/nvim-ide
nvim
NVIM_APPNAME=nvim-ide nvim 
```

Inside Neovim, run:

```vim
:Lazy sync
:Mason
```

Install external CLI tools used by this config:

```bash
uv tool install ruff
uv tool install mypy
npm install -g prettier
sudo apt install ripgrep fd-find
```

The config expects a project `.venv` for debugging and normal `uv run ...` usage.

##  Mappings cheatsheet

- `<leader>ff` find files
- `<leader>fg` grep project
- `<leader>e` file explorer
- `<leader>f` format
- `<leader>ca` code action
- `<leader>rn` rename
- `<leader>xx` diagnostics
- `<leader>us` `uv sync`
- `<leader>ur` `uv run python %`
- `<leader>ut` `uv run pytest`
- `<leader>um` `uv run mypy .`
- `<leader>uf` `uv run flask run`
- `<F5>` start/continue debugger
