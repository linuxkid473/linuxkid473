#!/usr/bin/env python3
"""Generate the neon/hacker SVG panels behind the linuxkid473 profile README.

Usage: python3 scripts/generate-assets.py
Writes assets/hero.svg, assets/console.svg and assets/stack.svg.
assets/activity.svg is generated separately by scripts/generate-activity.js.
"""

import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

BG0, BG1 = "#04070b", "#080d13"
EDGE0, EDGE1 = "#1d3a40", "#0d1a1f"
DIM = "#31505b"     # timestamps / structure
MID = "#5d7f8b"     # secondary text
TXT = "#d8fff4"     # primary text
GRN = "#39ff14"     # neon green
CYN = "#19f7ff"     # neon cyan
MAG = "#ff2bd6"     # neon magenta
AMB = "#ffb000"

CW = 0.6  # monospace advance width per em


def w(text, size):
    return len(text) * size * CW


def defs_common(prefix):
    return f'''  <defs>
    <linearGradient id="{prefix}bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{BG0}"/>
      <stop offset="100%" stop-color="{BG1}"/>
    </linearGradient>
    <linearGradient id="{prefix}edge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{EDGE0}"/>
      <stop offset="100%" stop-color="{EDGE1}"/>
    </linearGradient>
    <linearGradient id="{prefix}neon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{GRN}"/>
      <stop offset="45%" stop-color="{CYN}"/>
      <stop offset="100%" stop-color="{MAG}"/>
    </linearGradient>
    <linearGradient id="{prefix}sweep" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{CYN}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{CYN}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{CYN}" stop-opacity="0"/>
    </linearGradient>
    <filter id="{prefix}glow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="{prefix}soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.4" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <pattern id="{prefix}grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0 H0 V40" fill="none" stroke="{CYN}" stroke-opacity="0.05" stroke-width="1"/>
    </pattern>
    <pattern id="{prefix}scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#ffffff" opacity="0.022"/>
    </pattern>
  </defs>'''


def shell_open(prefix, w_, h_, extra=""):
    return f'''  <g clip-path="url(#{prefix}clip)">
    <rect x="1" y="1" width="{w_-2}" height="{h_-2}" rx="12" fill="url(#{prefix}bg)"/>
    <rect x="1" y="1" width="{w_-2}" height="{h_-2}" rx="12" fill="url(#{prefix}grid)"/>
    <rect x="1" y="1" width="{w_-2}" height="{h_-2}" rx="12" fill="url(#{prefix}scan)"/>
{extra}'''


def shell_close(prefix, w_, h_):
    return f'''    <rect x="1" y="1" width="{w_-2}" height="{h_-2}" rx="12" fill="url(#{prefix}sweep)" opacity="0.09">
      <animate attributeName="y" values="{-h_};{h_}" dur="9s" repeatCount="indefinite"/>
    </rect>
    <rect x="1" y="1" width="{w_-2}" height="{h_-2}" rx="12" fill="none" stroke="url(#{prefix}edge)" stroke-width="1.5"/>
  </g>'''


