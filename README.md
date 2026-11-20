# Bad Apple!! in a terminal

`bad-apple.sh` plays the *Bad Apple!!* shadow-art video in a terminal, once for each way a terminal can draw a picture. It starts with crude ASCII line art and moves on through Braille dots, block letters, libcaca, sixel, color emoji and the kitty graphics protocol. Each act runs into the limit of the one before it, so the show doubles as a tour of what your terminal can do.

It was made to demonstrate what [vtium](https://github.com/vtium/vtium) can do on the Linux console. It also runs in desktop terminals. It asks the terminal which image protocols it supports, and where one is missing it shows a placeholder that says so. In kitty, every act plays except the sixel act.

[![A recording of the show, filmed straight off a 7680×2160 screen running vtium](https://img.youtube.com/vi/Gy728LnIpFc/maxresdefault.jpg)](https://www.youtube.com/watch?v=Gy728LnIpFc)

The recording above was filmed straight off the screen. [Watch it on YouTube](https://www.youtube.com/watch?v=Gy728LnIpFc).

## Licences and credits

*Bad Apple!!* is a fan work (original by ZUN, arrangement by Alstroemeria Records feat. nomico, shadow-art video by Anira). The video is never downloaded or committed: you supply your own copy and name it with `BAD_APPLE=/path/to/video`.

- The code, and everything else not named below: MIT ([LICENSE](LICENSE)).
- The original music, the cues in `music/` (their Strudel sources and `.ogg` renderings): CC BY 4.0 ([music/LICENSE](music/LICENSE)).
- The drums mixed into the `.ogg` files: MckAudio's TR-8 recordings, CC0 1.0, fetched from a pinned commit ([Music](#music)).
- The six cat faces in `cats/`: Noto Emoji, Apache License 2.0 ([cats/LICENSE-noto-emoji](cats/LICENSE-noto-emoji)).

The pixel sunglasses (`cats/sunglasses.svg`) were drawn new for the show and are under MIT with the code. Strudel and Playwright are used only to render the music, and are not shipped.

The rule for anything added: every third-party asset is under Creative Commons or another known licence, and nothing NC, ND or unlicensed. The video is never shipped.

## What you need

- Your own copy of the *Bad Apple!!* video.
- A terminal. The image acts need a terminal that supports sixel, the kitty graphics protocol, or both. Sixel is the bitmap image format of DEC's terminals. The [kitty graphics protocol](https://sw.kovidgoyal.net/kitty/graphics-protocol/) sends images to the terminal as escape sequences.
- The programs below. The script installs nothing. `./bad-apple.sh --dry-run` lists any that are missing, with the Arch Linux package that provides each one.

| Program | Arch package | Debian or Ubuntu package | Used by |
|---|---|---|---|
| bash, python3 | bash, python | bash, python3 | every act and effect; Python's standard library only |
| ffmpeg, ffprobe | ffmpeg | ffmpeg | acts 1, 3, 5 and 7: decoding the video, and act 5's glitched clip |
| img2txt | libcaca | caca-utils | act 3 |
| mpv | mpv | mpv | act 5 (`--vo=sixel`); with `--audio`, the soundtrack and the music cues |
| toilet | toilet | toilet | the block letters of acts 2 and 7; without it, figlet's `banner` font, then plain text |
| figlet | figlet | figlet | the fallback for toilet |
| rsvg-convert | librsvg | librsvg2-bin | optional: act 6's interlude in kitty graphics; without it, emoji |
| node, npm, chromium | nodejs, npm, chromium | — | only to render the music cues again (`music/render.mjs`), not to play the show |

## Run it

From a checkout of this repository, in the terminal you want to try:

```sh
BAD_APPLE=/path/to/your/copy ./bad-apple.sh --audio
```

With `--audio`, the show first asks which output the sound plays through. See [Sound](#sound) for details. Then it waits for a key. Press q or Ctrl-C at any point to end the show. It stops its players and restores the cursor, the main screen, the colors and the terminal's modes.

Before the show takes the screen, it renders frame caches for acts 1, 3 and 5 that it has not rendered yet. To render them ahead of time, so that the show starts at once, run:

```sh
BAD_APPLE=/path/to/your/copy ./bad-apple.sh --prepare
```

To play the show on the Linux console with vtium, log in on a VT that runs vtium and run the same command there. See [vtium](https://github.com/vtium/vtium) for how to install and start it.

## What each terminal plays

The show asks the terminal what it supports before the image acts, so the same command works everywhere:

| Terminal | Act 3 | Act 5 | Act 7 |
|---|---|---|---|
| kitty | a framed 80×25 region, because kitty ignores the resize request | a placeholder, because kitty has no sixel | the video, through kitty graphics |
| `xterm -ti vt340` | a real 80×25 grid when `allowWindowOps` is on | sixel | a placeholder, because xterm has no kitty graphics |

In kitty 0.49, act 3 played in its frame, act 5 showed its placeholder, and act 7 played the video. In `xterm -ti vt340`, act 5 played in sixel. In any terminal, the answers to these queries decide what plays:

- **Sixel:** the terminal lists attribute 4 in its reply to the primary device attributes query, DA1 (`CSI c`).
- **Kitty graphics:** the terminal answers a kitty graphics query (`a=q`) with `OK`. The show sends this query just before DA1. A terminal without kitty graphics ignores the query and answers DA1 alone.
- **The resize in act 3:** the terminal resizes itself to 80×25 when asked with xterm's `CSI 8 ; 25 ; 80 t`, within `RESIZE_WAIT` seconds.

`SIXEL=yes|no` and `KITTY=yes|no` override the answers.

The image acts size their pictures in pixels from the character cell size the terminal reports. The show asks for it before each act with XTWINOPS 16 (`CSI 16 t`, the cell size), then XTWINOPS 14 (`CSI 14 t`, the text area's size). Without an answer, it uses the pty's pixel size, and then 10×20. A DA1 query follows the two, so a terminal that answers neither is not waited for and is not asked again.

## The acts

| Act | What plays | Needs |
|---|---|---|
| 1. stick figures | The video as crude ASCII line art: the silhouettes' outlines traced with `- \| / \` on a 27-row grid at 12 frames a second. Then a Braille pass, 2×4 dots in each cell, up to 52 rows tall at 24 frames a second. | ffmpeg, python3 |
| 2. we can do better | Black, a dramatic pause, then "we can do better!" slammed in letter by letter in toilet's `mono12` block letters (▀ ▄ █) in rainbow colors. A half-block plasma fades in behind them, followed by shadebobs. | python3, toilet |
| 3. aalib | "this has got to beat ascii line art... how about ... AALIB?" typed on black, then the video through libcaca's `img2txt` at 80×25. The show asks the terminal for a real 80×25 grid. Where the resize takes effect it plays full screen, and elsewhere in a double-lined 80×25 frame. Then the picture freezes, broken, and a resized terminal is put back to its size. | ffmpeg, img2txt, python3 |
| 4. don't we have libsixel? | "wait a minute... don't we have ... LIBSIXEL?" typed over the frozen frame. | python3 |
| 5. sixel | `mpv --vo=sixel` plays the video at half the screen's height, centered. Then the picture glitches: red channel only, shifted, with a band torn sideways. It halts on its last frame while the sound stutters like a skipping buffer. Without sixel, a panel of static reads "[no sixel: DA1 lacks attribute 4]". | ffmpeg, mpv, python3 |
| 6. kitty and the cats | A fire wipe burns the screen away and uncovers lines of CJK ideographs scrolling up behind the flames. The ideographs fill the screen for two bars, and a wind blows them away. "hold on, we also have kitty. one sec, feeding the cats" is typed, and a crowd of color emoji cats follows. In an interlude, six Noto Emoji cat faces stand in a row in kitty graphics, up to a quarter of the screen's height. Pixel sunglasses drop onto each face, one a beat, and the row slides off the left edge. Without kitty graphics or rsvg-convert, the interlude uses emoji and ⌐■-■. | python3; rsvg-convert for the interlude in kitty graphics |
| 7. kitty, full size | The video through the show's own kitty graphics player for a minute, above a demoscene scroller. The picture and sound fade in over 1.5 s. One copy in the middle slides left with a bounce, then a second copy slides out from behind it, then a third. Each frame is sent once and placed once for each copy. The scroller rides a sine wave over copper bars in toilet's `mono9` block letters, with color emoji between the words. Without kitty graphics, a panel reads "[no kitty graphics: the a=q query got no OK]" above the scroller. | ffmpeg, toilet, python3 |

An end card follows act 7: the credits over a turning Braille wireframe, until you press a key.

The video acts follow the video's own timeline. Act 1 plays from 0:00, and its Braille pass starts at 0:11.3. Act 3 plays from 0:30, act 5 from 0:38, and act 7 from 0:46 to 1:46, where the end card takes over. Act 7's sound fades out over its last two seconds (`ACT7_FADE`).

These times are a cue sheet, `CUES` at the top of `bad-apple.sh`, written in the video's time as m:ss. You can edit them there, and `--list` prints them. A time may carry a fraction, as in `0:54.5`. Acts 2, 4 and 6 play between the cues for their own lengths, each to a music cue of its own. The soundtrack picks up again at the next cue. Delete the `endcard` line to play act 7 to the end of the video.

Act 7's moves are cues as well. Its copy slides left at 0:54 (`act7-slide`), the second copy comes out at 1:02 (`act7-copy2`), and the third at 1:10 (`act7-copy3`). A move whose line you delete never happens.

The scroller's text is one variable, `BANNER_FEATURES` at the top of `bad-apple.sh`. Features are separated by `;`, and each is followed by the next emoji of `BANNER_EMOJI`. `--act 7 --banner-only` runs the scroller alone, without the video.

## Options

```sh
./bad-apple.sh --list                                  # the acts, the effects, what each needs, and the cue sheet
./bad-apple.sh --dry-run [--act N | --from N]          # the plan and the programs each act would use; runs nothing
BAD_APPLE=... ./bad-apple.sh --act 3                   # one act
BAD_APPLE=... ./bad-apple.sh --from 5                  # from act 5 on
./bad-apple.sh --act 7 --banner-only                   # the scroller alone, no video needed
BAD_APPLE=... ./bad-apple.sh --prepare                 # render the frame caches only
./bad-apple.sh --fx plasma                             # one effect alone, with its frame rate
```

`--audio` plays the soundtrack and the music cues. `--no-wait` starts without waiting for a key. Acts 2, 4 and 6, and act 7 with `--banner-only`, run without the video.

mpv's video outputs turn on mouse tracking (`CSI ?1003 h`) and turn it off only when they exit cleanly. So on its way out, the show turns off every mouse mode and encoding, focus events and bracketed paste. While mpv plays, the show drops a mouse report that arrives as keys once the report is complete, even when it arrives split across reads. This keeps a byte of the report's coordinates from being taken for q.

## Sound

With `--audio`, before the show takes the screen, `pick-audio.sh` asks where the sound plays. It lists the outputs that `mpv --audio-device=help` finds. With a sound server running, it lists the server's outputs, PipeWire's before PulseAudio's, with the server's default first. Without a sound server, it lists each ALSA card's default and HDMI devices. `0` means no sound. A server with no sink except its dummy (`auto_null`) counts as none.

When you pick a number, the picker plays a one-second 660 Hz tone through that output. Then `y` keeps the output, `t` plays the tone again, and any other answer asks again. You can also type an mpv device name in place of the number.

`AUDIO_DEVICE=NAME` answers the question in advance, with an mpv device name or `none`. With `--no-wait`, nothing is asked and the sound plays through mpv's default output, so `AUDIO_DEVICE` is how you pick an output for an unattended run. Nothing is asked when no act in the run plays sound, as with `--act 7 --banner-only`.

On a VT login without a logind session, the sound cards (`/dev/snd`) may be out of reach while that VT is on screen. Joining the `audio` group gives your user access to the sound cards on every VT: run `sudo usermod -aG audio $USER`, then log out of every session or reboot. The picker says when this is the problem, and offers what still plays. A desktop session, or a login on a VT that logind manages, needs no group.

### Music

Where the video's soundtrack does not play, the show plays music of its own. The music is original, written for the show in [Strudel](https://strudel.cc) and rendered to Opus in `music/`. It is in the soundtrack's key and tempo (E♭ minor, 138 BPM), so each cue hands back to the video without a jolt.

| Cue | Plays | Length |
|---|---|---|
| `act2-better` | act 2: a riser through the pause, a rising blip and tom for each letter, and a slam on the "!". Then a 909 groove, bass and arpeggio under the plasma, a gliding saw lead over the shadebobs, and a last hit | 10 bars and a ring |
| `act3-aalib` | act 3's opening line: a soft square-wave arpeggio, a question after the "...", and a run up to a chime on AALIB and a build into the video | 4.5 bars, 7.8 s of typing |
| `act4-minute` | act 4: a tape stop, a ticking clock and a sneaking bass, a question after each "...", and a B♭ chime on LIBSIXEL with a half-bar build into act 5 | 4.5 bars, 7.8 s of typing |
| `act6-fire` | act 6's fire and CJK stream: rumble, crackle and an arpeggio that doubles its speed each bar, and data bleeps as the stream rises. A hit as the fire goes out, two driving bars under the full-screen stream, a stop as it clears, then a music box in G♭ major under the typing | 5 bars, then until the cats |
| `act6-cats` | the cats: a square-wave tune in G♭ major whose long notes meow, a bloop for each cat, and a run up to D♭ into the interlude | 5 bars and a ring |
| `act6-shades` | the interlude: a bloop as each face pops in, and a slide whistle, a synth meow and a click for each pair of sunglasses, over a half-time beat. A major seventh once all six are on, then a gust over B♭ as the row slides off and act 7 fades in | 4 bars |
| `endcard` | the end card: pad, arpeggio, half-time drums and a lead that glides and bends, looped until the key | 16 bars, looped |

The acts' timings fall on their cues' beats, and each timing is a variable at the top of `bad-apple.sh`. A cue starts just before what it plays under, and the act waits `CUE_LATENCY` (0.1 s) before it draws. Each cue stops the one before it, and the soundtrack stops a cue that is still ringing.

To change a cue, edit its `.js` file and render it again:

```sh
cd music && npm install && node render.mjs act2-better.js   # or no file: every cue
```

A cue also plays on strudel.cc once the drums are loaded there: run `samples(...)` with the map and base that `render.mjs` builds from its `DRUMS`.

`render.mjs` runs Strudel's own offline renderer (`renderPatternAudio` from `@strudel/web`) in headless Chromium. It uses `/usr/bin/chromium`, or the path in `CHROMIUM=`. The drums are a Roland TR-8's 909 voices, recorded one hit at a time by MckAudio and dedicated to the public domain under CC0 1.0 ([MckAudio/MckSamplePacks](https://github.com/MckAudio/MckSamplePacks), `TR8/`, its top-level `LICENSE`). They are fetched from `https://raw.githubusercontent.com/MckAudio/MckSamplePacks/5db40e8fe26785c256845a5bb38921b2654a887f/TR8/`. A cue plays them as the bank `tr8`.

`render.mjs` cuts each recording 30 ms after it falls to its noise floor, and sets each sound's level to that of the 909 sample it replaced. Each cue's header names its tempo, bars, tail and whether it loops. A loop is rendered twice and the second pass is kept, so it starts with its own reverb and loops without a seam. ffmpeg brings each cue to -8 LUFS (`LUFS=`) under a limiter 2 dB down and encodes Opus at 160 kb/s. Node, npm and Chromium are needed only to render; the show plays the `.ogg` files.

## Settings

The cue sheet sets where each video act starts and stops. Every other timing is a variable at the top of `bad-apple.sh`, with a comment that says what it does. You can edit each variable there or set it in the environment for one run. Times are in seconds.

| Variable | Default | What it sets |
|---|---|---|
| `ACT1_START`, `ACT1_SECONDS`, `ACT1_DOTS_SECONDS`, `ACT3_START`, `ACT3_SECONDS`, `ACT5_START`, `ACT5_SECONDS`, `ACT7_START`, `ACT7_SECONDS` | from the cue sheet | where each video act starts in the video, and how long it plays |
| `ACT1_FPS`, `ACT1_ROWS`, `ACT1_DOTS_FPS`, `ACT1_DOTS_ROWS` | 12, 27, 24, 52 | act 1's frame rates and grid heights |
| `ACT2_PAUSE`, `ACT2_LETTER`, `ACT2_HOLD`, `ACT2_PLASMA`, `ACT2_FADE`, `ACT2_BOBS` | 2.065, 0.1087, 1.630, 6.957, 1.739, 5.217 | act 2's pause, letter speed, hold, plasma, fade-in and shadebobs |
| `ACT3_RESIZE`, `RESIZE_WAIT` | auto, 1.5 | whether act 3 asks for a real 80×25 grid (`no` keeps the frame), and how long it waits for the terminal |
| `ACT3_CPS`, `ACT3_DOTS`, `ACT3_HOLD`, `ACT4_CPS` | 14, 0.9, 1, 14 | the typing speed and pauses of acts 3 and 4 |
| `ACT5_SIZE`, `ACT5_WIDTH`, `ACT5_DITHER`, `ACT5_GLITCH`, `ACT5_STUTTER`, `ACT5_HOLD` | 0.5, 960, none, 2, 2, 0.5 | act 5's share of the screen's height, the clip's width in pixels, mpv's sixel dither, and the glitch, stutter and hold |
| `ACT6_FIRE`, `ACT6_CJK`, `ACT6_WIND`, `ACT6_CATS` | 5.217, 3.478, 1.739, 8.696 | the fire, the full-screen CJK stream, the wind and the cats |
| `ACT7_FADE_IN`, `ACT7_FADE` | 1.5, 2 | act 7's fade-in and fade-out |
| `ACT7_SLIDE_AT`, `ACT7_COPY2_AT`, `ACT7_COPY3_AT` | from the cue sheet | act 7's moves, in seconds into the act |
| `ACT7_MOVE`, `ACT7_BOUNCE`, `ACT7_GAP` | 1.2, 0.12, 2 | how long each slide takes, how far past its place a copy swings (as a share of the slide), and the columns between copies |
| `KITTY_TRANSPORT`, `KITTY_WIDTH` | png, 0 | how act 7's player sends frames, and the width it decodes them at. See [Act 7's player](#act-7s-player). |
| `ACT7_REPORT` | none | a file that act 7's player appends its frame rate to |
| `BANNER_ROWS`, `BANNER_FPS`, `BANNER_FEATURES`, `BANNER_EMOJI`, `BANNER_INTRO`, `BANNER_OUTRO` | 12, 40, ... | the scroller's rows, frame rate and words |
| `PLACEHOLDER_SECONDS` | 6 | how long a placeholder in act 5 or 7 stays |
| `CUE_LATENCY` | 0.1 | how long an act waits for its music cue's sound to start |
| `TITLE_SECONDS` | 0 | an optional starfield title card before act 1 |
| `SIXEL`, `KITTY` | auto | `yes` or `no` overrides the terminal's answer |
| `PROBE_TIMEOUT` | 1 | how long the show waits for the terminal's answers |
| `FX_SECONDS` | 10 | how long `--fx` runs |
| `SHOWCASE_CACHE` | `~/.cache/kmscon-showcase` | where the frame caches go |

## The effects

The effects draw with half blocks or Braille. A half block (▀ with a 24-bit foreground and background color) makes each cell two pixels. A Braille character makes each cell 2×4 dots in one color. The painters remember the last frame and send only the cells that changed. Each frame goes to the terminal in one `write()`. On a resize, the effect is rebuilt at the new size.

| `--fx` | Where it plays | Drawn with |
|---|---|---|
| `plasma` | act 2, behind the letters | half blocks: two sine fields and a cycling palette of 64 colors |
| `shadebobs` | act 2, after the plasma | half blocks: blurred blobs on Lissajous paths, added into a buffer that fades, so brightness piles up where they cross |
| `fire` | the wipe into act 6 | half blocks: the classic fire, its source on an edge that climbs the screen and chars what it touches. With `--cjk SECONDS`, CJK lines scroll up behind it in a scroll region and then fill the screen for that long |
| `copper` | act 7, under the scroller | half blocks: raster bars over a dark gradient |
| `stars` | the title card before act 1 | half blocks: a starfield behind the title in big letters |
| `braille` | behind the end card | Braille: a turning torus over an oscilloscope trace |
| `banner` | act 7's scroller | half blocks and emoji: the sine scroller over copper bars |

`--fx NAME` runs one effect alone for `FX_SECONDS` and then prints its frames per second and bytes per frame. That makes the effects a text throughput benchmark for a terminal. All but the plasma are paced to 40 frames a second. The plasma runs as fast as the terminal takes it, so its frame rate measures the terminal.

## Act 7's player

`kitty.py` plays act 7. It is written from the kitty graphics protocol's published specification alone. ffmpeg decodes the clip at a copy's own pixel size, at most 2160 pixels tall. The player transmits each frame once (`a=t`) and places it up to three times (`a=p`, placement ids 1 to 3) in each copy's cells.

A copy moves when the player places it again under its placement id at another column, so nothing is sent again. The frames alternate between two image ids, because sending an image id again deletes that image's placements. The player transmits a frame to one id, places its copies, and deletes the other id with `d=I`, all in one write. The terminal never holds more than two of the player's images, and a copy is never without its picture. Every command carries `q=2`, so the terminal sends no replies into the show's input, and every placement carries `C=1`, so the cursor stays put.

The player encodes each frame itself, so large copies cost more on a slow machine. A number in `KITTY_WIDTH` limits that work: the player decodes frames that many pixels wide, and the terminal scales them up.

`KITTY_TRANSPORT` chooses how the frames travel:

| Transport | What travels | Bytes a frame at 480×360 |
|---|---|---|
| `raw` | `f=24` RGB inline, base64 in 4096-byte chunks | 693,600 |
| `zlib` | the same, compressed with zlib (`o=z`) | about 31,400 |
| `png` (default) | `f=100`, an 8-bit grayscale PNG that the player makes. The protocol has no grayscale raw format, and PNG is its compact form | about 17,800 |
| `shm` | `f=24` RGB in a POSIX shared memory object (`t=s`), a new name each frame, which the terminal reads and unlinks | about 260 |

With `shm`, the player first sends a one-pixel `a=q` query, and falls back to `png` when the terminal refuses shared memory. While the frames the terminal has yet to read hold 64 MB, the player drops frames rather than send more.

With `--audio`, the frames follow the soundtrack. The player reads mpv's position (`time-pos`) over mpv's IPC socket four times a second and shows the frame for that moment, dropping the frames it is late for. The socket sits in `XDG_RUNTIME_DIR`, or in `/tmp` when that directory is missing or not writable. If mpv has not answered within 3 s, the player follows a wall clock from the moment the soundtrack started, and says so once the screen is back. Without sound, the player runs on its own clock. q ends the player even when the terminal has fallen behind. SIGTERM and SIGHUP end it as Ctrl-C does: it deletes its images and unlinks its shared memory.

## Files

| File | What it holds |
|---|---|
| `bad-apple.sh` | the acts (`act_1` to `act_7`), the act and effect tables, the cue sheet and settings, the terminal queries, and the clean exit |
| `fx.py` | the drawing commands that `bad-apple.sh` runs |
| `screen.py` | output, keys, the window size and resizes, colors, and the half-block and Braille painters |
| `effects.py` | plasma, shadebobs, fire, copper, stars, the Braille wireframe, and the runner that draws one effect alone |
| `scenes.py` | act 2's letters over the effects, act 7's scroller, typing, placeholders, the cats and the end card |
| `letters.py` | toilet's and figlet's letters read back into pixels |
| `frames.py` | the video acts' frame caches (outlines, Braille and libcaca) and their player |
| `kitty.py` | act 7's player: the kitty graphics commands, the transports, the copies' layout and moves, and the soundtrack's clock |
| `shades.py` | act 6's interlude, the cats in sunglasses, in kitty graphics, and its emoji fallback |
| `cats/` | the interlude's images: six Noto Emoji cat faces (`emoji_u*.svg`, from googlefonts/noto-emoji `2D/svg`, under the Apache License 2.0 that `2D/svg/LICENSE` names, its text in `LICENSE-noto-emoji`; the OFL in noto-emoji's top-level `LICENSE` covers its fonts) and pixel sunglasses (`sunglasses.svg`, drawn new for the showcase by a Claude session at the operator's request) |
| `music/` | the music cues: each cue's Strudel source (`.js`) and its rendering (`.ogg`), and `render.mjs`, which renders them |
| `pick-audio.sh` | the sound output picker |
| `ideographs.py` | the pool of ideographs for the CJK stream |
| `tests/showcase.py` | the tests |

The frame caches go to `~/.cache/kmscon-showcase/<video id>/`, and `SHOWCASE_CACHE` moves them. A cache is keyed by the video's path, size and modification time, and by each act's settings. A cache made for one grid size is not reused for another: act 1's grids and act 3's framed region shrink in a smaller terminal and render again there.

## Tests

`tests/showcase.py` needs none of the media programs and no video. CI runs it on every push and pull request:

```sh
python3 tests/showcase.py --root .
```

It checks the act and effect tables, the plan, the refusals and the pure helpers. It quits act 4 on a pty to check that every mouse mode, focus events and bracketed paste are turned off. It replays act 7's player in every transport on a model of the protocol's image store, with stand-ins for ffmpeg, ffprobe and mpv. It also runs act 6's interlude on a pty with a stand-in for rsvg-convert, and checks that every image is deleted at the end and on SIGTERM and SIGHUP.
