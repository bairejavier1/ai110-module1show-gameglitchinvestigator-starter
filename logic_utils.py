import random

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100

def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
        return True, value, None
    except ValueError:
        return False, None, "That is not a number."

def validate_range(guess: int, low: int, high: int):
    """Check if the guess is within the allowed range."""
    if guess < low or guess > high:
        return False, f"Number must be between {low} and {high}."
    return True, None

def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    elif guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"

# FIX: Removed win bonus logic entirely. Previously the function added a speed
# bonus on a win (100 - 10 * attempts) which inflated the score above 100 and
# made the progress bar meaningless — e.g. 7 wrong guesses followed by a win
# would push the score well above 30%, misrepresenting actual performance.
# Score now simply drains 10% per wrong guess and freezes on a win, so the
# final score honestly reflects how many wrong guesses the player made.
# FIX: Penalty changed from -5 to -10 to align with the progress bar logic:
# 10 attempts x 10% = bar fully drains to 0% if all attempts are used up.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome.
    - Each wrong guess: -10 (10 attempts x 10% = bar fully drains if all wrong).
    - On a win: no bonus. Final score is simply whatever health remains.
    """
    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 10
    return current_score