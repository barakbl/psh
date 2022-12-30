# psh / Simple Python shell

A basic Python based UNIX shell
This is in WIP and only intended for learning purpose


## Run:
`
python psh.py
`

## Features
- command history view (in memory only)
- a config directory, an env file example in env.example, to use it:

`
mkdir ~/.psh
cp psh.config ~/.psh/env
`
- set and view env vars (using builtin _**env**_ command)
- show the current directory, implementation of cd, exit and source
- basic autocomplete support
- basic command history support
- pipe support

## TODO
- plugins support
- tests
- better handling of returned errors from commands