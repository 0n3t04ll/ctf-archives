#!/usr/bin/env python3
import string

def main():
        whiteList = string.ascii_letters + string.digits + ",!?;`#+-/$@&|~^<>(){}"
        blackList = vars(__builtins__).copy()
        for key in (
                "getattr", "exec", "open", "__builtins__", "__build_class__", "__loader__", "__spec__"
        ):blackList[key] = None
        pwnhub = '''pwnhub'''
        print(pwnhub)
        print("Hi, Guys! Welcome to pyjail!")
        print("Are you looking for the flag?")
        print("No words, Show me your Payload:)")
        while True:
                line = input("$ ")
                if not line:
                        continue
                if any(keyword not in whiteList for keyword in line):
                        print("Oh, You are hacker:(")
                        continue
                try:
                        print(eval(line, blackList))
                except Exception as e:
                        print(e)

if __name__ == "__main__":
        main()