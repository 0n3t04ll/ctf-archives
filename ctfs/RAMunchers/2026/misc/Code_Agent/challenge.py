#!/usr/bin/python3

BLOCKLIST: list[str] = ['.', '\\', '[', ']', '{', '}',':', "blocklist", "globals", "compile", "sys"]
DISABLE_FUNCTIONS: list[str] = ["getattr", "setattr", "eval", "exec", "breakpoint", "lambda", "help", "list", "tuple", "dict"]
DISABLE_FUNCTIONS: dict = {func: None for func in DISABLE_FUNCTIONS}
   
def filter_command(command: str) -> tuple[bool, str]:
    is_valid: bool = True
    command = ''.join(char for char in command if ord(char) < 128) # remove any unicode etc

    if any([b in command for b in BLOCKLIST]):
        print("Invalid")
        is_valid = False
    return is_valid, command

def main() -> None:
    print('How can I help you?')
    cmd: str = input('>>> ')
    valid_command, cmd = filter_command(cmd)
    
    if not valid_command:
        print("Invalid command")
        return

    try:
        print(eval(cmd, DISABLE_FUNCTIONS))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
