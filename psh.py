#!/bin/env python

import readline
import os, sys
import subprocess
import json

default_envvars = {
    "PSH_MAX_HISTORY_SIZE": 100,
    "PSH_PROMPT": f"$ ",
    "TERM": "xterm-256color",  # TODO
}


def add_color_to_text(text,color="OKCYAN"):
    colors = {
    "HEADER": '\033[95m',
    "OKBLUE": '\033[94m',
    "OKCYAN": '\033[96m',
    "OKGREEN": '\033[92m',
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m'
    }
    ENDC = '\033[0m'
    color = colors.get(color) or f"{colors['OKCYAN']}"
    return f"{color}{text}{ENDC}"


def load_config():
    ## default config
    for k in default_envvars.keys():
        os.environ[k] = str(default_envvars[k])

    ### load config
    conf_file = f"{os.environ.get('HOME')}/.psh"
    try:
        with open(conf_file) as f:
            data = json.loads(f.read())
            if "envvars" in data:
                for v in data["envvars"]:
                    os.environ[v] = data["envvars"][v]
    except:
        print("no config file found")


load_config()
history = []


def cwd(absolute=False):
    d = subprocess.check_output("pwd").decode("utf-8").replace("\n", "")
    if absolute:
        return d
    return d.split("/").pop() or "/"


last_dir = cwd(absolute=True)


def history_cmd():
    [print(i) for i in history[::-1]]


def insert_history(cmd):
    if len(history) == os.environ.get("MAX_HISTORY_SIZE"):
        history.pop(0)
        history.append(cmd)
    else:
        history.append(cmd)


def help(cmd):
    print(f"\n###########################################################\n"
          f"This is psh, a simple shell written in Python by Barak Bloch\n"
          f"homepage: https://github.com/barakbl/psh\n\n"
          f"any question? contact me barak.bloch at gmail.com\n"
          f"###########################################################\n")


def cd(target):
    global last_dir
    curr_dir = cwd(absolute=True)
    if not target:
        print("target is missing")
        return

    if target == "-":
        os.chdir(os.path.abspath(last_dir))
    else:
        try:

            os.chdir(os.path.abspath(target))
        except Exception:
            print(f"cd: no such file or directory: {target}")
    last_dir = curr_dir


def run_command(cmd, tokens=None):
    if "|" in tokens:
        print(add_color_to_text(f"psh: That`s embarcing, pipe (|) not supported yet","FAIL"))
        return
    try:
        subprocess.run(tokens)
    except Exception as e:
        print(f"psh: command not found: {tokens}")


def env_cmd(var=None):
    if var:
        v = var.split("=")
        if len(v) == 1:
            print(os.environ.get(var, f"env variable {var} not set"))
        else:
            os.environ[v[0]] = v[1]
    else:
        print(dict(os.environ))


def parse_to_tokens(command):
    HOME = os.environ.get("HOME")
    tokens = [
        t.replace("~", HOME,1) if t.startswith("~") else t
        for t in command.split(" ")
        if t not in [""]
    ]
    return tokens


def autocomplete(text, state):
    vocab = history + ["cd", "pwd", "top", "whoami", "cat", "ls", "git", "echo"]
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]


if __name__ == "__main__":
    readline.parse_and_bind("tab: complete")
    while True:
        readline.set_completer(autocomplete)
        inp = input(f"{add_color_to_text(cwd())} {os.environ.get('PSH_PROMPT')}").strip()
        tokens = parse_to_tokens(inp)
        inp = " ".join(tokens)

        if inp.startswith("exit"):
            sys.exit(0)
        elif inp.startswith("help"):
            help(inp)
        elif inp.startswith("cd"):
            cd(inp[3:].strip())
        elif inp.startswith("history"):
            history_cmd()
        elif inp.startswith("env"):
            env_cmd(inp[3:].strip())
        else:
            run_command(inp,  tokens)
        insert_history(inp)
