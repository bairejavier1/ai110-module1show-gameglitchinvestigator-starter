import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, validate_range, check_guess, update_score
import random

# Streamlit page config
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

# Sidebar - Difficulty
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
low, high = get_range_for_difficulty(difficulty)
MAX_ATTEMPTS = 10  # fixed attempts for all difficulties

# FIX: Added game_id counter to session state. Incrementing it changes the key of
# st.text_input, forcing Streamlit to remount it as a fresh widget and clearing
# the input box in a single New Game click instead of requiring two clicks.
if "game_id" not in st.session_state:
    st.session_state.game_id = 0

# Initialize session state for each difficulty
if "games" not in st.session_state:
    st.session_state.games = {}

if difficulty not in st.session_state.games:
    st.session_state.games[difficulty] = {
        "secret": random.randint(low, high),
        "attempts": 0,
        # FIX: Score now initializes at 100 instead of 0 so the progress bar
        # starts full and drains 10% per wrong guess, giving a clear visual
        # representation of performance (10 attempts x 10% = 0% if all wrong).
        "score": 100,
        "history": [],
        "status": "playing",
        "input_value": ""
    }

game = st.session_state.games[difficulty]

# Sidebar info
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {MAX_ATTEMPTS}")

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game now resets ALL difficulties (not just the current one) so
# switching difficulty after clicking New Game always shows a clean state.
# game_id is also incremented here to trigger the text_input remount.
if new_game:
    st.session_state.game_id += 1
    st.session_state.games = {}
    for diff in ["Easy", "Normal", "Hard"]:
        lo, hi = get_range_for_difficulty(diff)
        st.session_state.games[diff] = {
            "secret": random.randint(lo, hi),
            "attempts": 0,
            "score": 100,
            "history": [],
            "status": "playing",
            "input_value": ""
        }
    game = st.session_state.games[difficulty]
    st.info("New game started!")

# FIX: game_id is included in the widget key so Streamlit remounts the input
# fresh on every new game, clearing any leftover text from the previous game.
game["input_value"] = st.text_input(
    "Enter your guess:",
    value=game["input_value"],
    key=f"guess_input_{difficulty}_{st.session_state.game_id}"
)

# FIX: Added game["status"] == "playing" guard so the submit block is completely
# skipped on finished games, preventing phantom attempts when clicking New Game
# on a won/lost game. Also guards against submitting an empty input.
if submit and game["input_value"].strip() != "" and game["status"] == "playing":
    ok, guess_value, err = parse_guess(game["input_value"])
    if not ok:
        st.error(err)
    else:
        valid, range_err = validate_range(guess_value, low, high)
        if not valid:
            st.error(range_err)
        else:
            game["attempts"] += 1
            # FIX: check_guess is always called before history.append so that
            # hint_msg is guaranteed to be defined, preventing a NameError when
            # show_hint is disabled (previously hint_msg was only set inside the
            # if show_hint block, causing a crash when that block was skipped).
            outcome, hint_msg = check_guess(guess_value, game["secret"])
            if show_hint:
                st.warning(hint_msg)
            # FIX: History now stores a dict with the guess and hint separately.
            # hint is captured at submission time — None if show_hint was off —
            # so toggling the checkbox later only affects future guesses, not
            # previously recorded ones.
            game["history"].append({"guess": guess_value, "hint": hint_msg if show_hint else None})
            game["score"] = update_score(game["score"], outcome, game["attempts"])
            if outcome == "Win":
                st.balloons()
                game["status"] = "won"
            elif game["attempts"] >= MAX_ATTEMPTS:
                game["status"] = "lost"
            game["input_value"] = ""

# FIX: Win/loss messages moved here as the single source of truth, outside the
# submit block. Previously they were inside submit which caused duplicate messages
# on the same rerun, and st.stop() was preventing game state from persisting
# correctly when switching difficulty after a finished game.
if game["status"] == "won":
    st.success(f"You won! Secret was {game['secret']}. Final score: {game['score']}%. Start a new game to play again.")
elif game["status"] == "lost":
    st.error(f"Game over! Secret was {game['secret']}. Final score: {game['score']}%. Start a new game to try again.")

# FIX: Attempts used/left captions moved to after the submit block so Streamlit
# renders the updated count on the same rerun as the guess submission. Previously
# this was rendered before submit ran, so it always showed the stale value.
st.sidebar.caption(f"Attempts used: {game['attempts']}")
st.sidebar.caption(f"Attempts left: {MAX_ATTEMPTS - game['attempts']}")

# FIX: Added score health progress bar to the sidebar. Score and health are kept
# in sync (no separate health field needed) since the win bonus was removed.
# Bar starts full at 100% and drains exactly 10% per wrong guess.
st.sidebar.markdown("---")
st.sidebar.caption("🏆 Score Health")
st.sidebar.progress(max(0, game["score"]) / 100)
st.sidebar.caption(f"Score: {game['score']}%")

# FIX: Guess history is now rendered in the UI. Previously history was stored in
# session state but never displayed. Each entry shows the guess number, the value
# entered, and the hint only if show_hint was enabled at the time of submission.
if game["history"]:
    st.markdown("### 📜 Previous Guesses")
    for i, entry in enumerate(game["history"]):
        hint_part = f" — {entry['hint']}" if entry["hint"] is not None else ""
        st.markdown(f"**Guess {i + 1}:** `{entry['guess']}`{hint_part}")