# ---------------------------------------------------------------- hero -------
def hero():
    p = "h"
    W, H = 1000, 330
    corners = "".join(
        f'    <path d="{d}" fill="none" stroke="{GRN}" stroke-opacity="0.5" stroke-width="2"/>'
        for d in (
            "M22 46 V22 H46",
            f"M{W-22} 46 V22 H{W-46}",
            f"M22 {H-46} V{H-22} H46",
            f"M{W-22} {H-46} V{H-22} H{W-46}",
        )
    )
    noise_left = [
        "0xDEADBEEF", "mov eax, 0x473", "lgdt [gdt_desc]",
        "int 0x80", "cli / sti", "call kmain",
    ]
    noise_right = [
        "0b10100101", "xchg esp, ebp", "retf 0x08", "0x7C00",
        "iretd", "page_fault",
    ]
    left = "\n".join(
        f'    <text x="30" y="{116 + i*26}" font-size="12" fill="{DIM}" opacity="0.5">{t}</text>'
        for i, t in enumerate(noise_left)
    )
    right = "\n".join(
        f'    <text x="{W-30}" y="{116 + i*26}" font-size="12" fill="{DIM}" opacity="0.5" text-anchor="end">{t}</text>'
        for i, t in enumerate(noise_right)
    )
    name = "VIHAAN NATHAN"
    size = 76
    span = w(name, size) + len(name) * 4
    return f'''<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="heroTitle heroDesc">
  <title id="heroTitle">Vihaan Nathan — systems programmer</title>
  <desc id="heroDesc">
    Neon terminal banner. Vihaan Nathan, 14, systems programmer: writes operating
    systems, kernels and emulators from scratch in C, x86 assembly and C++.
  </desc>
{defs_common(p)}
  <clipPath id="{p}clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12"/></clipPath>
{shell_open(p, W, H, corners)}
{left}
{right}

    <!-- status line -->
    <g font-family="{MONO}" font-size="12.5" letter-spacing="1.2">
      <circle cx="34" cy="30" r="5" fill="{MAG}" opacity="0.85"/>
      <circle cx="52" cy="30" r="5" fill="{AMB}" opacity="0.55"/>
      <circle cx="70" cy="30" r="5" fill="{GRN}" opacity="0.85"/>
      <text x="94" y="34" fill="{MID}">root@github:~# ./whoami --verbose</text>
      <text x="{W-30}" y="34" text-anchor="end" fill="{DIM}">id 0x473 · tty/1</text>
    </g>
    <line x1="1" y1="52" x2="{W-1}" y2="52" stroke="{EDGE1}" stroke-width="1"/>

    <!-- glitch ghosts + name -->
    <g font-family="{MONO}" font-size="{size}" font-weight="700" letter-spacing="4" text-anchor="middle">
      <text x="{500 - 5}" y="158" fill="{MAG}" opacity="0.5">
        {name}
        <animateTransform attributeName="transform" type="translate" values="0 0;0 0;-8 2;7 -2;0 0;0 0;0 0;0 0" keyTimes="0;0.6;0.63;0.66;0.69;0.82;0.92;1" dur="5.5s" repeatCount="indefinite"/>
      </text>
      <text x="{500 + 5}" y="158" fill="{CYN}" opacity="0.42">
        {name}
        <animateTransform attributeName="transform" type="translate" values="0 0;0 0;9 -2;-6 2;0 0;0 0;0 0;0 0" keyTimes="0;0.6;0.63;0.66;0.69;0.82;0.92;1" dur="5.5s" repeatCount="indefinite"/>
      </text>
      <text x="500" y="158" fill="url(#{p}neon)" filter="url(#{p}glow)">
        {name}
        <animate attributeName="opacity" values="0.88;1;0.88" dur="3.2s" repeatCount="indefinite"/>
      </text>
    </g>

    <!-- underline sweep -->
    <line x1="{500 - span/2:.1f}" y1="178" x2="{500 + span/2:.1f}" y2="178" stroke="url(#{p}neon)" stroke-width="2.5" stroke-dasharray="{span:.1f}" stroke-dashoffset="0">
      <animate attributeName="stroke-dashoffset" values="{span:.1f};0;0" keyTimes="0;0.35;1" dur="6s" repeatCount="indefinite"/>
    </line>

    <!-- subtitle -->
    <g font-family="{MONO}" text-anchor="middle">
      <text x="500" y="222" font-size="17.5" letter-spacing="0.6" fill="{CYN}" filter="url(#{p}soft)">systems programmer · 14 · builds oses, kernels &amp; emulators from scratch</text>
      <text x="500" y="256" font-size="13" letter-spacing="3.5" fill="{MID}">C · x86-64 ASM · C++ · BASH · NO FRAMEWORKS</text>
    </g>

    <!-- footer strip -->
    <line x1="1" y1="{H-46}" x2="{W-1}" y2="{H-46}" stroke="{EDGE1}" stroke-width="1"/>
    <g font-family="{MONO}" font-size="12" letter-spacing="1.2">
      <text x="34" y="{H-22}" fill="{GRN}" opacity="0.85">[ ok ]</text>
      <text x="88" y="{H-22}" fill="{MID}">13 public repos · everything compiled on bare metal and qemu</text>
      <text x="{W-34}" y="{H-24}" text-anchor="end" fill="{DIM}">bash 5.2</text>
    </g>
    <rect x="{W-30}" y="{H-38}" width="11" height="16" fill="{GRN}" opacity="1">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.02;0.05;0.5;0.53;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
{shell_close(p, W, H)}
</svg>
'''


