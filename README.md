# boot.dev Asteroids

Asteroids game from the boot.dev course [*"Build Asteroids using Python and Pygame"*][course]

- Run `python main.py` to play
- Chose a game-mode from the main menu
- <kbd>Left</kbd> <kbd>Right</kbd> turn the ship
- <kbd>Up</kbd> accelerates
- <kbd>Space</kbd> shoots
- <kbd>Q</kbd> exits the game or goes back to the main menu
- <kbd>P</kbd> pauses/unpauses the game


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


### Taurus Mode

In this variant of [Endless Mode](#endless-mode), you take control of the
mighty *Taurus-Class Mobile Defense Platform* to protect the terran sector from
asteroids!

The Taurus doesn't turn, but can accelerate in any direction due to its
multi-thruster array. Its many gun-emplacements allow it to fire in any
direction, and the large onboard-reactor can even power the mighty *Mjolnir
Defense Cannon*.

You control movement with the Arrow-Keys or <kbd>WASD</kbd> and fire using the
mouse. <kbd>Mouse-LEFT</kbd> fires the normal plasma gun,
<kbd>Mouse-RIGHT</kbd> fires the Mjolnir Cannon on a 5 second cooldown.


## Versions

Access the desired version by checking out `main` at the indicated tag.

- `v1.0.0` Base version after the Course goal was reached
- `v1.1.0` Code and technical improvements
- `v1.1.1` Gameplay improvements (score display and aceleration)
- `v1.2.0` Graphics update
- `v1.2.1` Level-Mode and Menus
- `v1.2.2` Better font and Taurus-Class player ship


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
- [x] Wrap-Around for ship & asteroids
- [x] Game-Over Screen
- [x] Background image
- [x] Restart
- [x] Pause and Resume
- [x] New ship available
- [ ] New asteroid classes
    - [ ] Magnetite
    - [ ] Titanium
    - [ ] Black Hole
- [ ] Better Endless Mode rules
- [ ] Ship selection


### Graphics

- [x] Sprites for asteroids and spaceship
- [x] Spaceship exhaust while accelerating
- [x] Shot sprites
- [x] EXPLOSIONS!
- [x] Better font


## License

Licensed under "The Unlicense". For more information, see [LICENSE](./LICENSE)


## Attributions

This Project uses the following amazing open source projects:

Monogram font by Vinícius Menézio - https://datagoblin.itch.io/monogram

For more information, see [NOTICE.txt](./NOTICE.txt)


[course]: https://www.boot.dev/courses/build-asteroids-python
