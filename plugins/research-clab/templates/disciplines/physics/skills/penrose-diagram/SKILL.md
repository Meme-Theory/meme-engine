---
name: penrose-diagram
description: TikZ-based Penrose / Carter-Penrose diagram authoring — preamble, pattern library, worked templates for Schwarzschild, Kerr, dS, CCC, dynamical compactification, and the M4 × SU(3)(τ) modulus-space transit. Use whenever a causal-structure diagram is needed.
disable-model-invocation: true
argument-hint: --schwarzschild | --kerr | --ds | --ads | --ccc | --transit | --minkowski | --patterns | --preamble | --check <file> | --new <name> | --help
allowed-tools: [Read, Write, Edit, Bash]
---

# Penrose Diagram Skill

A TikZ-based authoring guide for Carter-Penrose diagrams. Designed to be invoked from inside an agent conversation when a causal-structure figure is needed. Returns a copy-paste-ready LaTeX block, never an ASCII sketch.

**Where this lives in the project:**
- Skill source: `.claude/skills/penrose-diagram/SKILL.md` (this file)
- Diagram outputs: `figures/penrose/` (create if missing)
- General TikZ primer: `.claude/templates/LaTeX/08_TikZ_PGF_Scientific_Diagrams.md` (Feynman, eigenvalue, commutative diagrams — NOT Penrose-specific)

**When to use this skill:**
- Any time the agent would otherwise produce an ASCII Penrose sketch
- Constructing causal structure for the M4 × SU(3)(τ) transit through the dump point
- Visualizing trapped surfaces in the internal SU(3)
- Carroll-Johnson-Randall–style nucleation diagrams (4D universe behind an event horizon)
- Conformal-cyclic-cosmology aeon boundaries
- Higher-dimensional black-hole causal structure (Myers-Perry, black strings, GL pinch)

**When NOT to use:**
- Quick conversational sketch where ASCII still beats compilation overhead — that's fine, use ASCII inline. Save the skill for *output* diagrams that need to land in a paper or session report.

---

## Usage

```
/penrose-diagram --help                  Show usage
/penrose-diagram --preamble              Emit the canonical standalone preamble
/penrose-diagram --patterns              Show the snippet library (null lines, infinity labels, horizons, singularities, regions)
/penrose-diagram --minkowski             Emit minimal Minkowski lightcone .tex
/penrose-diagram --schwarzschild         Emit Schwarzschild four-region maximal extension .tex
/penrose-diagram --kerr                  Emit Kerr Penrose .tex with inner Cauchy horizon
/penrose-diagram --ds                    Emit de Sitter Penrose square .tex
/penrose-diagram --ads                   Emit anti-de Sitter cylinder .tex
/penrose-diagram --ccc                   Emit Penrose CCC two-aeon connection .tex
/penrose-diagram --transit               Emit M4 × SU(3)(τ) modulus-space transit diagram .tex
/penrose-diagram --new <name>            Scaffold a new diagram file with the standard preamble + an empty tikzpicture
/penrose-diagram --check figures/penrose/foo.tex   Audit an existing .tex for common Penrose-diagram errors
```

When invoked, the skill returns the requested LaTeX as a code block AND offers to save it to `figures/penrose/<name>.tex`. If the user accepts, the skill writes the file using the Write tool.

---

## The Author → Compile → Review Loop (MANDATORY for paper-quality diagrams)

**Why this exists**: TikZ authoring is code-blind by default — the agent writes coordinates and offsets but cannot see whether labels overlap, whether text extends outside the drawing area, whether colors clash, or whether the layout feels cramped. The result is "childlike" diagrams: substance correct, visual polish missing. The Read tool's ability to render PDFs as images closes this loop. Every paper-destined diagram MUST iterate through at least one review cycle; "write the .tex once and ship" is prohibited.

### The loop

1. **Author** the .tex using the canonical preamble, pattern library, and one of the worked templates as a starting point.
2. **Compile** with `xelatex -interaction=nonstopmode -output-directory=figures/penrose figures/penrose/<name>.tex` or via the `build.sh` helper. A clean compile is required before review; do not attempt to review a .tex that didn't produce a PDF.
3. **Read** the resulting PDF with the Read tool. Claude Code renders it as an image. You will see exactly what a human would see.
4. **Critique** against the Verification Rubric below. Write the observations down explicitly — do NOT skip to editing. The act of writing the critique is what surfaces problems you missed.
5. **Edit** the .tex to fix the specific problems identified. Use targeted Edit calls, not rewrites.
6. **Recompile** and **re-Read**. If the critique's issues are fixed and no new ones introduced, stop. If issues remain, loop.
7. **Iteration cap**: three review cycles maximum. If a fourth is needed, flag the diagram for human review and explain what's blocking convergence (e.g., "the diamond is too narrow at the label positions, need larger `scale`").

### Verification Rubric (apply in this order on every PDF read)

