from flask import Flask, request
import random, json, os

app = Flask(__name__)
WORDS = [
    "plastic", "banana", "camera", "ocean", "marathon", "python",
    "internet", "television", "mountain", "keyboard", "window", "penguin", "marlon", "kiwi", "football", "rocket", "gym", "jolly", "basketball", "gymshark", "gamble", "trickster", "fooled", "internet", "monk", "notable", "fantasy", "quantum", "mystery", "glacier", "painter", "volcano", "pancake", "nebula",
    "emerald", "serpent", "enchanted", "origami", "peacock", "vibrate", "zephyr", "latitude", "fortune",
    "dragonfly", "clothes", "silence"
]

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    else:
        word = random.choice(WORDS)
        state = {"word": word}
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
    hint = word[:2] + " " + " ".join(["_"] * (len(word) - 2))

    if not guess:
        return f"Hint: {hint}"
    if guess and guess.lower() == word.lower():
        new_word = random.choice([w for w in WORDS if w != word])
        state["word"] = new_word
        save_state(state)
        new_hint = new_word[:2] + " " + " ".join(["_"] * (len(new_word) - 2))
        return f"!give {user} 1000\n🎉 {user} guessed it! The word was '{word}'. New hint: {new_hint}"
    else:
        return f"Nope, {user}! Try again. Hint: {hint}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
