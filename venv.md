# Python 3.10 Setup with pyenv on macOS

This guide explains how to install Python 3.10 on macOS using `pyenv`, set it as the default version, and create a virtual environment.

---

## Requirements

- macOS
- Homebrew (https://brew.sh/)
- Terminal (zsh or bash)

---

## Installation Steps

### 1. Install Homebrew (if you don't have it)
```bash
brew -v # Check if Homebrew is installed
```
if installed skip this step

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install pyenv

```bash
brew install pyenv
```

### 3. Configure Shell for pyenv

Add the following lines to your shell configuration file:
- For **zsh** (`~/.zshrc`):

  ```bash
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
  echo 'eval "$(pyenv init -)"' >> ~/.zshrc
  source ~/.zshrc
  ```

- For **bash** (`~/.bash_profile`):

  ```bash
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
  echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile
  echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
  source ~/.bash_profile
  ```

### 4. Install Python 3.10

```bash
pyenv install 3.10.13
```

You can check all available versions with:

```bash
pyenv install --list
```

### 5. Set Python 3.10 as Global Version

```bash
pyenv global 3.10.13
```

Verify installation:

```bash
python --version
```

---

## Create and Use a Virtual Environment

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

This will create a folder called `.venv/`.

### 2. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

Your terminal will show `(.venv)` when activated.

---

## Tips

- Use `pyenv local 3.10.13` to set Python 3.10 for a specific project directory.
- Use `pyenv versions` to list installed Python versions.
- Use `pyenv uninstall 3.10.13` to remove a version if needed.

---

# Done! 🚀  
You are now ready to work with Python 3.10 and virtual environments.
