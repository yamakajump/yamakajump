## Corentin Batard

Independent developer on the French Atlantic coast. I run [CodWingz](https://codwingz.com),
a one-person software company, which means I write the code, run the servers, answer the
support mail and send the invoices.

Most of my work is closed source, so this profile is a slice rather than the whole thing.
Here is the honest map.

### What I ship

**[Tifox](https://tifox-maternelle.fr)** is a progress-book SaaS for French preschool
teachers. They photograph what a child achieved, tick the matching skill from the national
curriculum, and get a print-ready PDF at the end of the term instead of an evening of
paperwork. Flutter on Android and iOS, Laravel 11 API, React front, all three live.

**Brainy** is an AI accountability companion. It remembers who you are, structures your
goals, and comes after you when you drift. Flutter, Laravel, streaming LLM chat.

Both are private repositories. The code that pays rent does not go on GitHub.

### What is public

**[mindustry-ai](https://github.com/yamakajump/mindustry-ai)** is where the interesting
problem is. Mindustry is a factory-building tower defense game, and winning it needs three
things that rarely appear together: long-horizon economics, spatial reasoning on a grid, and
reactive combat. Factorio has a learning environment. StarCraft II has pysc2. Mindustry had
nothing, so I am building it: a JVM mod that exposes game state, a Gymnasium environment on
top, and a replay viewer that renders training runs inside the real game client.

**[EDT-discord-bot](https://github.com/yamakajump/EDT-discord-bot)** runs a French fitness
community. Members upload their gym export, the bot turns it into heatmaps and streaks,
computes their nutrition and one-rep-max numbers, and promotes them through roles as they
show up. Around fifty slash commands, MySQL, Docker, deployed by GitHub Actions.

**[discord-bot-template](https://github.com/yamakajump/discord-bot-template)** is the
skeleton underneath all of that, extracted so the next bot starts at hour zero instead of
week one. Nested commands, buttons, modals, select menus and a MySQL DAO layer, all loaded
dynamically from the filesystem.

The **Basic-Fit suite** ([launcher](https://github.com/yamakajump/Basicfit_discord-bot),
[coach](https://github.com/yamakajump/Basicfit-Coach_discord-bot),
[manager](https://github.com/yamakajump/Basicfit-Manager_discord-bot),
[security](https://github.com/yamakajump/Basicfit-Securite_discord-bot)) came first, three
bots split by concern and held together by git submodules.

### Stack

Dart and Flutter for mobile. PHP and Laravel for APIs. TypeScript and React for the web.
Node and Python for everything else. MySQL, Docker, GitHub Actions, and servers I administer
myself: a Proxmox box at home for development, a VPS in production.

### Reach me

[codwingz.com](https://codwingz.com) · corentin@codwingz.com
