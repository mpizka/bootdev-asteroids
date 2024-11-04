# boot.dev Asteroids

Asteroids game from the boot.dev course [*"Build Asteroids using Python and Pygame"*][course]

- Run `python main.py` to play
- In the main menu <kbd>L</kbd> starts Level, <kbd>E</kbd> starts Endless Mode
- <kbd>Left</kbd> <kbd>Right</kbd> turn the ship
- <kbd>Up</kbd> accelerates
- <kbd>Space</kbd> shoots
- <kbd>Q</kbd> or <kbd>Esc</kbd> exits the game
- <kbd>P</kbd> Pauses and Unpauses the game
- After game over <kbd>M</kbd> gets you back to the menu


### Endless Mode

Asteroids spawn continuously from the edges of the screen. Try to survive as
long as possible! If your ship flies into the void (leaves the screen) or an
asteroid hits it, it's game over!


### Level Mode

You start at Level 1 and progress by destroying all the asteroids. For each
level, 2 large asteroids will spawn at the edges of space. When an asteroid
hits you, it's game over! How far can you go?  Both asteroids and your ship can
go over the edge of the screen to reappear on the other side.

When you finish a level, press <kbd>N</kbd> to progress to the next!


## Versions

Access the desired version by checking out `main` at the indicated tag.

- `v1.0.0` Base version after the Course goal was reached
- `v1.1.0` Code and technical improvements
- `v1.1.1` Gameplay improvements (score display and aceleration)
- `v1.2.0` Graphics update


## Roadmap

Changes planned or already implemented

### Technical improvements

- [x] Exit with <kbd>Q</kbd>
- [x] Cleaning up group-assignment logic
- [x] Replace the asteroid-generation logic
- [x] Track and destroy out-of-screen objects
- [x] Stateful game loop


### New game features

- [x] Acceleration
- [x] Score Display
- [ ] Wrap-Around for ship & asteroids
- [x] Game-Over Screen
- [x] Background image
- [x] Restart
- [x] Pause and Resume


### Graphics

- [x] Sprites for asteroids and spaceship
- [x] Spaceship exhaust while accelerating
- [x] Shot sprites
- [x] EXPLOSIONS!


[course]: https://www.boot.dev/courses/build-asteroids-python
