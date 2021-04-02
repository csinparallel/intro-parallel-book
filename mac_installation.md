# Instructions For Setting Up The Runestone Environment On Mac OS X
By Suzanne Rivoire, Ph.D.
Sonoma State University

## My Mac preliminaries

### Homebrew package manager
Why?  [How to set up virtual environments for Python on MacOS | Opensource.com](https://opensource.com/article/19/6/python-virtual-environments-mac)
How? [The Missing Package Manager for macOS (or Linux) — Homebrew](https://brew.sh/)
Note that Homebrew seems to install Xcode command line tools if needed, contrary to what most articles suggest.

### Pyenv
Better solution than having Homebrew manage your Python:
* [How to set up virtual environments for Python on MacOS | Opensource.com](https://opensource.com/article/19/6/python-virtual-environments-mac)
* [The right and wrong way to set up Python 3 on MacOS | Opensource.com](https://opensource.com/article/19/5/python-3-default-mac)

```
$ brew install pyenv pyenv-virtualenv
$ cd ~/
$ echo ‘eval “$(pyenv init -)”’ >> .bash_profile
$ echo ‘eval “$(pyenv-virtualenv init -)”’ >> .bash_profile
$ brew install zlib sqlite
```

### Python latest version
```
$ export LDFLAGS="-L/usr/local/opt/zlib/lib -L/usr/local/opt/sqlite/lib"
$ export CPPFLAGS="-I/usr/local/opt/zlib/include -I/usr/local/opt/sqlite/include"
$ pyenv install 3.9.2 # or whatever the latest is
```
### Set pyenv default to latest Python version and update bash profile
`$ pyenv global 3.9.2 `
and verify it worked 
```
$ pyenv version
3.7.3 (set by /Users/rivoire/.pyenv/version)
```
After confirmation:
`$ echo -e ‘if command -v pyenv 1>/dev/null 2>&1; then\n  eval “$(pyenv init -)”\nfi’ >> ~/.bash_profile`
Remove the earlier Python stuff from path, keeping the pyenv init lines

## Setting up and installing Runestone

Reference
* [Managing Multiple Python Versions With pyenv – Real Python](https://realpython.com/intro-to-pyenv/#virtual-environments-and-pyenv)
* [runestone · PyPI](https://pypi.org/project/runestone/)

One-time: Create virtual environment
```
$ pyenv virtualenv 3.9.2 PDCbook
```

One time? Set up local .python_version file
```
$ pyenv local myproject
```

Virtual environment doesn’t need to be activated or deactivated after this - will happen when entering or exiting project directory.
```
$ pip install runestone
```

## Checking out PDCbook repo

Install GitHub CLI and authorize to use GH account:
```
$ brew install gh
$ gh auth login
```

Fork http://github.com/csinparallel/intro-parallel-book

Clone my fork:
```
 gh repo clone srivoire/intro-parallel-book
```