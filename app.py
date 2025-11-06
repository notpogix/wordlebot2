from flask import Flask, request
import random, json, os

app = Flask(__name__)
WORDS = [
    "anchor", "beetle", "cactus", "dancer", "eagle", "fabricate", "garden", "helmet", "island", "jungle", "kitten", "legend", "mystic", "notion", "oracle", "planet", "quartz", "rhythm", "shield", "throne", "uplift", "vacant", "whisper", "zeroth", "advent", "behold", "cobalt", "doodle", "effort", "filter", "glance", "harvested", "ignore", "jarvis", "keeper", "legacy", "mantle", "nectary", "oblong", "parade", "quench", "rubber", "signal", "thrill", "urgent", "victor", "wanderer", "zenith", "allied", "border", "copper", "dynamo", "expert", "frozen", "gentle", "humane", "injury", "jovial", "kernel", "living", "marine", "notice", "outfit", "poetic", "reason", "sacred", "tropic", "uneven", "virtue", "windowed", "zygote", "almost", "breeze", "carbon", "decent", "empire", "future", "growth", "humble", "impact", "jacket", "manual", "native", "object", "public", "reward", "simple", "tennis", "update", "visual", "wealth", "accept", "beauty", "custom", "daring", "exotic", "figure", "glider", "hazard", "inside", "joyful", "lawyer", "method", "normal", "option", "people", "rarely", "supply", "tender", "unique", "vacuum", "wander", "yellowed", "zodiac", "artist", "battle", "candle", "divide", "ethics", "forged", "golden", "hidden", "invest", "jumper", "latina", "motive", "number", "oppose", "praise", "reboot", "series", "subtle", "tunnel", "urgent", "valley", "wisdom", "yonder", "abound", "beyond", "clutch", "donate", "export", "forget", "grassy", "hearty", "infect", "joined", "little", "mutual", "oakley", "planet", "quaint", "retail", "secure", "threat", "unreal", "vision", "wither", "accord", "bother", "charge", "debate", "engineer", "formal", "gather", "helmeted", "inched", "jester", "lawful", "modern", "nature", "office", "proper", "result", "silent", "taught", "useful", "volume", "wonder", "aboard", "betray", "circle", "deluxe", "empire", "factor", "golden", "handle", "invent", "jungle", "lament", "memory", "object", "pillar", "quiver", "relief", "scheme", "trophy", "unison", "virtue", "winner", "zinger", "coastal", "cradle", "damage", "domain", "esteem", "fabric", "fusion", "genius", "heroic", "ignore", "jigsawed", "latest", "moment", "notary", "pickup", "quorum", "ranger", "symbol", "tonics", "update", "voyage", "wealthy"

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