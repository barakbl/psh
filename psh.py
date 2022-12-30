#!/bin/env python
import readline
import os, sys
import subprocess
import signal


def add_color_to_text(text: str, color: str = "OKCYAN") -> str:
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


default_envvars = {
    "PSH_MAX_HISTORY_SIZE": 100,
    "PSH_PROMPT": f"$ ",
    "TERM": "xterm-256color",  # TODO
}


def load_default():
    for k in default_envvars:
        load_env(k, str(default_envvars[k]))


history = []


def cwd(absolute: bool = False):
    d = subprocess.check_output("pwd").decode("utf-8").replace("\n", "")
    if absolute:
        return d
    return d.split("/").pop() or "/"


last_dir = cwd(absolute=True)


def history_cmd() -> None:
    [print(i) for i in history[::-1] if i !="-----"]


def insert_history(cmd: str) -> None:
    if len(history) == os.environ.get("MAX_HISTORY_SIZE"):
        history.pop(0)
        history.append(cmd)
    else:
        history.append(cmd)


def help(cmd: str):
    print(f"\n###########################################################\n"
          f"This is psh, a simple shell written in Python by Barak Bloch\n"
          f"homepage: https://github.com/barakbl/psh\n\n"
          f"any question? contact me barak.bloch at gmail.com\n"
          f"###########################################################\n")


def cd(target: str):
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


def run_command(cmd: str, tokens: list =None):
    if "|" in tokens:
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(ps.communicate()[0].decode("utf-8")[0:-1])
        return
    try:
        subprocess.run(tokens)
    except Exception as e:
        print(f"psh: command not found: {cmd}")


def env_cmd(var=None, ret=False):
    if var:
        v = var.split("=")
        if len(v) == 1:
            out = os.environ.get(var, f"env variable {var} not set")
            if ret:
                return out
            else:
                print(out)
        else:
            os.environ[v[0]] = v[1]
    else:
        out = dict(os.environ)
        if ret:
            return out
        else:
            print(out)


def parse_to_tokens(command: str) -> list:
    HOME = os.environ.get("HOME")
    tokens = [
        t.replace("~", HOME, 1) if t.startswith("~") else t
        for t in command.split(" ")
        if t not in [""]
    ]
    return tokens


def autocomplete(text: str, state):
    vocab = history + ["cd", "pwd", "top", "whoami", "cat", "ls", "git", "echo"]
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]


def load_env(key: str, val: str):
    os.environ[key] = val

def source(*args):
    if len(args) == 0:
        print(add_color_to_text("psh: error, source file not passed", "FAIL"))

    for a in args:
        try:
            with open(os.path.abspath(a)) as f:
                lines = f.readlines()
                for l in lines:
                    k, v = l.replace("\n", "").split("=")
                    load_env(k.strip(), v.replace("\"", "").strip())
        except:
            print(add_color_to_text(f"psh: error while load source file {a}", "FAIL"))

def get_history_file_path():
    return f"{os.environ.get('HOME')}/.psh/history"
def load_history():
    global history
    with open(get_history_file_path(),"r") as f:
        data = f.read()
        if data:
            hist =  data.split("\n") +  ["-----"]
            history = [h for h in hist if h !=""]
def init():
    load_default()

    signal.signal(signal.SIGTERM, sigterm_handler)
    PSH_DIR = f"{os.environ.get('HOME')}/.psh"
    ENV_FILE = f"{PSH_DIR}/env"
    HIST_FILE = get_history_file_path()
    if not os.path.isdir(PSH_DIR):
        os.makedirs(PSH_DIR)
    if os.path.isfile(ENV_FILE):
        source(ENV_FILE)
    if not os.path.isfile(HIST_FILE):
        with open(HIST_FILE,"w") as f:
            f.write("")
    load_history()
def save_history():
    his = []
    for h in history[::-1]:
        if h == "-----":
            break
        his.append(h)

    with open(get_history_file_path(),"r") as f:
        data = f.read()
        d = data.split("\n")
        out = his + d
    with open(get_history_file_path(), "w") as f:
        f.write("\n".join(out[0:int(os.environ.get("PSH_MAX_HISTORY_SIZE"))]))

def sigterm_handler(_signo, _stack_frame):
    ## save history
    save_history()
if __name__ == "__main__":
    readline.parse_and_bind("tab: complete")
    init()
    while True:
        readline.set_completer(autocomplete)
        inp = input(f"{env_cmd('PS1',ret=True)} {add_color_to_text(cwd())} {os.environ.get('PSH_PROMPT')} ").strip()
        tokens = parse_to_tokens(inp)

        if inp.startswith("exit"):
            save_history()
            sys.exit(0)
        elif inp.startswith("help"):
            help(inp)
        elif inp.startswith("source"):
            source(tokens[1:])
        elif inp.startswith("cd"):
            cd(inp[3:].strip())
        elif inp.startswith("history"):
            history_cmd()
        elif inp.startswith("env"):
            env_cmd(inp[3:].strip())
        else:
            run_command(inp, tokens)
        insert_history(inp)
