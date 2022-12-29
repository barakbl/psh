# psh / Simple Python shell

A basic Python based UNIX shell
This is in WIP and only intended for learning purpose


## Running
`
python psh.py
`

 


## Features
- command history view (in memory only)
- a config file (save psh.config as ~/.psh and modify as needed):

`
cp psh.config ~/.psh
`
- set and view env vars (using builtin _**env**_ command)
- show the current directory, implementation of cd and exit
- basic autocomplete support
## TODO
- pipe (|) support is  very important but not implemented yet
- save history in disk (and load it in new psh)
- plugins support
- tests
- better handling of returned errors from commands