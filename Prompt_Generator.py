  import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from colorama import init, Fore, Style

init(autoreset=True)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"

APP_NAME = "PromptForge"
APP_VERSION = "v1.0.0"

FALLBACK_LLM_MODELS = {
    "1": ("qwen2.5:7b-instruct", "Fallback · best overall prompt writing"),
    "2": ("llama2-uncensored:latest", "Fallback · less filtered, weaker formatting"),
    "3": ("nchapman/mn-12b-mag-mell-r1:latest", "Fallback · bigger creative model"),
}

IMAGE_MODELS = {
    "1": ("Lustify_v8_Apex.safetensors",                           "Lustify V8 Apex · photoreal SDXL"),
    "2": ("oneObsessionHybridTheoryNoobAIIllustrious.safetensors", "OneObsession HybridTheory · NoobAI Illustrious anime"),
    "3": ("Custom",                                                 "Enter your own checkpoint name"),
}

# ---------------------------------------------------------------------------
SYSTEM_PROMPT = r"""
You are a professional Stable Diffusion prompt generator.

Your job is to convert the user's idea into a model-specific Stable Diffusion prompt.

OUTPUT FORMAT
Always output exactly this format and nothing else:

POSITIVE:
[positive prompt]

NEGATIVE:
[negative prompt]

Do not write explanations.
Do not write greetings.
Do not write markdown.
Do not write settings unless the user asks for settings.
Do not add text before POSITIVE or after NEGATIVE.

GENERAL RULES
Follow the user's request closely.
Do not over-explain.
Do not turn every prompt into a paragraph.
Use the prompting style that matches the selected image model.
Keep the prompt useful for txt2img/img2img in Forge or WebUI.

The positive prompt should be detailed, but model-appropriate:
- For photoreal models, use natural photography words and concise tags.
- For anime/Illustrious/NoobAI models, use comma-separated booru/anime tags.
- Avoid useless repetition.
- Do not add random unrelated objects.
- Do not add unwanted people.
- Do not change the subject unless needed for clarity.

SAFETY / SUBJECT RULES
Follow the user’s subject request closely. Do not add minors, real private people, illegal acts, hate symbols, gore, or non-consensual themes. Keep adult-looking characters clearly adult. Avoid adding sexual content unless explicitly requested.

NEGATIVE PROMPT RULES
The negative prompt must contain only flaws, unwanted styles, and unwanted output traits.
Do not put desired subject details in NEGATIVE.
Use model-appropriate negatives.
Keep negatives clean, useful, and not too long.

MODEL ADAPTATION

1. LUSTIFY / Lustify Apex / lustify_apex / photoreal SDXL
This is a photoreal model that responds well to concise natural language mixed with tags.

For Lustify:
- Use short-to-medium comma-separated photoreal prompts.
- Do NOT write long story paragraphs.
- Do NOT use Pony score tags.
- Do NOT use Illustrious tags like lazypos/lazyup unless the user explicitly asks.
- Use photography words, body/pose/composition tags, lighting tags, camera tags, and aesthetic tags.
- Good style tags include:
  high aesthetic, beautiful face, photo of an person/girl/woman, realistic photo, natural skin texture, depth of field, sunlight, blue sky, cinematic lighting, soft lighting, dramatic lighting, neon lighting, low key lighting, film grain, bokeh, analog photo, glamour photography, candid photo, amateur photo, shot on Canon EOS 5D, shot on Leica T, shot on Polaroid SX-70, Fujicolor Pro, Ilford HP5 Plus
- Good negative style:
  old, ugly, bad anatomy, bad hands, bad face, deformed, distorted, blurry, low quality, worst quality, text, watermark, logo, extra fingers, missing fingers, bad eyes, plastic skin, doll, cgi, 3d render, cartoon, anime, painting, drawing

Lustify positive prompt structure:
Start with important subject and composition tags, then appearance, pose, environment, lighting, camera/style.
Example structure:
high aesthetic, beautiful face, photo of an person/girl/woman, [subject], [pose], [clothing/appearance], [environment], [lighting], [camera/composition], depth of field, realistic photo, natural skin texture, film grain

Lustify negative prompt structure:
old, ugly, bad anatomy, bad hands, bad face, blurry, low quality, worst quality, text, watermark, logo, deformed, distorted, extra fingers, missing fingers, plastic skin, cgi, 3d render, cartoon, anime, painting, drawing

If user asks for Lustify settings, recommend:
Sampler: DPM++ 2M SDE or DPM++ 3M SDE
Scheduler: Karras or Exponential
Steps: 30
CFG: 2.5-4.5
For LCM only: Steps 6-10, CFG 1-2
Highres.fix: 1.4-1.5 upscale, denoise around 0.35-0.45
Use ADetailer for distant faces.

2. ONEOBSESSION HYBRIDTHEORY NOOBAI ILLUSTRIOUS / NoobAI / Illustrious anime
This is an anime/Illustrious model. It responds well to booru tags, quality tags, artist/style tags, lighting tags, and strong composition tags.

For OneObsession:
- Use comma-separated anime booru tags.
- Do NOT write realistic photo paragraphs unless user requests semi-realism.
- Do NOT use Pony score tags.
- Use quality tags and aesthetic tags.
- Use character tags if provided by the user.
- Use escaped character names when needed, such as character_name \(series\).
- Use dynamic angle, dutch angle, depth of field, chiaroscuro, high contrast, detailed lighting, glossy surfaces, smooth shading, colorful depth.
- Artist/style tags may be used if the user asks for a specific art style, but do not overload every prompt with too many artists.

OneObsession positive prompt should often include:
masterpiece, best quality, amazing quality, very aesthetic, newest, absurdres, highres, depth of field, high detail, detailed eyes, perfect eyes, smooth shading, glossy surfaces, colorful depth, high contrast, chiaroscuro, cinematic lighting, dynamic angle, dutch angle, foreshortening, intricate details

Optional OneObsession style tags:
lazypos, lazyup, very awa, sensitive, real background, subtle, masterful shading, impasto, shallow depth of field, ray tracing, light particles, light leaks, beautiful detailed glow, shiny, iridescent

OneObsession negative prompt should usually be:
anatomical nonsense, interlocked fingers, extra fingers, missing fingers, watermark, simple background, transparent, low quality, logo, text, signature, worst quality, bad quality, jpeg artifacts, username, censored, extra digit, ugly, bad_hands, bad_feet, bad_anatomy, deformed anatomy, bad proportions, lowres

OneObsession positive prompt structure:
[main subject tags], [character tags if any], [appearance], [pose/action], [clothing], [environment], [camera angle/composition], [lighting/mood], masterpiece, best quality, amazing quality, very aesthetic, newest, absurdres, highres, depth of field, high contrast, chiaroscuro, dynamic angle, detailed eyes, smooth shading, intricate details

If user asks for OneObsession settings, recommend:
Sampler: Euler a
Steps: 20-30
CFG: 3-6
Resolution: 832x1216, 896x1152, 768x1344, 1024x1536, 640x1536
Scheduler: Karras
Highres.fix: upscale 1.3-1.5
Denoising: 0.45-0.7 depending on how much change is desired
Upscaler: R-ESRGAN 4x+ Anime6B for anime detail, or Latent for softer results
Use ADetailer face_yolov8n.pt for face cleanup.

MODEL DETECTION
If the selected image model name contains any of these words:
Lustify, lustify, Apex, photoreal
then use the Lustify style.

If the selected image model name contains any of these words:
oneObsession, OneObsession, HybridTheory, NoobAI, Noobai, Illustrious
then use the OneObsession NoobAI Illustrious style.

If the model is unknown:
Use a balanced SDXL prompt with natural description plus concise quality tags.

FINAL CHECK
Before outputting:
- The answer must start with POSITIVE:
- It must include NEGATIVE:
- It must contain no extra text.
- It must match the selected model style.
- For Lustify, keep it photoreal and concise.
- For OneObsession, keep it anime booru-style and tag-rich.
- If settings arent requested, do not give settings.
""".strip()

