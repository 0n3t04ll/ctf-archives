#!/usr/bin/env python3
# ❄️ Winterbucks Secret Confession ❄️
# Someone left a confession in the code... can you find it?

import sys
import base64
from functools import reduce

# Frozen layers of winter secrets
_SNOWFLAKE = [119, 105, 110, 116, 101, 114, 95, 109, 97, 103, 105, 99]
_ICICLE = lambda x: ''.join([chr(i) for i in x])
_FROST = bytes([102, 114, 111, 122, 101, 110, 95, 104, 101, 97, 114, 116])

class WinterBucks:
    def __init__(self):
        self._snow = [0x57, 0x69, 0x6e, 0x74, 0x65, 0x72]
        self._flake = [0x73, 0x65, 0x63, 0x72, 0x65, 0x74]
        self._storm = self._generate_blizzard()
        
    def _generate_blizzard(self):
        return ''.join([chr(x) for x in self._snow + self._flake])
    
    @staticmethod
    def _cold_brew(mixture):
        return bytes([b ^ 0x42 for b in mixture])
    
    @staticmethod
    def _iced_latte(espresso):
        return ''.join([chr(ord(c) - 3) for c in espresso])
    
    @staticmethod
    def _peppermint_mocha(ingredients):
        steamed = []
        for i, byte in enumerate(ingredients):
            steamed.append(byte ^ (i % 256))
        return bytes(steamed)
    
    def _avalanche_encryption(self, data):
        layer1 = base64.b64encode(data.encode()).decode()
        layer2 = ''.join([chr(ord(c) + 5) for c in layer1])
        layer3 = layer2[::-1]
        return layer3
    
    def verify_confession(self, confession):
        # The winter magic verification spell
        frozen = self._avalanche_encryption(confession)
        
        # Magical winter constants
        _SNOW_DEPTH = "BBV_p>7^l97gtW]jVGX_7>LglpJN;97guS8hq_rg{SLN~[Lizq7ilp]Y"
        _ICE_CRYSTAL = self._cold_brew(bytes([35, 54, 33, 33, 54, 36, 29]))
        
        # Layer upon layer of winter frost
        thaw_step1_encrypted = bytes([96, 111, 37, 100, 120, 32, 98, 39, 101, 124, 32, 106, 37])
        thaw_step1_decoded = bytes([c ^ 0x13 for c in thaw_step1_encrypted]).decode()
        thaw_step2 = self._iced_latte(thaw_step1_decoded)
        
        # The confession checker
        if frozen == _SNOW_DEPTH:
            magic_phrase = _ICE_CRYSTAL.decode()
            winter_secret = magic_phrase + thaw_step2
            return True, winter_secret
        
        return False, None

def _hidden_in_snow():
    """The confession lies dormant in winter's embrace"""
    _glacier = [0x4d, 0x79, 0x20, 0x77, 0x69, 0x6e, 0x74, 0x65, 0x72, 
                0x20, 0x63, 0x6f, 0x6e, 0x66, 0x65, 0x73, 0x73, 0x69,
                0x6f, 0x6e, 0x3a, 0x20]
    
    # The barista's secret recipe
    _hot_cocoa = lambda beans: reduce(lambda a, b: a + chr(b), beans, '')
    
    # Multiple layers of obfuscation like layers of snow
    _sleet = bytes([34, 18, 18, 5, 18, 28, 84, 11, 26, 0x45, 
                    19, 71, 6, 84, 24, 66, 3, 70, 17, 29, 65])
    
    # Reverse the frost
    _blizzard_key = [i ^ 0x42 for i in _sleet]
    
    # Combine winter elements
    confession = _hot_cocoa(_glacier) + ''.join([chr(x) for x in _blizzard_key])
    
    return confession

def winter_storm(user_input):
    """Process the user's attempt through winter's gauntlet"""
    wb = WinterBucks()
    
    # Check if the confession matches
    is_valid, secret = wb.verify_confession(user_input)
    
    if is_valid:
        print("❄️ ═══════════════════════════════════════ ❄️")
        print("  The winter confession has been revealed!")
        print("❄️ ═══════════════════════════════════════ ❄️")
        print()
        print(f"  {secret}")
        print()
        print("❄️ ═══════════════════════════════════════ ❄️")
        return True
    else:
        print("🌨️  The confession remains frozen in ice...")
        return False

def main():
    print(r"""
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║            ❄️  WINTERBUCKS COFFEE ❄️                 ║
    ║                                                      ║
    ║            "Where Secrets Stay Warm"                 ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    print("  A barista left a confession in the code...")
    print("  Can you uncover their winter secret?")
    print()
    
    # Encrypted challenge prompt
    _prompt_frost = bytes([32, 11, 17, 0, 23, 69, 17, 13, 0, 69, 6, 10, 11, 
                           3, 0, 22, 22, 12, 10, 11, 69, 13, 0, 23, 0, 95])
    
    prompt = ''.join([chr(b ^ 0x65) for b in _prompt_frost])
    
    user_confession = input(f"  {prompt} ")
    print()
    
    winter_storm(user_confession)

# The real confession, frozen in time
_TRUE_CONFESSION = _hidden_in_snow()

if __name__ == "__main__":
    main()
