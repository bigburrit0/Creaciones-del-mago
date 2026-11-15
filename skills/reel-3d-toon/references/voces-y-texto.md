# Voices, subtitles and the end card

## Voice cast (Gemini TTS prebuilt voices)

| Character | Voice | Style prompt (summary) |
|---|---|---|
| El Mago | **Charon** (also used in the garden reel; keep it) | kind older wizard from Montevideo, warm and calm, playful smile, a bit mischievous with an idea; natural pace |
| Papá Noel | **Algenib** | big jolly old man on holiday in the Montevideo heat; deep, slightly gravelly, warm; out of breath when tired, belly laugh when happy |

Accent block for every prompt: Rioplatense Spanish from Montevideo (voseo, "sh" for "ll"/"y"). Model:
`gemini-3.8-flash-tts` (also listed: `gemini-3.1-flash-tts-preview`, `gemini-3.8-flash-lite-tts`).

## Process

1. `voces.json`: `{ "<Character>": {"voice", "style", "lines": [[id, text], ...]}, "_edits": {...} }`.
2. `python3 videos/biblioteca/tts_lineas.py voces.json voz/` → `_take_<Character>.wav` (ignored by git),
   `<id>_raw.wav` (cut at the N-1 longest pauses), `<id>.wav` (edited, -16 LUFS, 48 kHz), `durations.json`.
3. Check each line: `python3 videos/biblioteca/check_voces.py clips voz/*.wav` (one request per clip).
4. Fit: `_edits` → `{"to": s}` / `{"from": s}` keeps a span, `{"squeeze": [start, end, new_len]}` shortens a pause;
   then `--post-only` (no API call).
5. Place each line as `<audio id="v-<id>" class="clip" src="assets/voz/<id>.wav" data-start data-duration
   data-track-index data-volume="1" data-who="santa|mago" data-text="...">` (`data-sub="no"` when the card says it).
6. Duck the music in the cues: `[start-0.06, end+0.06, 0.38]` per line.
7. After the render: `check_voces.py mix reel.mp4` → every line "clear".

## Subtitles

- One pill per line, speaker colours: Papá Noel red `#C0392B` with cream text; El Mago purple `#2E2160` with gold
  `#F2C14E`; 6 px dark outline `#150A34`, hard drop shadow; a small name label above ("PAPÁ NOEL", "EL MAGO").
- Fredoka 700, 66 px (label 600, 30 px), centred, max 900 px wide.
- Instagram safe area: nothing in the top 220 px or the bottom 450 px of 1920. The pill's bottom edge sits at y 1450.
- Pop in over 0.16 s with a slight overshoot; out 0.12 s, always before the next line starts; hold 0.3 s after the
  line ends at most.

## End card

- About 3 s, cream card with a dark outline, over the last shot (the character stays visible above it).
- Text: "Regalos impresos en 3D" / "¡Pedí el tuyo!" / "Escribime por mensaje" / "Creaciones del Mago · Montevideo".
- No phone number in the video (it goes in the caption). The character's closing line says the card's text.

## Caption (Instagram)

- First line under ~110 characters, a hook from the reel's funniest image.
- First person singular (the website's voice: "te paso", "entrego", "mando"), Rioplatense.
- Only real facts: price and date by WhatsApp before starting, no commitment; minimum 48 h; free delivery in La Unión,
  La Blanqueada and part of Buceo; ships to all Uruguay; WhatsApp 092 104 419; creacionesdelmago.com.
- 3-4 emojis at most; 5-8 hashtags.