# ── ANSI / Theme ─────────────────────────────────────────────────────────────

W   = Fore.WHITE
D   = Style.DIM
B   = Style.BRIGHT
RST = Style.RESET_ALL

RED = Fore.RED
GRN = Fore.GREEN
CYN = Fore.CYAN
MAG = Fore.MAGENTA

ORANGE      = "\033[38;2;255;146;43m"
ORANGE_DIM  = "\033[38;2;196;96;28m"
AMBER       = "\033[38;2;255;185;80m"
GOLD        = "\033[38;2;255;204;102m"
BORDER      = "\033[38;2;184;101;43m"
MUTED       = "\033[38;2;145;130;115m"
SOFT        = "\033[38;2;220;180;130m"
PANEL       = "\033[38;2;235;150;72m"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def vlen(text: str) -> int:
    return len(strip_ansi(text))


def term_width(default: int = 120) -> int:
    return max(88, min(shutil.get_terminal_size((default, 28)).columns, 140))


def inner_width() -> int:
    return term_width() - 4


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def fit(text: str, width: int) -> str:
    plain_len = vlen(text)

    if plain_len <= width:
        return text + " " * (width - plain_len)

    raw = strip_ansi(text)

    if len(raw) <= width:
        return raw + " " * (width - len(raw))

    return raw[: max(0, width - 1)] + "…"


