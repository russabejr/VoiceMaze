# Voice Maze

A maze game using only voice prompts.
The objective is simple:
navigate a ten-room maze using only your voice, collect three keys, and escape.

---

## How to Build and Run

### Dependencies
```bash
pip install pyttsx3 SpeechRecognition pyaudio
```
### Running
```bash
python maze.py
```

---

## How to Play

Speak one of the following commands at any time:

| Command | Action |
|---|---|
| `north` / `south` / `east` / `west` | Move in that direction |
| `look` | Hear your current room and exits again |
| `take` | Pick up a key in the current room |
| `help` | Hear the list of commands again |
| `quit` | Exit the game |

Any phrases that contain the key word will also work:

For example: "go north" or "I want to go east" also work.

---

## Code

### `voice.py`

Handles all speech input and output.

- `speak(text)` — Converts text to speech using pyttsx3. Reinitializes the engine on each call to avoid audio capture being ignored.
- `calibrate()` — Adjusts the recognizer for ambient noise at startup.
- `listen(timeout, phrase_time_limit)` — Records audio and returns recognized text via Google speech recognition.
  - `timeout` is how long the program waits for user input
  - `phrase_time_limit` is the maximum length a user can speak for.
- `ask(prompt)` — Speaks a prompt and immediately listens for a response.

### `maze.py`

Implements the game logic.

- `rooms` — Dictionary of room data. Each room has a description, an exits dictionary, and an (optional) treasure field.
- `TOTAL_TREASURES` — Set of all treasure names required to unlock the exit.
- `interpret(text)` — Parses recognized speech into a game intent.
- `instructions()` — Speaks the full list of commands to the user.
- `describe_room(room, inventory)` — Speaks the room description, any uncollected treasure, and available exits.
- `build_exit_str(exits)` — Formats a list of exits into natural language sentence structure (e.g. "north, east and south").
- `main()` — Game loop. Calibrates mic, runs instructions, and processes player commands until game win or user quit.

---

## Maze Map

```
[ 1 ] --E-- [ 2*] --E-- [ 3*]
  |            |            |
  S            S            S
  |            |            |
[ 4 ] --E-- [ 5*]        [ 6 ]
               |            |
               S            S
               |            |
             [ 8 ] --E-- [ 7 ]
               |
               S
               |
             [ 9 ] --E-- [ WIN ]

* = key room
```

---
## Design Process

I started with the example starter code provided on the [assignment page](https://hwilt.github.io/Ursinus-CS474-Spring2026/Assignments/Programming/VoicePrompt). I played around and tested with how to capture and play audio from TTS. Once I had created my voice methods, I began to work on the game. The game went through many iterations before reaching its final form.

The first version was a simple three room maze with no objectives, just movement. This let me focus purely on getting the voice loop working reliably before adding complexity. From there I expanded the maze to ten rooms and introduced the key collection mechanic, where all three keys must be found before the exit unlocks.

A significant design challenge was deciding how much information to give the player at each step. Early versions just described the room and said nothing else, which I realized could be confusing for some players. After rewriting the game loop several times, I decided always announcing exits at the end of each room description, announcing treasure on entry, and giving spoken feedback for every action including errors was the best way to go. The goal was that a player with no prior knowledge of the game could figure out how to play entirely from what they hear.

---

## Written Questions

**What did you do, how did you did it, and what challenges did you encounter?**

I built a voice-only text adventure game in Python. The player navigates a ten-room maze, collects three keys, and unlocks an exit, all using spoken commands. The main challenge was a pyttsx3 bug where the engine silently failed after the first microphone capture, resulting in audio being unheard. I fixed this by reinitializing the engine inside each `speak()` call.

**Did you work with a buddy?**

No. This submission represents my own original work.

**Portions not originally written by me:**

The base speech recognition template was adapted from Dr. Alvin Grissom's 2020 HCI course and Dr. Bill Mongan's 2024 HCI course, which can be found on the [assignment page](https://hwilt.github.io/Ursinus-CS474-Spring2026/Assignments/Programming/VoicePrompt). All voice input, audio output, and game logic were written by me.

**Approximately how many hours did this take?**

The assignment took approximately 5 hours.

**Overall impression:**

I thought it was really fun to create and design! However, even in the final result the speech recognition is poor, requiring several iterations of the same command.

**Self-assessed grade:**

- **Human-Centric Design (20%):** I would give myself a 100%. The game consistently announces exits and available actions, gives clear feedback for blocked paths, items on the floor, and unknown commands or errors.
- **Design Report (20%):** I would give myself a 100%, as I address everything in the README.
- **Algorithm Implementation (30%):** I would give myself a 100%. The maze, key collection, locked door logic, and win condition all work correctly. Special cases like keys already taken or blocked exits are handled.
- **Code Quality (20%):** I would give myself a 100%. Helper functions are used to avoid repetition, and a clean style was used throughout the code.
- **Writeup and Submission (10%):** I would give myself a 100%. README answers all required questions.