# ------------------------------------------------------------- console -------
def console():
    p = "c"
    W, H = 1000, 404
    rows = [
        ("0.000000", "vihaan", "systems programmer · age 14 · writes operating systems from scratch", TXT),
        ("0.000473", "kernel", "pureunix — process table, vfs, signals, pipes, usb/xhci online", GRN),
        ("0.001337", "kernel", "asteros — darwin / xnu based, booting to loginwindow", GRN),
        ("0.002950", "emulate", "ppcosxkvm — powerpc mac os x tiger on apple silicon", MAG),
        ("0.004096", "emulate", "maclator — arm64 binaries on intel via interpreter + jit + aot cache", MAG),
        ("0.005611", "gpu", "metal bridge mounted · quartz extreme · core image online", CYN),
        ("0.006942", "toolchain", "gnu · nasm · ld · gdb · qemu · git — no framework, no hand-holding", TXT),
        ("0.009118", "userland", "mounting /home/vihaan ..... ok", GRN),
    ]
    lines = []
    for i, (ts, tag, msg, color) in enumerate(rows):
        begin = 0.15 + i * 0.3
        lines.append(f'''      <text x="40" y="{76 + i*30}" opacity="1" filter="url(#{p}soft)">
        <tspan fill="{DIM}">[  {ts}]</tspan><tspan fill="{MID}" dx="6">{tag}:</tspan><tspan fill="{color}" dx="6">{msg}</tspan>
        <animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.12s" fill="freeze"/>
      </text>''')
    log = "\n".join(lines)
    y_prompt = 76 + len(rows) * 30 + 22
    return f'''<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="conTitle conDesc">
  <title id="conTitle">Boot console</title>
  <desc id="conDesc">
    Animated boot console: vihaan, 14, systems programmer. Loads PureUNIX (unix-like
    kernel from scratch), AsterOS (darwin/xnu based), the ppcosxkvm and maclator
    emulators, the Metal GPU bridge and the GNU/QEMU toolchain, then drops to a
    verbose run prompt.
  </desc>
{defs_common(p)}
  <clipPath id="{p}clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12"/></clipPath>
{shell_open(p, W, H, "")}
    <!-- chrome bar -->
    <rect x="1" y="1" width="{W-2}" height="34" fill="#070c11"/>
    <circle cx="26" cy="18" r="5" fill="{MAG}" opacity="0.8"/>
    <circle cx="44" cy="18" r="5" fill="{AMB}" opacity="0.5"/>
    <circle cx="62" cy="18" r="5" fill="{GRN}" opacity="0.8"/>
    <text x="500" y="22" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MID}" letter-spacing="1.5">/dev/console — vihaan@github</text>
    <line x1="1" y1="35" x2="{W-1}" y2="35" stroke="{EDGE1}" stroke-width="1"/>

    <g font-family="{MONO}" font-size="15">
{log}

      <!-- prompt -->
      <text x="40" y="{y_prompt}" opacity="1" font-size="16">
        <tspan fill="{GRN}">vihaan</tspan><tspan fill="{DIM}">@</tspan><tspan fill="{GRN}">github</tspan><tspan fill="{DIM}">:</tspan><tspan fill="{MID}">~$</tspan><tspan fill="{CYN}" dx="6">./run --verbose</tspan>
        <animate attributeName="opacity" from="0" to="1" begin="{0.15 + len(rows)*0.3:.2f}s" dur="0.2s" fill="freeze"/>
      </text>
      <rect x="{40 + w('vihaan@github:~$ ./run --verbose', 16) + 8:.0f}" y="{y_prompt - 14}" width="10" height="18" fill="{GRN}" opacity="1">
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.001;0.01;0.5;0.51;1" begin="{0.5 + len(rows)*0.3:.2f}s" dur="1.05s" repeatCount="indefinite"/>
      </rect>
    </g>
{shell_close(p, W, H)}
</svg>
'''


