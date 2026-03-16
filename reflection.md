# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

> When I first ran the game, several behaviors seemed incorrect. The hints were misleading because when a guess was higher than the secret number, the message told the player to “go higher” instead of “go lower.” The difficulty ranges were also inconsistent, since Easy was 1–20, Normal was 1–100, and Hard was 1–50, which made Normal harder than Hard. I also noticed that the UI was confusing because the attempts counter and difficulty changes did not always match the displayed game state. Additionally, the New Game button did not reset all game variables such as score, history, and attempts, which caused inconsistent behavior after restarting the game.

> Concrete Bugs:

  Bug 1: Incorrect hint directions (higher/lower logic)
  Bug 2: Inconsistent difficulty ranges
  Bug 3: New Game button does not fully reset game state

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

> I used ChatGPT and Claude to help analyze the code and understand where the logic errors were occurring. 
> One correct suggestion from AI was identifying that the hint messages were reversed in the check_guess function and needed to be swapped so that “Too High” tells the player to go lower. I verified this by testing several guesses against the secret number and confirming the hints matched the expected behavior. 
> One misleading suggestion occurred when AI recommended changing the difficulty ranges without reviewing how the secret number was generated, which would have caused additional inconsistencies. This showed me that AI suggestions still require careful verification before applying them to the code.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

> To determine whether a bug was fixed, I ran the game manually multiple times and tested guesses that were higher, lower, and equal to the secret number. 
> For example, if the secret number was 50 and the guess was 60, I verified that the game correctly returned “Too High” and the hint instructed the player to go lower. I also ran the pytest tests included in the project to verify that the core game logic behaved correctly after refactoring. 
> AI helped me understand the purpose of the tests and how they validate the check_guess function’s behavior. Using both automated tests and manual testing helped confirm that the fixes were working correctly.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

> I learned that Streamlit reruns the entire script from top to bottom every time the user interacts with the interface, such as clicking a button or entering a guess. Because of this behavior, variables must be stored in st.session_state if they need to persist between interactions. Without using session state correctly, values like the secret number, score, and attempt count can reset or behave inconsistently. I would explain it to a friend by saying that Streamlit apps refresh every time something happens, so session state acts like memory that allows the app to remember important values between interactions.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

> One habit I want to continue using is breaking down debugging problems into small steps and testing each fix individually. I also learned the importance of reviewing AI-generated code carefully instead of assuming it is correct. 
> In the future, I would use AI more strategically by asking it to explain logic before applying changes directly to the code. 
> This project showed me that AI can accelerate development, but human reasoning is still necessary to identify bugs and design reliable solutions.