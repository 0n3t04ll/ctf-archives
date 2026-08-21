#!/usr/bin/env python3

import hashlib
import os

FLAG = os.environ.get("FLAG", "bhackariCTF{redacted_flag}")

statement = (
    "Venice is a * city . The food there is * . People in there are * . "
    "The weather is * . The architecture is * . The canals are * . "
    "The nightlife is * . The art is * . The history is * . "
    "The shopping is * . The transportation is * . The hotels are * . "
    "The festivals are * . The parks are * . The safety is * . "
    "The cost is * . The music is * . The sports are * . The schools are * . "
    "The hospitals are * . The streets are * . The squares are * . The monuments are * . "
    "The museums are * . The churches are * . The bridges are * . The gardens are * . "
    "The lakes are * . The mountains are * . The rivers are * . The forests are * . "
    "The animals are * .") # The birds are * . The insects are * . The fish are * . "
    # "The shops are * . The markets are * . The bakeries are * .")




good_words = ["cool", "great", "friendly", "sunny", "beautiful", "romantic", "gorgeous", "lively", "artistic", "historic", "trendy", "convenient", "comfortable", "good", "upbeat", "heavenly",  "stylish", "fashionable",
              "delicious", "tasty", "fresh", "authentic", "exciting", "fascinating", "vibrant", "efficient", "luxurious", "fun", "relaxing", "safe", "affordable", "amazing", "wonderful", "charming", "snazzy", "swanky",
              "delightful", "enchanting", "inviting", "captivating", "breathtaking", "spectacular", "stunning", "magnificent", "festive", "welcoming", "hospitable", "clean", "organized", "modern", "innovative",
              "eco-friendly", "sustainable", "family-friendly", "adventurous", "cultural", "picturesque", "scenic", "tranquil", "serene", "idyllic", "legendary", "mythical", "paradisiacal", "utopian", 
              "divine", "exquisite", "splendid", "radiant", "joyful", "cheerful", "glorious", "impressive", "outstanding", "superb", "marvelous", "fantastic", "brilliant", "stellar", "positive", "optimistic", 
              "resplendent", "flourishing", "prosperous", "thriving", "robust", "dynamic", "energetic", "vivacious", "zestful", "peppy", "buoyant", "gleeful", "mirthful", "jubilant", "exuberant","dapper",
              "admirable", "commendable", "laudable", "notable", "noteworthy", "exceptional", "phenomenal", "majestic", "regal", "noble", "pristine", "untarnished", "unblemished", "immaculate", "swish", 
              "spotless", "crisp", "refreshing", "soothing", "harmonious", "peaceful", "calm", "gentle", "mellow", "graceful", "elegant", "refined", "cultured", "sophisticated", "polished", "chic"]
            #    "debonair", "gallant", "valiant", "heroic", "intrepid", "fearless", "bold", "courageous", "resourceful", "ingenious",
            #   "inventive", "creative", "artful", "inspired", "visionary", "forward-thinking", "progressive", "modernistic", "cutting-edge", "state-of-the-art", "avant-garde", "trendsetting", "trailblazing"