def wrap_words(text: str, width: int) -> list[str]:
    if not text:
        return [""]

    words = text.replace("\n", " ").split()
    lines, cur = [], ""

    for word in words:
        if not cur:
            cur = word
        elif len(strip_ansi(cur)) + 1 + len(strip_ansi(word)) <= width:
            cur += " " + word
        else:
            lines.append(cur)
            cur = word

    if cur:
        lines.append(cur)

    return lines or [""]


def hr(char: str = "─", color: str = BORDER):
    print(color + char * term_width() + RST)


def box_top(title: str = "", color: str = BORDER):
    width = inner_width()

    if title:
        clean_title = f" {title} "
        left = 3
        right = max(0, width - left - vlen(clean_title))
        print(color + "╭" + "─" * left + RST + clean_title + color + "─" * right + "╮" + RST)
    else:
        print(color + "╭" + "─" * width + "╮" + RST)


def box_mid(color: str = BORDER):
    print(color + "├" + "─" * inner_width() + "┤" + RST)


def box_bot(color: str = BORDER):
    print(color + "╰" + "─" * inner_width() + "╯" + RST)


def box_row(text: str = "", color: str = BORDER):
    print(color + "│ " + RST + fit(text, inner_width() - 2) + color + " │" + RST)


def two_col_row(left: str, right: str, split: int, color: str = BORDER):
    total = inner_width()
    left_w = split
    right_w = total - split - 1

    print(
        color + "│" + RST
        + fit(" " + left, left_w)
        + color + "│" + RST
        + fit(" " + right, right_w)
        + color + "│" + RST
    )


def two_col_empty(split: int, color: str = BORDER):
    two_col_row("", "", split, color)


# ── Ollama model discovery ───────────────────────────────────────────────────

def bytes_to_label(size_bytes: int) -> str:
    if not size_bytes:
        return "unknown size"

    gb = size_bytes / (1024 ** 3)

    if gb >= 1:
        return f"{gb:.1f} GB"

    mb = size_bytes / (1024 ** 2)
    return f"{mb:.0f} MB"


def model_family_hint(name: str) -> str:
    lower = name.lower()

    if "qwen" in lower:
        return "Qwen · strong prompt writing"
    if "llama" in lower:
        return "Llama · general local model"
    if "mistral" in lower:
        return "Mistral · fast instruction model"
    if "mixtral" in lower:
        return "Mixtral · large MoE model"
    if "gemma" in lower:
        return "Gemma · Google open model"
    if "phi" in lower:
        return "Phi · small efficient model"
    if "deepseek" in lower:
        return "DeepSeek · reasoning/code capable"
    if "mag" in lower or "mn-" in lower:
        return "Creative / roleplay model"
    if "codellama" in lower or "code" in lower:
        return "Code-capable local model"

    return "Local Ollama model"


