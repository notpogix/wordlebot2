from flask import Flask, request
import random, json, os

app = Flask(__name__)
WORDS = [
    "plastic", "banana", "camera", "ocean", "marathon", "python",
    "internet", "television", "mountain", "keyboard", "window", "penguin", "marlon", "kiwi", "football", "rocket", "gym", "jolly", "basketball", "gymshark", "gamble", "trickster", "fooled", "internet", "monk", "notable", "fantasy", "quantum", "mystery", "glacier", "painter", "volcano", "pancake", "nebula",
    "emerald", "serpent", "enchanted", "origami", "peacock", "vibrate", "zephyr", "latitude", "fortune",
    "dragonfly", "clothes", "silence", "twitch", "faze", "lacy", "mario", "minecraft", "stableronaldo", "silky", "cinna", "chatters", "sped", "drew", "europe", "controversy", "lemon", "telephone", "drake", "playlist", "album", "tiktok", "prime", "banned", "time", "crazy", "streamer", "arsenal", "chelsea", "liverpool", "manchester", "united", "city", "tottenham", "everton", "leicester", "wolves", "villa", "newcastle", "brighton", "palace", "fulham", "brentford", "forest", "bournemouth", "southampton", "barcelona", "madrid", "atletico", "sevilla", "valencia", "villarreal", "betis", "sociedad", "athletic", "bilbao", "getafe", "osasuna", "mallorca", "girona", "almeria", "juventus", "milan", "inter", "napoli", "roma", "lazio", "fiorentina", "atalanta", "torino", "bologna", "genoa", "sassuolo", "udinese", "verona", "bayern", "dortmund", "leipzig", "leverkusen", "frankfurt", "gladbach", "wolfsburg", "freiburg", "# Months
"january", "february", "march", "april", "june", "july", "august", "september", "october", "november", "december", "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "hampshire", "jersey", "mexico", "york", "carolina", "dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "island", "tennessee", "texas", "utah", "vermont", "virginia", "washington", "wisconsin", "wyoming", "apple", "banana", "orange", "grape", "mango", "pineapple", "strawberry", "blueberry", "raspberry", "blackberry", "watermelon", "cantaloupe", "honeydew", "peach", "plum", "cherry", "apricot", "kiwi", "papaya", "guava", "lychee", "dragon", "passion", "coconut", "avocado", "lemon", "lime", "grapefruit", "tangerine", "clementine", "pomegranate", "persimmon", "fig", "date", "raisin", "cranberry", "mulberry", "gooseberry", "starfruit", "jackfruit", "durian", "rambutan", "longan", "tamarind", "aurora", "breeze", "castle", "delight", "erupt", "fabric", "galaxy", "harvest", "ignite", "jigsaw", "kingdom", "lantern", "meadow", "nectar", "oasis", "pistol", "quarry", "rewind", "summit", "temple", "utensil", "velvet", "wander", "xenon", "yellow", "zipper", "abrupt", "beacon", "circus", "denim", "engine", "fossil", "glacier", "harbor", "instant", "jungle", "kettle", "miracle", "noble", "orchard", "parrot", "quest", "ripple", "silver", "tunnel", "upshot", "venom", "winter", "xylem", "yawned", "zestful", "arcade", "column", "deity", "evolve", "gallop", "hybrid", "jaunty", "kayak", "lemony", "mimic", "nuance", "omen", "patrol", "query", "refuge", "shimmer", "talon", "unique", "vivid", "xenial", "yearn", "zealot", "adopt", "barrier", "clamor", "draped", "earnest", "flicker", "gusty", "hinge", "improv", "kinetic", "lavish", "niche", "opener", "plaza", "quiver", "robust", "statute", "thawed", "volume", "wrangle"

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
        return f"!give {user} 20000\n🎉 {user} guessed it! The word was '{word}'. New hint: {new_hint}"
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
        return f"Nope, {user}! Try again. Hint: {hint}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))