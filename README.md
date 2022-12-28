# psh / Simple Python shell

A basic Python based UNIX shell
This is in WIP and only intended for learning purpose


## Running
`
python psh.py
`

 


## Features
- command history view (in memory only)
- a config file (see psh.config for example)
- set and view env vars
- show the current directory, implementation of cd and exit
## TODO
- pipe (|) support is  vary important but not implemented yet
- compilation support
- save history in disk (and load it in new psh)
- colors for nicer shell view
- plugins support
- tests
- support for ~  in paths
- better handling of returned errors from commands