bad_words = ["boring", "bad", "unfriendly", "rainy", "ugly", "dull", "uncomfortable", "overcrowded", "expensive", "dirty", "noisy", "crowded", "unsafe", "slow", "inefficient","abandoned", "infested",
             "terrible", "awful", "disgusting", "inedible", "bland", "overrated","depressing", "dreary", "gloomy", "unpleasant", "horrible", "lousy", "pathetic", "crumbling", "derelict", "chilly",  
             "hideous", "grimy", "filthy", "seedy", "squalid", "dingy", "chaotic", "disorganized", "polluted", "outdated", "obsolete", "ineffective", "inconvenient", "unreliable", "decrepit", "raw",
             "dangerous", "overpriced", "unaffordable", "stressful", "frustrating", "disappointing", "unwelcoming", "hostile", "rude", "impolite", "unhygienic", "unsanitary", "dilapidated", "run-down", 
             "atrocious", "appalling", "dreadful", "ghastly", "horrendous", "abysmal", "wretched", "deplorable", "lamentable", "dire", "grim", "bleak", "forlorn", "hopeless", "desolate", "neglected",
             "ravaged", "ruined", "wrecked", "shabby", "tattered", "battered", "mangled", "mutilated", "scarred", "marred", "defaced", "defiled", "tainted", "corrupt", "vile", "vicious", "nippy",
             "malicious", "malevolent", "sinister", "ominous", "menacing", "threatening", "perilous", "hazardous", "risky", "treacherous", "precarious", "unstable", "volatile", "explosive", "outraged",
             "tumultuous", "turbulent", "stormy", "tempestuous", "wild", "fierce", "savage", "brutal", "barbaric", "cruel", "ruthless", "merciless", "pitiless", "cold", "icy", "frigid",  "indignant",]
            #  "biting", "stinging", "scathing", "scornful", "contemptuous", "disdainful", "disgusted", "repulsed", "revolted", "nauseated", "sickened", "offended",
            #  "insulted", "affronted",  "aggrieved", "resentful", "embittered", "sullen", "surly", "gruff", "brusque", "curt", "snappish", "crabby", "cantankerous"

assert len(good_words) == len(set(good_words))
assert len(bad_words) == len(set(bad_words))

def hash(s: str) -> int:
    # Use SHA-256 for hashing
    h = hashlib.sha256(s.encode('utf-8')).digest()
    # Take the last 6 bytes (lower 48 bits)
    lower_48 = int.from_bytes(h[-6:], 'big')
    return lower_48

def main():
    # print(len(good_words), "good words available.")
    # print(len(bad_words), "bad words available.")
    # print(statement.count("*"), "words to fill in.\n")

    print("You are being interviewed by two journalists about Venice.")
    print("They are from two different journals with different opinions about Bhackari.")
    print("Journalist 1 always enjoys visiting them, while Journalist 2 is a friend of an opposing team.")
    print("However, they will check, via hash, that you said the same things to both of them!\n")
    print("They both sent you the same template to follow for your interview.")
    print("--- Statement Template ---")
    print(statement)
    print("-------------------------\n")
    msg1 = input("Enter your statement for Journalist 1: ").strip()
    msg2 = input("Enter your statement for Journalist 2: ").strip()

    msg1_parts = msg1.split(" ")
    msg2_parts = msg2.split(" ")
    statement_parts = statement.split(" ")

    # Check that the statements match the template
    if len(msg1_parts) != len(statement_parts) or len(msg2_parts) != len(statement_parts):
        print(f"Your statements do not match the template.")
        return False
    for i, word in enumerate(statement_parts):
        if word != "*":
            if msg1_parts[i] != word or msg2_parts[i] != word:
                print(f"Your statements do not match the template.")
                return False

    # Check that all words in msg1 corresponding to '*' are in good_words and all are different
    msg1_good_words = [msg1_parts[i] for i, word in enumerate(statement_parts) if word == "*"]
    if len(msg1_good_words) != len(set(msg1_good_words)):
        print("Journalist 1 thinks your statement is too repetitive.")
        return False
    for w in msg1_good_words:
        if w not in good_words:
            print(f"Journalist 1 is upset that you said '{w}'!")
            return False

    # Check that all words in msg2 corresponding to '*' are in bad_words and all are different
    msg2_bad_words = [msg2_parts[i] for i, word in enumerate(statement_parts) if word == "*"]
    if len(msg2_bad_words) != len(set(msg2_bad_words)):
        print("Journalist 2 thinks your statement is too repetitive.")
        return False
    for w in msg2_bad_words:
        if w not in bad_words:
            print(f"Journalist 2 is upset that you said '{w}'!")
            return False
        
    # Finally, check if the hashes are equal
    hash1 = hash(msg1)
    hash2 = hash(msg2)
    if hash1 != hash2:
        print("The journalists noticed that you are trying to play them!")
        return False
    else:
        print("Both journalists are satisfied with your statements!")
        print(f"Congratulations! Here is the flag: {FLAG}")
        return True

if __name__ == "__main__":
    main()