# --------------------------------------------------------------- stack -------
def stack():
    p = "s"
    W = 1000
    cards = [
        ("0x01", "LANGUAGES", CYN, ["C · x86-64 assembly", "C++ · Bash · Make", "JavaScript · HTML/CSS"]),
        ("0x02", "SYSTEMS", GRN, ["kernel · memory · sched", "syscalls · signals · elf", "vfs · drivers · usb/xhci"]),
        ("0x03", "EMULATION", MAG, ["qemu · powerpc g3/g4", "interpreter · jit · aot", "metal / opengl bridges"]),
        ("0x04", "TOOLCHAIN", AMB, ["gnu · nasm · ld · ld64", "gdb · make · git", "qemu · opencore / openduet"]),
        ("0x05", "PLATFORMS", CYN, ["x86-64 · arm64 · powerpc", "linux · macos / xnu", "legacy bios · uefi"]),
        ("0x06", "CURIOSITY", MAG, ["reverse engineering", "bootloaders · firmware", "gpu, metal & kernel internals"]),
    ]
    cw, ch = 296, 124
    xs = [32, 352, 672]
    ys = [78, 214]
    out = []
    for i, (idx, title, color, items) in enumerate(cards):
        x, y = xs[i % 3], ys[i // 3]
        begin = 0.2 + i * 0.18
        item_txt = "\n".join(
            f'        <text x="{x+18}" y="{y+74 + j*20}" font-size="12.5" fill="{MID}">{t.replace("&", "&amp;")}</text>'
            for j, t in enumerate(items)
        )
        out.append(f'''    <g opacity="1">
      <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" fill="#070c11" stroke="{color}" stroke-opacity="0.32" stroke-width="1"/>
      <rect x="{x}" y="{y}" width="52" height="3" rx="1.5" fill="{color}"/>
      <text x="{x+18}" y="{y+34}" font-family="{MONO}" font-size="14" letter-spacing="2.4" fill="{color}" filter="url(#{p}soft)">{title}</text>
      <text x="{x+cw-18}" y="{y+34}" font-family="{MONO}" font-size="11" fill="{DIM}" text-anchor="end">{idx}</text>
      <line x1="{x+18}" y1="{y+46}" x2="{x+cw-18}" y2="{y+46}" stroke="{color}" stroke-opacity="0.22" stroke-width="1"/>
{item_txt}
      <animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>
    </g>''')
    body = "\n".join(out)
    H = 366
    return f'''<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="stkTitle stkDesc">
  <title id="stkTitle">Stack matrix</title>
  <desc id="stkDesc">
    Stack matrix. Languages: C, x86-64 assembly, C++, Bash, Make, JavaScript.
    Systems: kernel, memory management, scheduling, syscalls, signals, ELF, VFS,
    drivers, USB/xHCI. Emulation: QEMU, PowerPC, interpreter, JIT, AOT cache,
    Metal and OpenGL bridges. Toolchain: GNU, nasm, ld, GDB, Make, Git, OpenCore.
    Platforms: x86-64, arm64, PowerPC, Linux, macOS/XNU, legacy BIOS, UEFI.
  </desc>
{defs_common(p)}
  <clipPath id="{p}clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12"/></clipPath>
{shell_open(p, W, H, "")}
    <text x="32" y="42" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{MID}">/etc/profile.d/stack.conf</text>
    <text x="{W-32}" y="42" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{DIM}" text-anchor="end">cat stack.conf</text>
    <line x1="32" y1="54" x2="{W-32}" y2="54" stroke="{EDGE1}" stroke-width="1"/>
{body}
    <line x1="32" y1="{H-34}" x2="{W-32}" y2="{H-34}" stroke="{EDGE1}" stroke-width="1"/>
    <text x="32" y="{H-14}" font-family="{MONO}" font-size="12" fill="{MID}">
      <tspan fill="{GRN}" opacity="0.85">[ ok ]</tspan><tspan dx="8">hand-written c, asm and linker scripts — boots on real hardware and qemu</tspan>
    </text>
{shell_close(p, W, H)}
</svg>
'''


os.makedirs(OUT, exist_ok=True)
for name, fn in (("hero.svg", hero), ("console.svg", console), ("stack.svg", stack)):
    path = os.path.join(OUT, name)
    with open(path, "w") as fh:
        fh.write(fn())
    print(f"wrote {path} ({os.path.getsize(path)} bytes)")