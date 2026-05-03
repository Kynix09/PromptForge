# PromptForge

**PromptForge** is a local terminal app for generating **Stable Diffusion prompts** with **Ollama**.

It converts a simple image idea into:

- **POSITIVE prompt**
- **NEGATIVE prompt**
- **Model-specific prompt style**
- **Stable Diffusion-ready text**
- **Clipboard-copyable output**

PromptForge runs locally through Ollama.

---

## Preview

![Home screen](https://github.com/Kynix09/PromptForge/blob/d845d2a3a590f98a1978f87ca39345b5ec9a254c/Images/01-home-screen.png?raw=true)

![LLM selector](https://github.com/Kynix09/PromptForge/blob/d845d2a3a590f98a1978f87ca39345b5ec9a254c/Images/02-select-llm.png?raw=true)

![Image model selector](https://github.com/Kynix09/PromptForge/blob/d845d2a3a590f98a1978f87ca39345b5ec9a254c/Images/03-select-image-model.png?raw=true)

![Generating prompt](https://github.com/Kynix09/PromptForge/blob/d845d2a3a590f98a1978f87ca39345b5ec9a254c/Images/04-generating-prompt.png?raw=true)

![Result output](https://github.com/Kynix09/PromptForge/blob/d845d2a3a590f98a1978f87ca39345b5ec9a254c/Images/05-result-output.png?raw=true)

![Doctor screen](https://github.com/Kynix09/PromptForge/blob/d845d2a3a590f98a1978f87ca39345b5ec9a254c/Images/06-doctor-check.png?raw=true)
---

## Features

- **Claude Code-style terminal interface**
- **Automatic Ollama model detection**
- **LLM models sorted largest to smallest**
- **Image checkpoint selection**
- **Custom checkpoint input**
- **Model-specific system prompt adaptation**
- **Positive and negative prompt output**
- **Clipboard support**
- **Doctor command for checking Ollama**
- **Easy source-code customization**

---

## Requirements

- **Python 3.10+**
- **Ollama**
- **colorama**
- At least one installed Ollama model

Install Python dependency:

```bash
pip install colorama
```

Install an Ollama model:

```bash
ollama pull qwen2.5:7b-instruct
```

Start Ollama:

```bash
ollama serve
```

Run PromptForge:

```bash
python promptforge.py
```

---

## Basic Usage

Start the app:

```bash
python promptforge.py
```

Choose an Ollama LLM model.

Choose an image checkpoint.

Type an image idea:

```text
> cinematic photo of a fantasy castle on a snowy mountain at sunset
```

PromptForge returns:

```text
POSITIVE:
...

NEGATIVE:
...
```

Copy options:

```text
1 positive
2 negative
3 both
Enter skip
```

---

## Commands

| Command | Action |
|---|---|
| `/llm` | Change Ollama LLM model |
| `/img` | Change image checkpoint |
| `/clear` | Redraw interface |
| `/doctor` | Check Ollama status |
| `/help` | Show help |
| `?` | Show help |
| `/bye` | Exit |
| `exit` | Exit |
| `quit` | Exit |

---

## Project Structure

```text
PromptForge/
├─ promptforge.py
├─ README.md
└─ images/
   ├─ 01-home-screen.png
   ├─ 02-select-llm.png
   ├─ 03-select-image-model.png
   ├─ 04-generating-prompt.png
   ├─ 05-result-output.png
   └─ 06-doctor-check.png
```

---

# Editing PromptForge

Most customization happens in:

```text
promptforge.py
```

Main editable sections:

| Code section | Purpose |
|---|---|
| `APP_NAME` | App name |
| `APP_VERSION` | App version |
| `IMAGE_MODELS` | Image checkpoint menu |
| `SYSTEM_PROMPT` | Prompt-generation rules |
| Theme colors | UI colors |
| `PF_LOGO` | Terminal logo |
| `header_home()` | Home screen text |
| `choose_image_model()` | Image model menu logic |
| `discover_ollama_models()` | Ollama model detection |
| `ask_ollama()` | Ollama request settings |
| `copy_menu()` | Clipboard menu |
| `doctor()` | Diagnostic screen |
| `main()` | Commands and app loop |

---

## Change App Name

Find:

```python
APP_NAME = "PromptForge"
APP_VERSION = "v1.0.0"
```

Change to:

```python
APP_NAME = "YourAppName"
APP_VERSION = "v1.1.0"
```

---

## Change Theme Colors

Find:

```python
ORANGE      = "\033[38;2;255;146;43m"
ORANGE_DIM  = "\033[38;2;196;96;28m"
AMBER       = "\033[38;2;255;185;80m"
GOLD        = "\033[38;2;255;204;102m"
BORDER      = "\033[38;2;184;101;43m"
MUTED       = "\033[38;2;145;130;115m"
SOFT        = "\033[38;2;220;180;130m"
PANEL       = "\033[38;2;235;150;72m"
```

Color format:

```text
\033[38;2;R;G;Bm
```

Examples:

```python
ORANGE = "\033[38;2;255;120;20m"
BORDER = "\033[38;2;120;70;35m"
MUTED = "\033[38;2;130;130;130m"
```

---

## Change PF Logo

Find:

```python
PF_LOGO = [
    "██████╗ ███████╗",
    "██╔══██╗██╔════╝",
    "██████╔╝█████╗  ",
    "██╔═══╝ ██╔══╝  ",
    "██║     ██║     ",
    "╚═╝     ╚═╝     ",
]
```

Replace with your own logo.

Keep the logo width small so the box layout does not break.

---

## Change Home Screen Text

Find this inside `header_home()`:

```python
right_lines = [
    f"{GOLD}{B}Tips for getting started{RST}",
    f"{SOFT}Type your image idea and press Enter.{RST}",
    f"{SOFT}Use /img to swap checkpoints, /llm to swap writing models.{RST}",
    f"{BORDER}────────────────────────────────────────────{RST}",
    f"{GOLD}{B}What's new{RST}",
    f"{SOFT}Claude Code style terminal layout.{RST}",
    f"{SOFT}Automatic Ollama model detection.{RST}",
    f"{SOFT}LLM menu sorted largest to smallest.{RST}",
]
```

Example replacement:

```python
right_lines = [
    f"{GOLD}{B}PromptForge{RST}",
    f"{SOFT}Write an image idea and press Enter.{RST}",
    f"{SOFT}Use /img for checkpoints and /llm for LLMs.{RST}",
    f"{BORDER}────────────────────────────────────────────{RST}",
    f"{GOLD}{B}Local generation{RST}",
    f"{SOFT}Powered by Ollama.{RST}",
    f"{SOFT}Outputs positive and negative prompts.{RST}",
    f"{SOFT}Ready for Forge, WebUI, or ComfyUI.{RST}",
]
```

---

# Image Models

Image models are controlled here:

```python
IMAGE_MODELS = {
    "1": ("Lustify_v8_Apex.safetensors",                           "Lustify V8 Apex · photoreal SDXL"),
    "2": ("oneObsessionHybridTheoryNoobAIIllustrious.safetensors", "OneObsession HybridTheory · NoobAI Illustrious anime"),
    "3": ("Custom",                                                 "Enter your own checkpoint name"),
}
```

Format:

```python
"menu number": ("checkpoint filename", "menu description"),
```

Example:

```python
"1": ("myModel.safetensors", "My Model · short description"),
```

The checkpoint filename is sent to the LLM.

The menu description is only shown in the terminal.

---

## Add an Image Model

Before:

```python
IMAGE_MODELS = {
    "1": ("Lustify_v8_Apex.safetensors",                           "Lustify V8 Apex · photoreal SDXL"),
    "2": ("oneObsessionHybridTheoryNoobAIIllustrious.safetensors", "OneObsession HybridTheory · NoobAI Illustrious anime"),
    "3": ("Custom",                                                 "Enter your own checkpoint name"),
}
```

After adding RealVisXL:

```python
IMAGE_MODELS = {
    "1": ("Lustify_v8_Apex.safetensors",                           "Lustify V8 Apex · photoreal SDXL"),
    "2": ("oneObsessionHybridTheoryNoobAIIllustrious.safetensors", "OneObsession HybridTheory · NoobAI Illustrious anime"),
    "3": ("realvisxlV50.safetensors",                              "RealVisXL V5.0 · realistic SDXL"),
    "4": ("Custom",                                                 "Enter your own checkpoint name"),
}
```

Update the tags in `choose_image_model()`:

```python
tags = {
    "1": "photoreal",
    "2": "anime",
    "3": "realistic",
    "4": "custom",
}
```

Update the custom option logic.

Change:

```python
if choice in IMAGE_MODELS and choice != "3":
```

to:

```python
if choice in IMAGE_MODELS and choice != "4":
```

Change:

```python
if choice == "3":
```

to:

```python
if choice == "4":
```

---

## Better Custom Option Logic

Add this above `choose_image_model()`:

```python
def custom_image_model_key() -> str | None:
    for key, (model, _desc) in IMAGE_MODELS.items():
        if model.lower() == "custom":
            return key
    return None
```

Then use this inside `choose_image_model()`:

```python
custom_key = custom_image_model_key()
valid = ", ".join(IMAGE_MODELS.keys())

while True:
    choice = prompt_line()

    if choice in IMAGE_MODELS and choice != custom_key:
        return IMAGE_MODELS[choice][0]

    if choice == custom_key:
        print()
        name = prompt_line("checkpoint name")

        if name:
            return name

        print(f"\n  {RED}✗{RST} {MUTED}Checkpoint name cannot be empty.{RST}\n")
        continue

    print(f"\n  {RED}✗{RST} {MUTED}Enter one of: {valid}.{RST}\n")
```

This lets you move `Custom` anywhere in `IMAGE_MODELS`.

---

# System Prompt

The system prompt controls how prompts are written.

Find:

```python
SYSTEM_PROMPT = r"""
...
""".strip()
```

Only edit the text inside the triple quotes.

Do not remove:

```python
SYSTEM_PROMPT = r"""
```

Do not remove:

```python
""".strip()
```

---

## Recommended System Prompt Structure

```text
You are a professional Stable Diffusion prompt generator.

OUTPUT FORMAT
...

GENERAL RULES
...

SAFETY / SUBJECT RULES
...

NEGATIVE PROMPT RULES
...

MODEL ADAPTATION
...

MODEL DETECTION
...

FINAL CHECK
...
```

---

## Output Format

The app expects:

```text
POSITIVE:
[positive prompt]

NEGATIVE:
[negative prompt]
```

The parser depends on:

```text
POSITIVE:
NEGATIVE:
```

Do not rename these labels unless you update `split_prompt()`.

---

## Parser

Current parser:

```python
def split_prompt(text: str) -> tuple[str, str]:
    if "POSITIVE:" in text and "NEGATIVE:" in text:
        after_pos = text.split("POSITIVE:", 1)[1]
        pos, neg = after_pos.split("NEGATIVE:", 1)
        return pos.strip(), neg.strip()

    return text.strip(), ""
```

If you add a `SETTINGS:` section, use a new parser:

```python
def split_prompt_with_settings(text: str) -> tuple[str, str, str]:
    positive = ""
    negative = ""
    settings = ""

    if "POSITIVE:" in text and "NEGATIVE:" in text:
        after_pos = text.split("POSITIVE:", 1)[1]
        pos, after_neg = after_pos.split("NEGATIVE:", 1)
        positive = pos.strip()

        if "SETTINGS:" in after_neg:
            neg, set_text = after_neg.split("SETTINGS:", 1)
            negative = neg.strip()
            settings = set_text.strip()
        else:
            negative = after_neg.strip()

    return positive, negative, settings
```

---

## Model Detection

PromptForge sends the selected checkpoint name to the LLM.

Example:

```text
Image model/checkpoint: Lustify_v8_Apex.safetensors
```

The system prompt detects style with rules like:

```text
If the selected image model name contains any of these words:
Lustify, lustify, Apex, photoreal
then use the Lustify style.
```

Good checkpoint names:

```text
Lustify_v8_Apex.safetensors
oneObsessionHybridTheoryNoobAIIllustrious.safetensors
realvisxlV50.safetensors
ponyDiffusionV6XL.safetensors
juggernautXL.safetensors
dreamshaperXL.safetensors
```

Bad checkpoint names:

```text
model1.safetensors
test.safetensors
new.safetensors
abc.safetensors
```

If a checkpoint has a bad name, add that exact name to `MODEL DETECTION`.

---

## Add Pony Diffusion Style

Add to `IMAGE_MODELS`:

```python
IMAGE_MODELS = {
    "1": ("Lustify_v8_Apex.safetensors",                           "Lustify V8 Apex · photoreal SDXL"),
    "2": ("oneObsessionHybridTheoryNoobAIIllustrious.safetensors", "OneObsession HybridTheory · NoobAI Illustrious anime"),
    "3": ("ponyDiffusionV6XL.safetensors",                         "Pony Diffusion V6 XL · score-tag style"),
    "4": ("Custom",                                                 "Enter your own checkpoint name"),
}
```

Update tags:

```python
tags = {
    "1": "photoreal",
    "2": "anime",
    "3": "pony",
    "4": "custom",
}
```

Add to `SYSTEM_PROMPT` under `MODEL ADAPTATION`:

```text
3. PONY DIFFUSION / Pony XL

This is a Pony-style SDXL model that responds well to score tags and comma-separated booru-style prompts.

For Pony:
- Use comma-separated tags.
- Start with quality score tags.
- Use score_9, score_8_up, score_7_up when appropriate.
- Use clear subject, pose, outfit, background, lighting, and composition tags.
- Do not write long paragraphs.
- Avoid photoreal camera language unless the user asks for realistic style.

Pony positive prompt structure:
score_9, score_8_up, score_7_up, [subject], [appearance], [pose/action], [clothing], [environment], [lighting], [composition], detailed, high quality

Pony negative prompt structure:
score_4, score_5, score_6, low quality, worst quality, bad anatomy, bad hands, extra fingers, missing fingers, text, watermark, logo, blurry, jpeg artifacts
```

Add to `MODEL DETECTION`:

```text
If the selected image model name contains any of these words:
Pony, pony, ponyDiffusion, score_
then use the Pony Diffusion style.
```

Add to `FINAL CHECK`:

```text
- For Pony, use score tags and comma-separated booru-style prompting.
```

---

## Add Realistic SDXL Style

Add to `IMAGE_MODELS`:

```python
IMAGE_MODELS = {
    "1": ("Lustify_v8_Apex.safetensors",                           "Lustify V8 Apex · photoreal SDXL"),
    "2": ("oneObsessionHybridTheoryNoobAIIllustrious.safetensors", "OneObsession HybridTheory · NoobAI Illustrious anime"),
    "3": ("realvisxlV50.safetensors",                              "RealVisXL V5.0 · realistic SDXL"),
    "4": ("Custom",                                                 "Enter your own checkpoint name"),
}
```

Update tags:

```python
tags = {
    "1": "photoreal",
    "2": "anime",
    "3": "realistic",
    "4": "custom",
}
```

Add to `SYSTEM_PROMPT` under `MODEL ADAPTATION`:

```text
3. REALVISXL / realistic SDXL

This is a realistic SDXL model that responds well to natural photography language, lighting, lens details, and realistic scene descriptions.

For RealVisXL:
- Use natural photographic language.
- Keep prompts clear and not too long.
- Use realistic lighting, lens, composition, and camera terms.
- Avoid anime, cartoon, painting, and illustration terms unless requested.
- Do not use Pony score tags.
- Do not use booru-style anime tags unless requested.

RealVisXL positive prompt structure:
realistic photo, [subject], [pose/action], [appearance], [clothing], [environment], [lighting], [camera/lens], depth of field, natural skin texture, high detail, cinematic composition

RealVisXL negative prompt structure:
anime, cartoon, illustration, painting, cgi, 3d render, plastic skin, doll, low quality, worst quality, blurry, bad anatomy, bad hands, bad face, text, watermark, logo, distorted, deformed
```

Add to `MODEL DETECTION`:

```text
If the selected image model name contains any of these words:
RealVis, realvis, realistic, photoreal
then use the RealVisXL style.
```

Add to `FINAL CHECK`:

```text
- For RealVisXL, keep it realistic, photographic, and natural.
```

---

## Safety Rules

Good short version:

```text
SAFETY / SUBJECT RULES
Follow the user's subject request closely. Do not add minors, real private people, illegal acts, hate symbols, gore, or non-consensual themes. Keep adult-looking characters clearly adult. Avoid adding sexual content unless explicitly requested.
```

Stricter version:

```text
SAFETY / SUBJECT RULES
Follow the user's subject request closely. Do not add minors, real private people, illegal acts, hate symbols, gore, non-consensual themes, sexualized violence, or exploitative content. Keep adult-looking characters clearly adult. Avoid adding sexual content unless explicitly requested.
```

General-safe version:

```text
SAFETY / SUBJECT RULES
Keep prompts suitable for general image generation. Do not add sexual content, minors, gore, hate symbols, real private people, illegal acts, or non-consensual themes. Follow the user's subject without adding unsafe details.
```

---

# Ollama LLM Models

PromptForge detects Ollama models from:

```text
http://127.0.0.1:11434/api/tags
```

Detection function:

```python
def discover_ollama_models() -> dict[str, tuple[str, str]]:
```

Models are sorted by size, largest first.

---

## Change Fallback LLM Models

Find:

```python
FALLBACK_LLM_MODELS = {
    "1": ("qwen2.5:7b-instruct", "Fallback · best overall prompt writing"),
    "2": ("llama2-uncensored:latest", "Fallback · less filtered, weaker formatting"),
    "3": ("nchapman/mn-12b-mag-mell-r1:latest", "Fallback · bigger creative model"),
}
```

Change to:

```python
FALLBACK_LLM_MODELS = {
    "1": ("llama3.1:8b", "Fallback · strong general model"),
    "2": ("mistral", "Fallback · fast local model"),
    "3": ("qwen2.5:7b-instruct", "Fallback · good prompt writer"),
}
```

Check installed models:

```bash
ollama list
```

---

## Change LLM Descriptions

Find:

```python
def model_family_hint(name: str) -> str:
```

Add new detection rules:

```python
if "yi" in lower:
    return "Yi · general local model"
```

Example:

```python
def model_family_hint(name: str) -> str:
    lower = name.lower()

    if "qwen" in lower:
        return "Qwen · strong prompt writing"
    if "llama" in lower:
        return "Llama · general local model"
    if "mistral" in lower:
        return "Mistral · fast instruction model"
    if "yi" in lower:
        return "Yi · general local model"

    return "Local Ollama model"
```

---

# Ollama Generation Settings

Find inside `ask_ollama()`:

```python
"options": {
    "temperature": 0.85,
    "top_p": 0.9,
    "repeat_penalty": 1.12,
},
```

Controlled output:

```python
"options": {
    "temperature": 0.55,
    "top_p": 0.85,
    "repeat_penalty": 1.15,
},
```

Creative output:

```python
"options": {
    "temperature": 1.0,
    "top_p": 0.95,
    "repeat_penalty": 1.08,
},
```

Balanced output:

```python
"options": {
    "temperature": 0.75,
    "top_p": 0.9,
    "repeat_penalty": 1.12,
},
```

---

# Clipboard Menu

Clipboard menu function:

```python
def copy_menu(positive: str, negative: str):
```

Current options:

```text
1 positive
2 negative
3 both
Enter skip
```

Add WebUI copy option:

```python
print(
    f"  {MUTED}copy{RST}  "
    f"{ORANGE}1{RST}{MUTED} positive  "
    f"{ORANGE}2{RST}{MUTED} negative  "
    f"{ORANGE}3{RST}{MUTED} both  "
    f"{ORANGE}4{RST}{MUTED} webui  "
    f"{ORANGE}↵{RST}{MUTED} skip{RST}\n"
)
```

Add this option:

```python
elif choice == "4":
    webui = f"{positive}\nNegative prompt: {negative}"
    ok("WebUI format copied." if copy_to_clipboard(webui) else "Clipboard unavailable.")
```

---

# Add Commands

Commands are handled in `main()`.

Example command:

```python
if cmd == "/doctor":
    doctor(llm_model, image_model)
    continue
```

Add `/models`:

```python
if cmd == "/models":
    show_models(llm_model, image_model)
    continue
```

Add function:

```python
def show_models(llm_model: str, image_model: str):
    render_shell(llm_model, image_model)

    box_top(f"{ORANGE}{B}Models{RST}", BORDER)
    box_row(f"Current LLM: {llm_model}")
    box_row(f"Current image model: {image_model}")
    box_bot(BORDER)
    print()
```

Update help:

```python
box_row(f"{ORANGE}/models{RST}  Show selected models")
```

---

# Doctor Screen

Doctor function:

```python
def doctor(llm_model: str, image_model: str):
```

Add selected image model:

```python
box_row(f"{ORANGE}✓{RST} Selected image model: {image_model}")
```

Add Ollama URL:

```python
box_row(f"{MUTED}Ollama URL: {OLLAMA_TAGS_URL}{RST}")
```

---

# Troubleshooting

## Ollama is not running

Start Ollama:

```bash
ollama serve
```

Restart PromptForge:

```bash
python promptforge.py
```

---

## No Ollama models show up

Check models:

```bash
ollama list
```

Install a model:

```bash
ollama pull qwen2.5:7b-instruct
```

---

## Fallback model does not work

Check installed models:

```bash
ollama list
```

Install the missing model or change `FALLBACK_LLM_MODELS`.

---

## Clipboard unavailable

Supported clipboard tools:

| System | Tool |
|---|---|
| Windows | `clip` |
| macOS | `pbcopy` |
| Linux X11 | `xclip` |
| Linux Wayland | `wl-copy` |

Install X11 clipboard:

```bash
sudo apt install xclip
```

Install Wayland clipboard:

```bash
sudo apt install wl-clipboard
```

---

## Boxes look broken

Use a terminal with Unicode box drawing support.

Recommended terminals:

- Windows Terminal
- WezTerm
- Kitty
- Alacritty
- GNOME Terminal
- iTerm2

---

## Prompt output is messy

Lower temperature:

```python
"temperature": 0.55,
```

Add stricter final rules to `SYSTEM_PROMPT`:

```text
- Do not explain.
- Do not add markdown.
- Do not add extra sections.
- Output only POSITIVE and NEGATIVE.
```

---

## Image model style is wrong

Add more detection words to `MODEL DETECTION`.

Example:

```text
If the selected image model name contains any of these words:
myCustomRealisticModel, realisticCustom, photoModel
then use the RealVisXL style.
```

---

# Editing Checklist

```text
[ ] SYSTEM_PROMPT still uses triple quotes
[ ] POSITIVE and NEGATIVE labels are unchanged
[ ] IMAGE_MODELS entries are valid
[ ] Custom option logic is correct
[ ] Image model tags are updated
[ ] Model detection words are added
[ ] Model adaptation rules are added
[ ] /llm works
[ ] /img works
[ ] /doctor works
[ ] Prompt generation works
[ ] Clipboard copying works
[ ] Terminal layout still looks correct
```

---

# Best Practices

- Make one change at a time.
- Test after every change.
- Keep checkpoint names descriptive.
- Keep system prompt sections organized.
- Keep negative prompts focused on flaws and unwanted traits.
- Keep output format stable.
- Use `/doctor` after changing Ollama settings.
- Use `/img` after changing image models.
- Use `/llm` after installing new Ollama models.

---

# License

Use, edit, and modify PromptForge however you want but you have to mention me.