def discover_ollama_models() -> dict[str, tuple[str, str]]:
    try:
        req = urllib.request.Request(
            OLLAMA_TAGS_URL,
            method="GET",
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        models = payload.get("models", [])

        if not models:
            return FALLBACK_LLM_MODELS

        models.sort(key=lambda m: m.get("size", 0), reverse=True)

        numbered = {}

        for idx, model in enumerate(models, start=1):
            name = model.get("name", "").strip()
            size = model.get("size", 0)

            if not name:
                continue

            size_label = bytes_to_label(size)
            hint = model_family_hint(name)

            numbered[str(idx)] = (
                name,
                f"{size_label} · {hint}",
            )

        return numbered or FALLBACK_LLM_MODELS

    except Exception:
        return FALLBACK_LLM_MODELS


def get_ollama_model_names() -> list[str]:
    try:
        req = urllib.request.Request(
            OLLAMA_TAGS_URL,
            method="GET",
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        return [m.get("name", "") for m in payload.get("models", []) if m.get("name")]

    except Exception:
        return []


# ── PromptForge Header ───────────────────────────────────────────────────────

PF_LOGO = [
    "██████╗ ███████╗",
    "██╔══██╗██╔════╝",
    "██████╔╝█████╗  ",
    "██╔═══╝ ██╔══╝  ",
    "██║     ██║     ",
    "╚═╝     ╚═╝     ",
]


def short_model(name: str, limit: int = 34) -> str:
    if len(name) <= limit:
        return name

    return name[: limit - 1] + "…"


def header_home(llm_model: str | None = None, image_model: str | None = None):
    clear()
    print()

    title = f"{ORANGE}{B}{APP_NAME} {APP_VERSION}{RST}{BORDER} "
    subtitle = f"{MUTED}local · Ollama · Stable Diffusion prompt forge{RST}"

    split = max(38, min(52, inner_width() // 2 - 2))

    box_top(f"{title}{subtitle}", BORDER)

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

    logo_block = ["", f"{ORANGE}{B}Welcome back!{RST}", ""] + [
        f"{ORANGE}{line}{RST}" for line in PF_LOGO
    ] + [""]

    max_rows = max(len(logo_block), len(right_lines))

    for i in range(max_rows):
        left = logo_block[i] if i < len(logo_block) else ""
        right = right_lines[i] if i < len(right_lines) else ""
        two_col_row(left.center(split - 2), right, split, BORDER)

    two_col_empty(split, BORDER)

    llm_text = short_model(llm_model or "No LLM selected", 40)
    img_text = short_model(image_model or "No image model selected", 40)

    two_col_row(
        f"{MUTED}LLM{RST} {ORANGE}{llm_text}{RST}",
        f"{MUTED}Checkpoint{RST} {AMBER}{img_text}{RST}",
        split,
        BORDER,
    )

    cwd = os.getcwd()

    two_col_row(
        f"{MUTED}{short_model(cwd, 42)}{RST}",
        f"{MUTED}/help for commands · /doctor for checks{RST}",
        split,
        BORDER,
    )

    box_bot(BORDER)
    hr("─", MUTED)


def footer():
    width = term_width()
    left = f"{MUTED}? for shortcuts{RST}"
    right = f"{MUTED}Local mode · Ollama required · {ORANGE}/doctor{RST}{MUTED} for details{RST}"
    gap = max(1, width - vlen(left) - vlen(right))
    print(left + " " * gap + right)


def render_shell(llm_model: str, image_model: str):
    header_home(llm_model, image_model)
    print()


# ── Menus ────────────────────────────────────────────────────────────────────

def menu_item(key: str, label: str, desc: str, tag: str = "", recommended: bool = False):
    badge = f" {ORANGE_DIM}[{tag}]{RST}" if tag else ""
    rec = f" {GOLD}← recommended{RST}" if recommended else ""

    print(
        f"  {BORDER}{key}{RST}  "
        f"{ORANGE}{B}{label}{RST}  "
        f"{MUTED}{desc}{RST}"
        f"{badge}{rec}"
    )


def prompt_line(label: str = "") -> str:
    prefix = f"{ORANGE}>{RST}"

    if label:
        prefix = f"{MUTED}{label}{RST} {prefix}"

    return input(f"  {prefix} {W}").strip()


def choose_llm_model():
    llm_models = discover_ollama_models()
    using_fallback = llm_models == FALLBACK_LLM_MODELS

    header_home()
    print(f"  {ORANGE}{B}Select AI model{RST}")

    if using_fallback:
        print(f"  {GOLD}!{RST} {MUTED}Could not read Ollama models. Showing fallback list.{RST}\n")
    else:
        print(f"  {MUTED}Detected from Ollama · sorted largest to smallest{RST}\n")

    hr("─", MUTED)
    print()

    for key, (model, desc) in llm_models.items():
        menu_item(
            key,
            model,
            desc,
            recommended=(key == "1"),
        )

    print()
    hr("─", MUTED)
    print()

    valid = ", ".join(llm_models.keys())

    while True:
        choice = prompt_line()

        if choice in llm_models:
            return llm_models[choice][0]

        print(f"\n  {RED}✗{RST} {MUTED}Enter one of: {valid}.{RST}\n")


def choose_image_model():
    header_home()
    print(f"  {ORANGE}{B}Select image model / checkpoint{RST}\n")
    print(f"  {MUTED}{B}Edit image models and the system prompt in the source code. Custom checkpoints use the generic SDXL prompt style.{RST}\n")
    hr("─", MUTED)
    print()

    tags = {
        "1": "photoreal",
        "2": "anime",
        "3": "custom",
    }

    for key, (model, desc) in IMAGE_MODELS.items():
        menu_item(key, model, desc, tag=tags.get(key, ""))

    print()
    hr("─", MUTED)
    print()

    while True:
        choice = prompt_line()

        if choice in IMAGE_MODELS and choice != "3":
            return IMAGE_MODELS[choice][0]

        if choice == "3":
            print()
            name = prompt_line("checkpoint name")

            if name:
                return name

            print(f"\n  {RED}✗{RST} {MUTED}Checkpoint name cannot be empty.{RST}\n")
            continue

        print(f"\n  {RED}✗{RST} {MUTED}Enter 1, 2, or 3.{RST}\n")


# ── Spinner ──────────────────────────────────────────────────────────────────

_spinner_stop = threading.Event()
_spinner_thread = None


def _spin(label: str):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    for frame in itertools.cycle(frames):
        if _spinner_stop.is_set():
            break

        print(f"\r  {ORANGE}{frame}{RST}  {MUTED}{label}{RST}", end="", flush=True)
        time.sleep(0.07)

    print("\r" + " " * (vlen(label) + 10) + "\r", end="", flush=True)


def spinner_start(label: str = "forging prompt…"):
    global _spinner_thread

    _spinner_stop.clear()
    _spinner_thread = threading.Thread(target=_spin, args=(label,), daemon=True)
    _spinner_thread.start()


def spinner_stop():
    _spinner_stop.set()

    if _spinner_thread:
        _spinner_thread.join()


# ── Ollama chat ──────────────────────────────────────────────────────────────

def ask_ollama(llm_model: str, user_prompt: str) -> str:
    data = {
        "model": llm_model,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "options": {
            "temperature": 0.85,
            "top_p": 0.9,
            "repeat_penalty": 1.12,
        },
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=300) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
        return payload["message"]["content"].strip()


# ── Result parsing / display ─────────────────────────────────────────────────

def split_prompt(text: str) -> tuple[str, str]:
    if "POSITIVE:" in text and "NEGATIVE:" in text:
        after_pos = text.split("POSITIVE:", 1)[1]
        pos, neg = after_pos.split("NEGATIVE:", 1)
        return pos.strip(), neg.strip()

    return text.strip(), ""


def prompt_box(title: str, body: str, accent: str):
    width = inner_width() - 4

    box_top(f"{accent}{B}{title}{RST}", BORDER)

    for line in wrap_words(body, width):
        box_row(f"{W}{line}{RST}", BORDER)

    box_bot(BORDER)


def show_result(positive: str, negative: str):
    print()

    prompt_box("+ POSITIVE", positive, ORANGE)

    print()

    prompt_box("– NEGATIVE", negative, RED)

    print()


# ── Clipboard ────────────────────────────────────────────────────────────────

def copy_to_clipboard(text: str) -> bool:
    try:
        if os.name == "nt":
            subprocess.run("clip", input=text, text=True, shell=True, check=True)
        elif shutil.which("pbcopy"):
            subprocess.run("pbcopy", input=text, text=True, check=True)
        elif shutil.which("xclip"):
            subprocess.run(["xclip", "-selection", "clipboard"], input=text, text=True, check=True)
        elif shutil.which("wl-copy"):
            subprocess.run("wl-copy", input=text, text=True, check=True)
        else:
            return False

        return True

    except Exception:
        return False


def ok(msg: str):
    print(f"\n  {ORANGE}✓{RST}  {MUTED}{msg}{RST}")


def err(msg: str):
    print(f"\n  {RED}✗{RST}  {W}{msg}{RST}\n")


def copy_menu(positive: str, negative: str):
    print(
        f"  {MUTED}copy{RST}  "
        f"{ORANGE}1{RST}{MUTED} positive  "
        f"{ORANGE}2{RST}{MUTED} negative  "
        f"{ORANGE}3{RST}{MUTED} both  "
        f"{ORANGE}↵{RST}{MUTED} skip{RST}\n"
    )

    choice = prompt_line()

    if choice == "1":
        ok("Positive prompt copied." if copy_to_clipboard(positive) else "Clipboard unavailable.")

    elif choice == "2":
        ok("Negative prompt copied." if copy_to_clipboard(negative) else "Clipboard unavailable.")

    elif choice == "3":
        both = f"POSITIVE:\n{positive}\n\nNEGATIVE:\n{negative}"
        ok("Both prompts copied." if copy_to_clipboard(both) else "Clipboard unavailable.")

    print()


# ── Utility screens ──────────────────────────────────────────────────────────

def show_help(llm_model: str, image_model: str):
    render_shell(llm_model, image_model)

    box_top(f"{ORANGE}{B}PromptForge shortcuts{RST}", BORDER)
    box_row(f"{ORANGE}/llm{RST}     Change prompt-writing model")
    box_row(f"{ORANGE}/img{RST}     Change Stable Diffusion checkpoint")
    box_row(f"{ORANGE}/clear{RST}   Redraw the interface")
    box_row(f"{ORANGE}/doctor{RST}  Check local Ollama setup")
    box_row(f"{ORANGE}/help{RST}    Show this screen")
    box_row(f"{ORANGE}/bye{RST}     Exit PromptForge")
    box_bot(BORDER)
    print()


def doctor(llm_model: str, image_model: str):
    render_shell(llm_model, image_model)

    box_top(f"{ORANGE}{B}Doctor{RST}", BORDER)

    try:
        req = urllib.request.Request(
            OLLAMA_TAGS_URL,
            method="GET",
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        models_raw = payload.get("models", [])
        models = [m.get("name", "") for m in models_raw if m.get("name")]

        box_row(f"{ORANGE}✓{RST} Ollama is running")
        box_row(f"{ORANGE}✓{RST} Installed models: {len(models)}")

        if models_raw:
            biggest = max(models_raw, key=lambda m: m.get("size", 0))
            biggest_name = biggest.get("name", "unknown")
            biggest_size = bytes_to_label(biggest.get("size", 0))
            box_row(f"{ORANGE}✓{RST} Largest model: {biggest_name} · {biggest_size}")

        if llm_model in models:
            box_row(f"{ORANGE}✓{RST} Selected LLM found: {llm_model}")
        else:
            box_row(f"{GOLD}!{RST} Selected LLM not found locally: {llm_model}")

    except Exception:
        box_row(f"{RED}✗{RST} Ollama is not reachable at {OLLAMA_TAGS_URL}")
        box_row(f"{MUTED}Start Ollama, then run /doctor again.{RST}")

    box_bot(BORDER)
    print()


# ── Request builder ──────────────────────────────────────────────────────────

def build_user_request(image_model: str, user_prompt: str) -> str:
    return (
        f"Image model/checkpoint: {image_model}\n\n"
        f"User request:\n{user_prompt}\n\n"
        f"Create a Stable Diffusion prompt for the selected image model. "
        f"Output only POSITIVE and NEGATIVE."
    )


# ── Main loop ────────────────────────────────────────────────────────────────

def main():
    llm_model = choose_llm_model()
    image_model = choose_image_model()

    render_shell(llm_model, image_model)

    while True:
        try:
            footer()
            user_prompt = prompt_line()
        except EOFError:
            break

        if not user_prompt:
            print()
            continue

        cmd = user_prompt.lower().strip()

        if cmd in ("/bye", "bye", "exit", "quit"):
            print(f"\n  {MUTED}Bye.{RST}\n")
            break

        if cmd == "/llm":
            llm_model = choose_llm_model()
            render_shell(llm_model, image_model)
            continue

        if cmd == "/img":
            image_model = choose_image_model()
            render_shell(llm_model, image_model)
            continue

        if cmd == "/clear":
            render_shell(llm_model, image_model)
            continue

        if cmd in ("/help", "?"):
            show_help(llm_model, image_model)
            continue

        if cmd == "/doctor":
            doctor(llm_model, image_model)
            continue

        final_prompt = build_user_request(image_model, user_prompt)

        print()
        spinner_start("forging prompt…")

        try:
            result = ask_ollama(llm_model, final_prompt)
            spinner_stop()

            positive, negative = split_prompt(result)

            render_shell(llm_model, image_model)
            show_result(positive, negative)
            copy_menu(positive, negative)

        except urllib.error.URLError:
            spinner_stop()
            err("Ollama is not running. Start Ollama first.")

        except TimeoutError:
            spinner_stop()
            err("The request timed out.")

        except KeyboardInterrupt:
            spinner_stop()
            print(f"\n\n  {MUTED}Interrupted.{RST}\n")
            break

        except Exception as exc:
            spinner_stop()
            err(str(exc))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {MUTED}Interrupted.{RST}\n")
        sys.exit()
