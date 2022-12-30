# psh / Simple Python shell

A basic Python based UNIX shell
This is in WIP and only intended for learning purpose


## Running
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
- pipe support

## TODO
- save history in disk and use it in new psh process
- plugins support
- tests
- better handling of returned errors from commands