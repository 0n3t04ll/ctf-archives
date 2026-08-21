#!/usr/bin/env python3

import os
import re
import hashlib

FLAG = os.environ.get("FLAG", "bhackariCTF{redacted_flag}")

class LCG:
    def __init__(self, a=1664525, c=1013904223, m=1 << 48):
        self.a = a
        self.c = c
        self.m = m
        seed_bytes = (self.m.bit_length() + 7) // 8
        self.state = int.from_bytes(os.urandom(seed_bytes), "big") % self.m

    def next(self):
        current = self.state
        self.state = (self.a * self.state + self.c) % self.m
        return current

class UniversalGrid:
    def __init__(self):
        self.special_grid = {}
        self.rule = lambda x: x
        self.lcg = LCG()

    def set_rule(self, expr_str):
        # Allow only digits, x, and +-*/%^
        if not re.fullmatch(r"[0-9x+\-*/%^]*", expr_str):
            print("[Error]: Expression contains forbidden characters.")
            self.rule = lambda x: x
            return
        try:
            full_expr = f"lambda x: {expr_str}"
            self.rule = eval(full_expr, {"__builtins__": {}})
        except Exception as e:
            print(f"[Error]: Could not evaluate '{expr_str}'. Error: {e}")
            self.rule = lambda x: x

class Challenge:
    def __init__(self):
        self.grid = UniversalGrid()
        self.sec_par = 128

    def final_check(self):
        common_digest = None
        used_states = set()
        max_prints = 40
        global_collision_check = True

        for i in range(self.sec_par):
            try:
                x = self.grid.lcg.next()

                if x in self.grid.special_grid:
                    state = self.grid.special_grid[x]
                else:
                    state = self.grid.rule(x)

                state = int(state)
                state = state % (1 << (512 * 16))

                used_states.add(state)

                byte_len = max(1, (state.bit_length() + 7) // 8)
                state_bytes = state.to_bytes(byte_len, "big", signed=False)
                digest = hashlib.md5(state_bytes).hexdigest()
                
            except Exception:
                return False

            if i == 0:
                common_digest = digest
                print(f"[OK] Common digest = {common_digest}")
            else:
                if digest == common_digest:
                    if i < max_prints:
                        print(f"[{i}] Common digest == {digest}")
                else:
                    global_collision_check = False
                    if i < max_prints:
                        print(f"[{i}] Common digest != {digest} ❌")

        if not global_collision_check:
            print("[Error]: Your universe didn’t collapse.")
            return False

        if len(used_states) < self.sec_par:
            print("[Error]: Your rule is not injective; you chose an already-collapsed universe.")
            return False

        return True

    def interact(self):
        print("Do you have what it takes to build a Universal Collider?")
        print("Your task is to describe a narrow strip of cosmos where every world will collide with every other.")
        print("You can input a universal rule to easily assign a state to each position in the strip,")
        print("or manually place specific planets by setting their (position → state).")
        print("We'll then verify the grand collapse.")

        while True:
            print("\nChoose an option:")
            print("1) Set a cosmic rule (e.g., x*3+1)")
            print("2) Place a planet: insert (position, state) into the star map")
            print("3) Run the simulation and check for a universal collision")
            print("4) Give up (quit)")
            choice = input("> ")

            if choice == "1":
                expr = input("Enter the expression (only: x, digits, + - * / % ^): ")
                self.grid.set_rule(expr)

            elif choice == "2":
                try:
                    pos = int(input("Position (integer): "))
                    st  = int(input("State (integer): "))
                    self.grid.special_grid[pos] = st
                    print("Added")
                except ValueError:
                    print("Invalid input.")

            elif choice == "3":
                success = self.final_check()
                if success:
                    print("🎉 FIREWORKS! You’ve built a true Universal Collider!")
                    print(f"FLAG: {FLAG}")
                    break
                else:
                    print("❌ Collapse not achieved.")

            elif choice == "4":
                print("Hope to see you soon.")
                break

            else:
                print("Invalid option.")

if __name__ == "__main__":
    challenge = Challenge()
    challenge.interact()
