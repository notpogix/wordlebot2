from flask import Flask, request
import random, json, os

app = Flask(__name__)
WORDS = [
    "absence", "balloon", "cabinetry", "deliver", "elasticity", "flamingo", "granite", "harvests", "imagine", "journeys", "kingdoms", "luggage", "machine", "nucleus", "octagon", "paradox", "quantum", "radiant", "science", "temples", "utility", "vulture", "warrior", "zephyrs",
"alchemy", "balance", "cascade", "decline", "eclipse", "forever", "gravity", "harbour", "immense", "justice", "lantern", "magnets", "neutral", "organic", "program", "reality", "silence", "tribute", "unknown", "venture",
"absolve", "biscuit", "clarity", "defense", "embrace", "fortune", "glimmer", "harvest", "initial", "journey", "kingpin", "letters", "mariner", "nostalg", "outline", "perform", "resolve", "sunrise", "through", "vintage",
"actress", "brewing", "channel", "diamond", "elegant", "freedom", "gateway", "highway", "impress", "justice", "landing", "measure", "natural", "orchard", "penguin", "rejoice", "shimmer", "tornado", "upwards", "voyager",
"adrenal", "builder", "cluster", "descent", "endless", "fiction", "glacier", "harmony", "inspire", "kitchen", "logical", "minimal", "nothing", "outside", "pattern", "renewal", "stellar", "tonight", "utility", "wonders",
"airwave", "bravery", "collect", "digital", "essence", "forging", "genuine", "harried", "insight", "journal", "kingdom", "library", "moments", "nourish", "officer", "passion", "reflect", "station", "united", "whistle",
"ancient", "breathe", "compass", "discard", "eternal", "flourish", "gallery", "harvest", "infused", "journey", "landing", "machine", "neptune", "organic", "protect", "resolve", "summits", "tension", "uplands", "wonder",
"appears", "between", "courage", "distant", "efforts", "fantasy", "glisten", "horizon", "install", "justice", "knowing", "measure", "morning", "network", "optical", "promise", "respect", "surface", "turbine", "visible",
"arrived", "beneath", "comfort", "dolphin", "elastic", "freight", "gallery", "honesty", "invited", "journey", "lantern", "marshal", "notable", "opinion", "passage", "recover", "shallow", "tribune", "upgrade", "vibrant",
"aspired", "broaden", "compose", "drought", "endless", "fragile", "griddle", "humming", "include", "journal", "keeping", "logical", "monster", "numeric", "orchids", "precise", "reserve", "texture", "utopian", "warfare",
"arrange", "bargain", "context", "deflect", "enchant", "festival", "glowing", "hustled", "invader", "journey", "kinglet", "lighter", "mystery", "notches", "operate", "prepare", "ripples", "subtlet", "unravel", "village",
"archive", "bassist", "comfort", "deliver", "emerald", "fiction", "gallant", "heroine", "include", "justice", "leading", "manager", "nothing", "obvious", "prelude", "remnant", "sincere", "theatre", "unequal", "voyager",
"adapter", "beloved", "caption", "density", "exhibit", "forgive", "granary", "honored", "insider", "journey", "keeper", "lingual", "modesty", "nautics", "offbeat", "patient", "rebuild", "stretch", "tumbler", "victory",
"advance", "brisket", "contain", "diverse", "eastern", "fiction", "glimmer", "heights", "inquire", "justice", "knitted", "landing", "marquee", "numeric", "observe", "preachy", "rushing", "skilled", "thistle", "unknown",
"afflict", "banquet", "contact", "decibel", "empower", "forward", "glacier", "hustler", "injured", "journey", "legible", "mankind", "natural", "operate", "perfect", "reserve", "spirits", "tranquil", "unevent", "visible",
"alright", "brutish", "control", "dormant", "embrace", "forging", "gesture", "highest", "invoked", "justice", "kingdom", "lighter", "measure", "network", "opulent", "program", "reflect", "sublime", "thunder", "venture",
"another", "bravest", "capture", "decline", "enchant", "fragile", "graceful", "harbour", "inspire", "journey", "knitted", "lasting", "moment", "outside", "proverb", "respect", "station", "tangent", "untamed", "voyager",
"arrival", "blanket", "chapter", "descent", "element", "fantasy", "glimmer", "healing", "involve", "journey", "library", "mystery", "nearest", "opinion", "pursuit", "renewed", "serpent", "tonight", "upright", "warrior",
"antenna", "breathe", "combine", "deliver", "emerald", "forging", "gravity", "harvest", "impress", "justice", "knitted", "landing", "monster", "notable", "outline", "patient", "rebuild", "sunrise", "tension", "village",
"ascend", "ballast", "collect", "dynamic", "elevate", "fiction", "glisten", "honored", "immense", "journey", "keeper", "library", "monster", "opulent", "protect", "recover", "spirits", "tonight", "unravel", "voyager"

]

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    else:
        word = random.choice(WORDS)
        state = {"word": word, "wrong_guesses": 0}
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
        return state

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

@app.route("/wordle")
def wordle():
    user = request.args.get("user", "unknown")
    guess = request.args.get("guess")
    state = load_state()
    word = state["word"]
    wrong_guesses = state.get("wrong_guesses", 0)

    # Calculate how many letters to reveal (starts at 2, adds 1 every 5 wrong guesses)
    letters_to_show = 2 + (wrong_guesses // 5)
    letters_to_show = min(letters_to_show, len(word))  # Don't exceed word length

    # Build the hint
    revealed = word[:letters_to_show]
    hidden = " ".join(["_"] * (len(word) - letters_to_show))
    hint = revealed + (" " + hidden if hidden else "")

    if not guess:
        return f"Hint: {hint}"
    if guess and guess.lower() == word.lower():
        new_word = random.choice([w for w in WORDS if w != word])
        state = {"word": new_word, "wrong_guesses": 0}  # Reset counter
        save_state(state)
        new_hint = new_word[:2] + " " + " ".join(["_"] * (len(new_word) - 2))
        return f"/me !give {user} 20000\n FeelsGoodMan 🎉 {user} guessed it! The word was '{word}'. They have guessed $(count.increment count-$(sender.provider_id)) wordles correctly!  New hint: {new_hint}"
    else:
        # Increment wrong guess counter
        state["wrong_guesses"] = wrong_guesses + 1
        save_state(state)
        # Recalculate hint with new guess count
        letters_to_show = 2 + (state["wrong_guesses"] // 5)
        letters_to_show = min(letters_to_show, len(word))
        revealed = word[:letters_to_show]
        hidden = " ".join(["_"] * (len(word) - letters_to_show))
        hint = revealed + (" " + hidden if hidden else "")
        return f"/me NOPERS {user}! Try again. Hint: {hint}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))