**Tier 1 — Layout-breaking (must fix)**
1. **Noodle lines**: worldlines, horizons, or trajectories drawn with bezier control points that cause lateral oscillation. A causal timelike worldline is monotone future-directed — it does NOT wiggle left and right. If your `\draw[worldline] (a) .. controls (b) and (c) .. (d)` has control points with offset x-coordinates, the curve will swing. Fix: use a straight line `(a) -- (d)` unless you have a specific geometric reason for the curve (e.g., acceleration in a boosted frame). Physically, the worldline should look like a timelike path: roughly vertical in the diamond, minimal lateral motion, single direction of travel. *(Framework-A iteration 4 fix: replaced `.. controls (wB) and (wC) ..` bezier with a pure `--` straight line.)*
2. **Text blockage**: any label whose glyphs are crossed by a line feature — worldline passing through the middle of a dashed-rule label, horizon clipping a corner label, singularity zigzag crossing a text block. Invisible in source; blindingly obvious in the PDF. Fix paths: (a) add `fill=white, inner sep=1pt` to the label's node options to give it an opaque background, (b) reposition the label away from the crossing feature using the **ideal justification** rule below, or (c) shorten the label so the crossing falls outside the shortened text.
3. **Ideal justification to avoid blockage**: when a horizontal rule (dashed horizon, dotted Cauchy slice, epoch rule) runs the full width of a diamond that has a central vertical worldline, the MIDPOINT (`pos=0.5`) of the rule is exactly where the worldline crosses it. Centered labels at the midpoint get sliced by the worldline. **Default placement**: put rule-labels at `pos=0.12` (left end) or `pos=0.88` (right end) instead of center. For two or more parallel rules, stack their labels at the SAME side for visual rhythm — e.g., τ≈0.22 and τ=0 both at `pos=0.12`, left-stacked — rather than alternating. *(Framework-A iteration 6 fix: τ=0 moved to pos=0.12 left, then τ≈0.22 moved to pos=0.12 left to match; the result reads as two stacked labels on the diamond's left shoulder, clear of the central worldline.)*
4. **Breathing room**: whitespace between corner labels (i⁺, i⁻, i⁰) and adjacent elements (caption block, legend, figure edge). A caption placed too close to i⁻ reads as a collision even if technically separated. **Minimum spacing**: 0.6–0.8 cm between the i⁻ label baseline and the first line of the caption; similarly for i⁺ to any element above the diamond. If the caption is at `(0, -3.85)` and the diamond goes to `(0, -3.2)`, that's only 0.65 cm gap minus the caption's line height — visually cramped. Move to `(0, -4.30)` or further. *(Framework-A iteration 6 fix: moved caption from y=-3.85 to y=-4.40, gap increased from ~0.4cm to ~0.9cm.)*
5. **Text overlaps other text**: two labels occupying the same pixels. Fix by repositioning one or by moving it into a callout box.
6. **Text extends outside the drawing area**: labels that run past the diamond edge or past the page border. Fix by reducing `text width`, choosing a shorter wording, or repositioning.
7. **Fragment rendering**: a label showing only part of its text (e.g., ".22" visible but "transit completion, τ≈0" clipped). Almost always caused by a callout/fill occluding the label.
8. **Invisible (nullfont) rendering**: entire labels or bold calls producing no glyphs. Indicates a missing font variant (see Font Troubleshooting below).

**Tier 2 — Polish (should fix)**
9. **Callout boxes not grouping related annotations**: floating text that should be in a bordered callout node. Fix with the `petrov callout` or `obs callout` styles (see templates).
10. **Two lines with the same visual style but different meanings**: e.g., two dashed blue lines, one a horizon and one an initial surface. Distinguish with color (blue dashed vs green dotted) and with explicit legend in the caption.
11. **Unlabeled features**: worldlines without a `γ_transit` label, horizons without `𝓗⁺`, shaded regions without a region name (I, II, III, IV). Every drawn feature that carries meaning needs a label.
12. **Inconsistent font authority**: bold labels rendered but their companion text in the same callout not bold, or vice versa. Fix by using the callout style uniformly.
13. **Leader-line tangles**: annotation lines crossing each other. Fix by repositioning or using straight anchors instead of curved leaders.

**Tier 3 — Aesthetic (nice to have)**
14. **Unbalanced visual weight**: one side of the diamond has all the callouts, the other is empty. Move one callout to the empty side or reduce the density on the crowded side.
15. **Font-mixing ugliness**: Greek letters in math-mode Computer Modern colliding with sans-serif text. The canonical preamble's `unicode-math` + `Latin Modern Math` setup fixes the common cases; if specific Greek letters still look wrong, switch to a different math font (Fira Math, STIX Two Math) and recompile.
16. **Caption prose that repeats what labels already show**: the caption should provide context, not re-state every number already in the diagram.
17. **Raw color numbers in the .tex**: any `blue!75!black` that isn't wrapped in a named color like `phHorizon` is a maintenance risk. Replace with the named color.

### When to use the `--review` subcommand

Use `/penrose-diagram --review <file.tex>` as a one-shot rubric application without editing: the skill reads the PDF, applies the rubric, and prints observations + recommended fixes. You then decide whether to apply them. This is the right mode when auditing a diagram authored by someone else, or when you want a second look before committing to edits.

For your OWN authoring, the loop above is the default — don't wait for `--review`, just do it.

### Font Troubleshooting

If a `\textbf{}` or plain text renders as empty (nullfont), your text font is missing a shape. Check with `fc-list | grep -i <fontname>`. The canonical preamble assumes Segoe UI Regular + Bold + Italic + Bold Italic — all four must be present. If any is missing, either:
- Install the missing variant, or
- Fall back to a font with full shape coverage: change `\setmainfont{Segoe UI}` to `\setmainfont{TeX Gyre Heros}` (bundled with TeX Live, always available).

If `\mathscr{I}` renders as a box or nothing: unicode-math's default mapping may not cover script letters in your chosen math font. Fix by adding after `\setmathfont{...}`:
```latex
\setmathfont{STIX Two Math}[range={scr,bfscr}]
```
This routes script glyphs to STIX Two Math which has reliable coverage.

---

## Compilation Prerequisites

This project ships with a working TeX Live 2025 install at `C:\texlive\2025\bin\windows` (on PATH) and a VS Code build configuration at `.vscode/settings.json` pre-wired for LaTeX Workshop. Three compile paths:

**1. VS Code** — Open any `.tex` file, hit `Ctrl+Alt+B` (or just save the file — auto-build is on). LaTeX Workshop uses xelatex by default and drops the PDF next to the source. PDF opens in a side tab. Alternative recipes (pdflatex, latexmk) are available via `Ctrl+Alt+B → Build with recipe`.

**2. Convenience build script** — `figures/penrose/build.sh` runs the full pipeline `.tex → .pdf → .png` in one command:
```bash
./figures/penrose/build.sh                                    # compile all framework-*.tex (PDF + PNG)
./figures/penrose/build.sh framework-B-modulus-space.tex     # compile one file (PDF + PNG)
./figures/penrose/build.sh --pdf-only                        # skip PNG step
./figures/penrose/build.sh --png-only                        # regenerate PNGs from existing PDFs
./figures/penrose/build.sh --clean                           # remove aux, PDFs, and PNGs
```

The PNG step uses `pdftoppm -r 200 -png -singlefile` (pdftoppm ships with TeX Live 2025, already on PATH). 200 DPI gives crisp labels when embedded inline in markdown while keeping file sizes ~70–150 KB per diagram. The PNGs go next to the .tex and .pdf files in `figures/penrose/`, and are referenced from `sessions/framework/Phononic-Penrose-Diagrams.md` and other consuming documents via relative markdown image syntax.

**3. Raw xelatex** — if you want full control:
```bash
xelatex -interaction=nonstopmode -output-directory=figures/penrose figures/penrose/foo.tex
```

**Why xelatex, not pdflatex**: the project's conventional Penrose preamble uses `mathrsfs` for `ℐ⁺` labels and unicode characters (ℐ, Ω, τ) in node text. pdflatex chokes on these; xelatex handles them natively. Both are installed and both work for ASCII-only labels, but xelatex is the default.

**Prerequisite check**: if `xelatex --version` returns a version string, you're good. If it returns "command not found," add `C:\texlive\2025\bin\windows` to your PATH (or reinstall TeX Live from https://www.tug.org/texlive/).

The `standalone` document class produces a PDF cropped to the diagram bounding box, suitable for direct `\includegraphics` in papers.

---

## Canonical Preamble (--preamble)

Every Penrose diagram in this project starts from this preamble. It loads the libraries needed for the entire pattern library below.

```latex
\documentclass[border=3pt,tikz]{standalone}

%% --- Required packages ---
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xfp}                % high-precision floating-point macros
\usepackage[outline]{contour}   % text glow for labels over shaded regions

%% --- Fonts (REQUIRES xelatex or lualatex — not pdflatex) ---
%% Text: Segoe UI (Windows system sans-serif; always available on this box)
%% Math: Latin Modern Math via unicode-math (OpenType, clean metrics,
%%       unified glyph shapes — no more ugly mixed-font Greek letters)
\usepackage{fontspec}
\usepackage{unicode-math}
\setmainfont{Segoe UI}[
  BoldFont       = Segoe UI Bold,
  ItalicFont     = Segoe UI Italic,
  BoldItalicFont = Segoe UI Bold Italic
]
\setmathfont{Latin Modern Math}
% unicode-math provides \symscr; legacy \mathscr is redefined automatically.
% If you need the old mathrsfs script, load it AFTER unicode-math and
% use \symscrhack{...}. Default: \mathscr{I} produces ℐ correctly.

%% --- TikZ libraries ---
\usetikzlibrary{calc}                       % coordinate arithmetic
\usetikzlibrary{decorations.markings}       % markings on paths
\usetikzlibrary{decorations.pathmorphing}   % zigzag, snake (singularities, photons)
\usetikzlibrary{angles,quotes}              % angle arcs with labels
\usetikzlibrary{arrows.meta}                % Latex-style arrowheads
\usetikzlibrary{patterns}                   % hatching for trapped regions
\usetikzlibrary{shadings}                   % horizon glow, ergoregion fade

%% --- Project color palette ---
\colorlet{phHorizon}{blue!75!black}          % event horizon
\colorlet{phCauchy}{purple!70!black}         % Cauchy / inner horizon
\colorlet{phSingularity}{red!85!black}       % curvature singularity
\colorlet{phNullInf}{teal!70!black}          % ℐ⁺ / ℐ⁻
\colorlet{phPointInf}{orange!85!black}       % i⁺, i⁻, i⁰
\colorlet{phPhoton}{orange!50!yellow!95!black}
\colorlet{phAcoustic}{green!55!teal}         % acoustic cone (bi-metric diagrams)
\colorlet{phWorldline}{black!75}
\colorlet{phTrapped}{red!10}                 % trapped-region fill
\colorlet{phNormal}{blue!5}                  % normal-region fill
\colorlet{phErgoregion}{green!15}
\colorlet{phBarrier}{green!55!blue}          % potential-barrier / friction-wall censorship

%% --- Reusable styles ---
\tikzset{
  >={Latex[length=5,width=4]},
  null line/.style       = {phPhoton, line width=0.7},
  photon/.style          = {-{Latex[length=5,width=4]}, phPhoton, line width=0.8,
                            decorate, decoration={snake, amplitude=1.0, segment length=5}},
  horizon/.style         = {phHorizon, line width=1.1},
  cauchy horizon/.style  = {phCauchy, line width=1.0, dashed},
  singularity/.style     = {phSingularity, line width=0.9, decorate,
                            decoration={zigzag, amplitude=2.5, segment length=5}},
  null infinity/.style   = {phNullInf, line width=0.9},
  worldline/.style       = {phWorldline, line width=0.7,
                            decoration={markings, mark=at position 0.5 with {\arrow{Latex}}},
                            postaction={decorate}},
  trapped region/.style  = {fill=phTrapped},
  normal region/.style   = {fill=phNormal},
  ergoregion/.style      = {fill=phErgoregion},
  %% --- Extended pattern set (rolled in from framework/ upgrade pass) ---
  acoustic null/.style   = {phAcoustic, line width=0.7},
  acoustic photon/.style = {-{Latex[length=5,width=4]}, phAcoustic, line width=0.8,
                            decorate, decoration={snake, amplitude=1.0, segment length=5}},
  barrier/.style         = {pattern=north east lines, pattern color=phBarrier,
                            draw=phBarrier, line width=0.8},
  thermal boundary/.style = {phNullInf, line width=0.9, dashed},
  epoch rule/.style      = {black!55, line width=0.5, dashed},
  bcs window/.style      = {fill=phTrapped!60!white, draw=phHorizon!60, line width=0.5},
}

\begin{document}
% \begin{tikzpicture}[scale=2]
%   ...
% \end{tikzpicture}
\end{document}
```

---

## Pattern Library (--patterns)

These are the building blocks. Drop them inside a `tikzpicture` environment that uses the canonical preamble.

### 1. The 45° null grid

Penrose diagrams put light rays at 45° **always**. The simplest way is to define the four corners of the diamond and reference them by name:

```latex
\coordinate (i0)  at ( 4, 0);   % spacelike infinity (right)
\coordinate (im0) at (-4, 0);   % spacelike infinity (left)
\coordinate (ip)  at ( 0, 4);   % future timelike infinity
\coordinate (ipm) at ( 0,-4);   % past timelike infinity

% Conformal boundary (the diamond)
\draw[null infinity] (ipm) -- (i0)  node[midway, below right] {$\mathscr{I}^+$};
\draw[null infinity] (i0)  -- (ip)  node[midway, above right] {$\mathscr{I}^+$};
\draw[null infinity] (ip)  -- (im0) node[midway, above left]  {$\mathscr{I}^-$};
\draw[null infinity] (im0) -- (ipm) node[midway, below left]  {$\mathscr{I}^-$};
```

For Schwarzschild, replace the spacelike-infinity sides with singularities. For dS, the entire boundary is spacelike (top and bottom). For Minkowski, ℐ⁺ and ℐ⁻ flank both sides; the diamond itself is the conformal compactification.

### 2. Five infinity labels

```latex
\node[phPointInf, right=2pt]  at (i0)  {$i^0$};
\node[phPointInf, left=2pt]   at (im0) {$i^0$};
\node[phPointInf, above=2pt]  at (ip)  {$i^+$};
\node[phPointInf, below=2pt]  at (ipm) {$i^-$};
% ℐ± labels go on the sides — see pattern 1
```

If you need both copies of i⁰ (Schwarzschild has two parallel universes), label them `$i^0_R$` and `$i^0_L$`.

### 3. Event horizon as a 45° null line

```latex
% Schwarzschild horizon — null line from bifurcation point to future infinity
\coordinate (B) at (0,0);                 % bifurcation 2-sphere
\coordinate (HRtop) at (2,2);              % right horizon meets singularity
\coordinate (HLtop) at (-2,2);             % left horizon meets singularity
\draw[horizon] (B) -- (HRtop)  node[midway, sloped, above] {$\mathcal{H}^+$};
\draw[horizon] (B) -- (HLtop);
```

### 4. Singularity (zigzag spacelike)

```latex
% Future singularity at r=0 — spacelike, drawn as a horizontal zigzag
\draw[singularity] (HLtop) -- (HRtop)
   node[midway, above=4pt] {$r=0$ (future singularity)};
```

For a *timelike* singularity (Reissner-Nordström, naked singularity), draw it vertically. For a *null* singularity (Cauchy horizon mass inflation), draw it at 45°.

### 5. Cauchy horizon (inner horizon)

```latex
% Reissner-Nordström or Kerr inner horizon — dashed null line
\draw[cauchy horizon] (B) -- (1,3) node[midway, sloped, above] {$\mathcal{H}^-_{\text{inner}}$};
```

### 6. Region shading

```latex
% Region I (right exterior, normal causality)
\fill[normal region] (B) -- (i0) -- (ip) -- cycle;
% Region II (interior, trapped — inside both horizons)
\fill[trapped region] (HLtop) -- (HRtop) -- (B) -- cycle;
% Use the 'phTrapped' color so trapped regions are visually distinct
```

### 7. Worldline of an infalling observer

```latex
\coordinate (start) at (3, -2);
\coordinate (cross) at (1.5, 0.5);  % crosses horizon
\coordinate (end)   at (0.5, 1.7);  % hits singularity
\draw[worldline] (start) .. controls (2.5,-0.5) and (2,1) .. (cross) .. controls (1,1.2) .. (end);
\node[phWorldline, right=2pt] at (start) {$\gamma$};
```

### 8. Photon worldline (snake decoration)

```latex
\draw[photon] (3,-2) -- (0,1);
```

### 9. Killing horizon generators (markings on the horizon)

```latex
\draw[horizon, decoration={markings, mark=between positions 0.2 and 0.8 step 0.2 with {\arrow{Latex}}},
      postaction={decorate}]
  (B) -- (HRtop);
```

### 10. Conformal-factor annotation

```latex
\node[font=\small, align=center] at (0,-3.3)
  {Conformally rescaled coordinates: $u = \tan^{-1}(t-r),\ v = \tan^{-1}(t+r)$};
```

---

## Worked Templates

Each template below is a complete, compilable .tex file. Copy verbatim, save into `figures/penrose/`, run `xelatex`.

### --minkowski (lightcone warmup)

```latex
\documentclass[border=3pt,tikz]{standalone}
\usepackage{amsmath,amssymb,mathrsfs}
\usetikzlibrary{calc,decorations.pathmorphing,arrows.meta}

\colorlet{phPhoton}{orange!50!yellow!95!black}
\tikzset{>={Latex[length=5,width=4]},
  photon/.style={-{Latex[length=5,width=4]}, phPhoton, line width=0.8,
                 decorate, decoration={snake, amplitude=1.0, segment length=5}}}

\begin{document}
\begin{tikzpicture}[scale=1.6]
  \def\R{2.2}
  \draw[->,thick] (-\R,0) -- (\R+0.3,0) node[below] {$x$};
  \draw[->,thick] (0,-\R) -- (0,\R+0.3) node[left]  {$ct$};
  % Light cone
  \draw[photon] (-\R,-\R) -- (-0.05,-0.05);
  \draw[photon] ( \R,-\R) -- ( 0.05,-0.05);
  \draw[photon] ( 0.05, 0.05) -- ( \R, \R);
  \draw[photon] (-0.05, 0.05) -- (-\R, \R);
  % Future and past cones (semi-transparent)
  \fill[phPhoton, opacity=0.08] (0,0) -- (\R,\R) -- (-\R,\R) -- cycle;
  \fill[phPhoton, opacity=0.08] (0,0) -- (\R,-\R) -- (-\R,-\R) -- cycle;
  \node[font=\small] at ( 0, 1.5) {future};
  \node[font=\small] at ( 0,-1.5) {past};
  \node[font=\small] at ( 1.6, 0) {elsewhere};
  \node[font=\small] at (-1.6, 0) {elsewhere};
  \fill (0,0) circle (1.2pt);
\end{tikzpicture}
\end{document}
```

### --schwarzschild (four-region maximal extension)

```latex
\documentclass[border=3pt,tikz]{standalone}
\usepackage{amsmath,amssymb,mathrsfs,xfp}
\usetikzlibrary{calc,decorations.markings,decorations.pathmorphing,arrows.meta}

\colorlet{phHorizon}{blue!75!black}
\colorlet{phSingularity}{red!85!black}
\colorlet{phNullInf}{teal!70!black}
\colorlet{phPointInf}{orange!85!black}
\colorlet{phNormal}{blue!5}
\colorlet{phTrapped}{red!8}
\tikzset{>={Latex[length=5,width=4]},
  horizon/.style={phHorizon, line width=1.1},
  singularity/.style={phSingularity, line width=0.9, decorate,
                      decoration={zigzag, amplitude=2.5, segment length=5}},
  null infinity/.style={phNullInf, line width=0.9}}

\begin{document}
\begin{tikzpicture}[scale=1.4]
  %% Coordinate corners — Kruskal-Szekeres conformal compactification
  \coordinate (iR0)  at ( 3, 0);  \coordinate (iL0)  at (-3, 0);
  \coordinate (iRp)  at ( 3, 3);  \coordinate (iLp)  at (-3, 3);
  \coordinate (iRm)  at ( 3,-3);  \coordinate (iLm)  at (-3,-3);
  \coordinate (B)    at ( 0, 0);              % bifurcation 2-sphere
  \coordinate (Stop) at ( 0, 3);              % future singularity midpoint
  \coordinate (Sbot) at ( 0,-3);              % past singularity midpoint

  %% Region shading
  \fill[phNormal]  (B) -- (iR0) -- (iRp) -- cycle;   % I  (right exterior)
  \fill[phNormal]  (B) -- (iL0) -- (iLp) -- cycle;   % III (left exterior, parallel universe)
  \fill[phTrapped] (B) -- (iRp) -- (iLp) -- cycle;   % II (black hole interior, trapped)
  \fill[phTrapped] (B) -- (iRm) -- (iLm) -- cycle;   % IV (white hole interior, anti-trapped)

  %% Singularities (top and bottom)
  \draw[singularity] (iLp) -- (iRp) node[midway, above=4pt] {$r=0$};
  \draw[singularity] (iLm) -- (iRm) node[midway, below=4pt] {$r=0$};

  %% Conformal infinity (the four ℐ sides)
  \draw[null infinity] (iRm) -- (iR0); \draw[null infinity] (iR0) -- (iRp);
  \draw[null infinity] (iLm) -- (iL0); \draw[null infinity] (iL0) -- (iLp);

  %% Event horizons (the X through the bifurcation point)
  \draw[horizon] (iRm) -- (iLp); \draw[horizon] (iLm) -- (iRp);

  %% Labels
  \node[phPointInf, right=2pt] at (iR0) {$i^0_R$};
  \node[phPointInf, left=2pt]  at (iL0) {$i^0_L$};
  \node[phPointInf, above=2pt] at (iRp) {$i^+$};
  \node[phPointInf, above=2pt] at (iLp) {$i^+$};
  \node[phPointInf, below=2pt] at (iRm) {$i^-$};
  \node[phPointInf, below=2pt] at (iLm) {$i^-$};

  \node[phNullInf] at ( 3.0, 1.5) {$\mathscr{I}^+$};
  \node[phNullInf] at ( 3.0,-1.5) {$\mathscr{I}^-$};
  \node[phNullInf] at (-3.0, 1.5) {$\mathscr{I}^+$};
  \node[phNullInf] at (-3.0,-1.5) {$\mathscr{I}^-$};

  \node[phHorizon] at ( 1.7, 1.3) {$\mathcal{H}^+$};
  \node[phHorizon] at (-1.7, 1.3) {$\mathcal{H}^+$};

  \node[font=\small] at ( 1.8, 0.4) {I};
  \node[font=\small] at (-1.8, 0.4) {III};
  \node[font=\small] at ( 0  , 1.7) {II};
  \node[font=\small] at ( 0  ,-1.7) {IV};

  \fill (B) circle (1.5pt);
  \node[font=\small, below right=1pt] at (B) {bifurcation};
\end{tikzpicture}
\end{document}
```

### --kerr (with Cauchy horizon)

```latex
% --- Same preamble as --schwarzschild plus: ---
% \colorlet{phCauchy}{purple!70!black}
% \tikzset{cauchy horizon/.style={phCauchy, line width=1.0, dashed}}

\begin{tikzpicture}[scale=1.3]
  % Outer block: Region I (right exterior), II (between horizons), III (inside Cauchy horizon)
  % Kerr is infinitely repeating; show ONE block with arrows indicating repetition.
  \coordinate (iR0) at ( 3, 0);  \coordinate (iRp) at ( 3, 3);  \coordinate (iRm) at ( 3,-3);
  \coordinate (B)   at ( 0, 0);
  \coordinate (Cp)  at ( 0, 1.5);  % top of region II = future Cauchy horizon
  \coordinate (Tp)  at ( 0, 3);    % future timelike infinity inside Cauchy horizon
  % Region I shading
  \fill[phNormal] (B) -- (iR0) -- (iRp) -- cycle;
  % Region II (between event and Cauchy horizons)
  \fill[phTrapped] (B) -- (iRp) -- (Cp) -- cycle;
  % Region III (inside Cauchy horizon)
  \fill[phNormal!60] (Cp) -- (iRp) -- (Tp) -- cycle;
  % Conformal infinity
  \draw[null infinity] (iRm) -- (iR0) -- (iRp);
  % Event horizon (outer)
  \draw[horizon] (iRm) -- (iRp) node[midway, sloped, above] {$\mathcal{H}^+$};
  % Cauchy horizon (inner, dashed)
  \draw[cauchy horizon] (B) -- (Cp);
  \draw[cauchy horizon] (Cp) -- (Tp);
  \node[phCauchy, right=2pt] at (Cp) {$\mathcal{H}^-_{\text{inner}}$};
  % Labels
  \node[phPointInf, right=2pt] at (iR0) {$i^0$};
  \node[phPointInf, above=2pt] at (iRp) {$i^+$};
  \node[phPointInf, below=2pt] at (iRm) {$i^-$};
  \node[font=\small] at (1.8, 0.5) {I};
  \node[font=\small] at (1.5, 1.8) {II};
  \node[font=\small] at (1.5, 2.6) {III};
  \node[font=\small, above] at (0, 3.2) {(repeats $\to$ infinitely)};
\end{tikzpicture}
```

### --ds (de Sitter Penrose square)

```latex
\begin{tikzpicture}[scale=1.5]
  \coordinate (BL) at (-2,-1.5);  \coordinate (BR) at (2,-1.5);
  \coordinate (TL) at (-2, 1.5);  \coordinate (TR) at (2, 1.5);
  % Square — top and bottom are SPACELIKE (ℐ⁺ and ℐ⁻ are spacelike in dS)
  \draw[null infinity] (BL) -- (BR) node[midway, below] {$\mathscr{I}^-$ (spacelike)};
  \draw[null infinity] (TL) -- (TR) node[midway, above] {$\mathscr{I}^+$ (spacelike)};
  % Sides (identify left edge with right edge — antipodal)
  \draw[dotted] (BL) -- (TL);
  \draw[dotted] (BR) -- (TR);
  \node[font=\small] at (-2.3, 0) {$\theta=0$};
  \node[font=\small] at ( 2.3, 0) {$\theta=\pi$};
  % Cosmological horizons of an observer at theta=pi/2
  \coordinate (O) at (0,-1.5);
  \draw[horizon] (O) -- (-2, 0.5);
  \draw[horizon] (O) -- ( 2, 0.5);
  \draw[horizon] ( 2, 0.5) -- (0, 1.5);
  \draw[horizon] (-2, 0.5) -- (0, 1.5);
  \node[phHorizon, font=\small] at (-1.0, -0.3) {past horizon};
  \node[phHorizon, font=\small] at ( 1.0,  0.8) {future horizon};
  \fill (O) circle (1.2pt) node[below right] {observer};
\end{tikzpicture}
```

### --ccc (Penrose conformal cyclic cosmology)

```latex
\begin{tikzpicture}[scale=1.2]
  % Two aeons stacked. Each aeon's ℐ⁺ is identified with the next aeon's Big Bang.
  \foreach \dy in {0, 3.2} {
    \coordinate (BL\dy) at (-2,-1.4+\dy);  \coordinate (BR\dy) at (2,-1.4+\dy);
    \coordinate (TL\dy) at (-2, 1.4+\dy);  \coordinate (TR\dy) at (2, 1.4+\dy);
    \fill[phNormal] (BL\dy) -- (BR\dy) -- (TR\dy) -- (TL\dy) -- cycle;
    \draw[null infinity] (BL\dy) -- (BR\dy);
    \draw[null infinity] (TL\dy) -- (TR\dy);
    \draw[dotted] (BL\dy) -- (TL\dy);
    \draw[dotted] (BR\dy) -- (TR\dy);
  }
  % Crossover surface (highlighted)
  \draw[phHorizon, line width=1.4]
      ($(BL3.2)+(0,-0.04)$) -- ($(BR3.2)+(0,-0.04)$);
  \node[phHorizon, font=\small, right=2pt] at (BR3.2) {crossover};
  \node[font=\small] at (0, 0)   {Aeon $n$};
  \node[font=\small] at (0, 3.2) {Aeon $n+1$};
  \node[font=\footnotesize, align=center, below=0.6] at (0,-1.7)
    {Conformal identification: $\mathscr{I}^+_{n}$ glues to Big Bang of Aeon $n+1$};
\end{tikzpicture}
```

### --transit (M4 × SU(3)(τ) modulus-space transit)

This is the framework-specific template. The horizontal direction is τ (Jensen deformation), the vertical is conformal time. The dump point τ ≈ 0.19 is a fold (first-order phase transition); the DNP crossing at τ ≈ 0.285 is where NEC violation provides the escape from the Russo-Townsend no-go.

```latex
\begin{tikzpicture}[scale=1.3]
  %% Axes
  \draw[->,thick] (0,-2.6) -- (0,2.6) node[left]  {conformal time $\eta$};
  \draw[->,thick] (-0.2,0) -- (5.2,0) node[below] {$\tau$ (Jensen deformation)};

  %% τ landmarks
  \draw[dashed] (0.95,-2.5) -- (0.95,2.5) node[above, font=\small] {$\tau_{\text{dump}}{=}0.19$};
  \draw[dashed] (1.42,-2.5) -- (1.42,2.5) node[above, font=\small] {$\tau_{\text{DNP}}{=}0.285$};
  \draw[dashed] (3.9, -2.5) -- (3.9, 2.5) node[above, font=\small] {$\tau\to\infty$ (Kasner)};

  %% Fold — first-order phase transition surface (vertical at τ_dump)
  \draw[horizon] (0.95,-2.5) -- (0.95,2.5);
  \node[phHorizon, font=\footnotesize, rotate=90] at (0.78,0) {fold (1st-order)};

  %% NEC violation strip between dump and DNP (trapped-region styling)
  \fill[phTrapped, opacity=0.6] (0.95,-2.5) rectangle (1.42,2.5);
  \node[font=\footnotesize, align=center] at (1.18,-1.7) {NEC\\violation};

  %% White hole — pre-transit causally disconnected region (Mach 13.75 supersonic)
  \fill[phNormal] (0,-2.5) rectangle (0.95,2.5);
  \node[font=\small] at (0.45,1.5) {pre-transit};
  \node[font=\footnotesize, align=center] at (0.45,-1.5) {acoustic\\white hole};

  %% Post-transit GGE region
  \fill[phNormal!50] (1.42,-2.5) rectangle (3.9,2.5);
  \node[font=\small] at (2.6, 1.5) {post-transit};
  \node[font=\footnotesize, align=center] at (2.6,-1.5) {GGE relic\\$N_{\text{exc}}{=}59.8$};

  %% Kasner singularity at τ → ∞ (right edge)
  \draw[singularity] (3.9,-2.5) -- (3.9,2.5);
  \node[phSingularity, font=\footnotesize, rotate=90] at (4.07,0) {Kasner};

  %% Sample worldline through the transit
  \draw[worldline] (0.3,-2.0) .. controls (0.7,-1) and (0.95,-0.5) .. (0.95,0)
                              .. controls (0.95,0.5) and (1.42,0.7) .. (1.42,1.0)
                              .. controls (1.8,1.4) .. (3.0,1.8);
  \node[phWorldline, font=\footnotesize, right=1pt] at (3.0,1.8) {$\gamma_{\text{transit}}$};

  %% Labels
  \node[font=\footnotesize, align=center, below=0.4] at (2,-2.7)
    {Modulus space transit: pre-transit white hole $\to$ fold $\to$ NEC violation $\to$ GGE relic};
\end{tikzpicture}
```

---

## Subcommand Dispatch

Parse the user's argument from `$ARGUMENTS` (the text after `/penrose-diagram`):

| Subcommand | Action |
|---|---|
| `--help` or empty | Print the Usage block above. Stop. |
| `--preamble` | Print the canonical preamble code block. Offer to save to `figures/penrose/_preamble.tex`. |
| `--patterns` | Print the entire Pattern Library section. |
| `--minkowski` | Print the Minkowski template. Offer to save to `figures/penrose/minkowski.tex`. |
| `--schwarzschild` | Print the Schwarzschild template. Offer to save to `figures/penrose/schwarzschild.tex`. |
| `--kerr` | Print the Kerr template (preamble + tikzpicture). Offer to save to `figures/penrose/kerr.tex`. |
| `--ds` | Print the de Sitter template. Offer to save to `figures/penrose/desitter.tex`. |
| `--ads` | Print the AdS cylinder template (build it from the dS template — replace top/bottom with timelike sides, see Conventions below). Offer to save. |
| `--ccc` | Print the CCC two-aeon template. Offer to save to `figures/penrose/ccc.tex`. |
| `--transit` | Print the M4 × SU(3)(τ) transit template. Offer to save to `figures/penrose/transit.tex`. |
| `--new <name>` | Scaffold `figures/penrose/<name>.tex` with the canonical preamble and an empty tikzpicture. |
| `--check <file>` | Read the file and audit per the Verification Checklist below. |

If the file save target already exists, ask before overwriting.

If the user invokes the skill from inside the SP-geometer agent during a session, save under `sessions/<current-session>/figures/` instead of `figures/penrose/` so the diagram travels with the session work.

---

## Verification Checklist (--check)

When auditing a TikZ Penrose-diagram .tex file, check:

1. **Preamble compliance**
   - `\documentclass[border=3pt,tikz]{standalone}` (or equivalent)
   - `\usepackage{tikz}` plus `\usetikzlibrary{decorations.pathmorphing}` (zigzag) and `\usetikzlibrary{arrows.meta}` (arrowheads)
   - `\usepackage{mathrsfs}` if any `\mathscr{I}` appears

2. **Null lines at exactly 45°**
   - All horizons and ℐ± boundaries should be drawn between coordinates whose Δx and Δy are equal in magnitude.
   - Flag any `\draw[horizon]` whose endpoints don't satisfy this. Conformal compactification REQUIRES null lines at 45°; a 30° "horizon" is wrong.

3. **Conformal infinity labels**
   - Schwarzschild diagrams need TWO copies each of i⁰, i⁺, i⁻, ℐ⁺, ℐ⁻ (right and left exteriors).
   - de Sitter has ℐ⁺ and ℐ⁻ as SPACELIKE top and bottom edges (not null) — flag if drawn at 45°.
   - Anti-de Sitter has TIMELIKE conformal infinity on the sides (vertical edges).

4. **Singularity styling**
   - Use the `singularity` style (zigzag, red). A plain straight line for r=0 is a common error.
   - Spacelike singularity = horizontal zigzag. Timelike = vertical. Null = 45°.

5. **Horizon vs Cauchy horizon**
   - Event horizons: solid thick blue (`horizon` style)
   - Inner / Cauchy horizons: dashed purple (`cauchy horizon` style)
   - Flag any case where both are drawn the same way.

6. **Region shading consistency**
   - Trapped regions should use `phTrapped` (red tint).
   - Normal regions use `phNormal` (blue tint).
   - Anti-trapped regions (white-hole interiors) use `phTrapped` too.
   - Flag any region with no fill — likely an oversight.

7. **Coordinate ordering for `\fill` paths**
   - TikZ fills the path in order; for a region defined by 3-4 corners, the corners must form a simple polygon. If the fill looks like an X, the corner order is wrong.

8. **Math labels in math mode**
   - `$\mathscr{I}^+$` not `\mathscr{I}^+` (raw)
   - `$\mathcal{H}^+$` not `H^+`

Report each violation with its line number and a one-line fix suggestion.

---

## Project Conventions

- **Save location**: `figures/penrose/<descriptive-name>.tex`. Output PDFs are gitignored; .tex sources are tracked.
- **File naming**: lowercase with hyphens, e.g., `schwarzschild-maximal.tex`, `transit-su3-fold.tex`, `ccc-aeon-glue.tex`.
- **Compilation**: prefer `xelatex` for unicode label safety. Single-file standalone class for individual figures; for multi-figure papers, set `tikz` package option `external` to cache compiled figures.
- **Inclusion in papers**: `\includegraphics{figures/penrose/foo}` (no extension; standalone produces foo.pdf). Wrap in a `figure` environment with `\caption` and `\label{fig:foo}`.
- **Color palette**: use the `phHorizon`, `phSingularity`, etc. colors from the canonical preamble for cross-figure consistency. Do NOT introduce new colors per figure unless the new color carries semantic meaning.
- **Coordinate scale**: use `[scale=1.4]` for standalone figures (~5cm wide). Adjust for two-column journal layout by changing only the scale, not the internal coordinates.
- **AdS note**: for AdS, use `phNullInf` color but draw conformal infinity as TIMELIKE side edges. The dS template's top/bottom become AdS's left/right, and the space inside is a vertical strip.

---

## Anti-Patterns

Things to NOT do (these are actual mistakes from prior auto-generated diagrams):

- **Drawing horizons with `\draw[blue, thick]`** — use the `horizon` style so all diagrams share one visual language.
- **Drawing the singularity as a plain line** — without the zigzag decoration, it looks like a coordinate boundary, defeating the diagram's purpose.
- **Forgetting to fill regions** — empty diagrams read as contour plots; the trapped/normal coloring is what makes the causal structure jump out.
- **Putting i⁰ at the top of the diamond** — i⁰ is SPACELIKE infinity (sides), not timelike (top/bottom). i⁺ is at the top.
- **Calling Schwarzschild "Region I, II, III" without saying which is the black hole interior** — always label II as the trapped region inside the future horizon.
- **Drawing Kerr Penrose diagrams as if they're Schwarzschild** — Kerr has an INFINITE tower of regions because of the inner Cauchy horizon; show at least one block with an arrow indicating repetition.
- **Drawing a CCC diagram with smooth top-to-bottom transition** — the crossover IS a discontinuity in proper time even though it's smooth conformally; mark it with `phHorizon` width 1.4.
- **Mixing units between coordinates and labels** — keep everything in TikZ default cm. Don't switch to pt or mm mid-diagram.

---

## References

- Hawking & Ellis, *The Large Scale Structure of Space-Time* (1973) — canonical Penrose-diagram conventions
- Wald, *General Relativity* (1984) — Chapter 11 on conformal compactification
- This project's library: `researchers/Schwarzschild-Penrose/index.md` — papers 21 (Lemos-Silva maximal extension), 23 (Friedrich conformal Einstein evolution), 25 (Carroll-Johnson-Randall dynamical compactification with Penrose diagrams), 11 (Meissner-Penrose CCC) all contain published Penrose diagrams worth studying as targets.
- TikZ manual, CTAN (https://ctan.org/pkg/pgf) — full TikZ reference
- Project TikZ primer: `.claude/templates/LaTeX/08_TikZ_PGF_Scientific_Diagrams.md` — general scientific TikZ patterns (Feynman, eigenvalue, commutative — NOT Penrose-specific)

## Future Extensions

- Add `--higher-d-bh` template for Myers-Perry / black ring causal structure (5D)
- Add `--gl-pinch` template for Gregory-Laflamme black-string pinch-off
- Add `--bon` template for Witten bubble of nothing
- Add 3D `--3d-transit` template using `tikz-3dplot` once we need to show the SU(3) fiber explicitly
- Add `--export-svg` option for web-rendered diagrams via `dvisvgm`
