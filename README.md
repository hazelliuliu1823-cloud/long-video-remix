# Long Video Remix

**A structured workflow for controllable AI video editing.**

Turn long-form video into reusable structured evidence, human-directed editorial decisions, and executable edit plans — without letting the agent silently change what has already been approved.

> **Structure the source. Direct the story. Execute the edit.**

---

## What is Long Video Remix?

Long Video Remix is an AI-native workflow for understanding, planning, and executing edits from long-form video.

Instead of asking an AI agent to repeatedly watch the source, decide what matters, and edit everything in one pass, Long Video Remix separates the work into three layers:

**Structure → Direct → Execute**

- **Structure** turns long-form footage into searchable, traceable observations and evidence.
- **Direct** keeps narrative and editorial decisions under human control.
- **Execute** turns approved decisions into a verifiable editing package for rendering and QA.

The goal is not to replace editorial judgment with automation.

The goal is to make AI-assisted video editing **reusable, traceable, controllable, and executable**.

---

## Why Long Video Remix?

Long-video editing agents often fail in predictable ways.

They may:

- repeatedly re-read expensive multimodal source material;
- confuse sampled observations with verified events;
- treat subtitles or ASR as if they were confirmed original audio;
- cut dialogue, reactions, or actions too early;
- lose context when moving from analysis to editing;
- change previously approved editorial decisions during execution;
- generate timelines that are difficult to trace back to source evidence;
- pass technical checks while still producing a poor edit.

Long Video Remix turns those problems into explicit workflow stages, structured evidence, protected ranges, authorization checks, timeline validation, and QA.

---

## Core idea

Long-form video is expensive to understand repeatedly.

Instead of loading the same source footage every time the creative direction changes, Long Video Remix first converts the source into a **compact, searchable, reusable structured layer**.

Creative work can then operate primarily on that structured layer.

Only the selected regions are examined again at high density.

Once the editorial direction is confirmed, the final plan is compiled into an executable timeline with evidence binding and integrity checks.

In short:

```text
Long-form source
      ↓
Broad Structure
      ↓
Reusable Structured Observation Layer
      ↓
Direct 1 — Narrative Direction
      ↓
Directed Deep / Detail Structure
      ↓
Direct 2 — Editorial Execution Plan
      ↓
Execute
      ↓
Render / QA
```

---

## What makes it different?

| Principle | How Long Video Remix handles it |
|---|---|
| **Reuse before re-reading** | Broad Structure creates a reusable content layer so later work does not need to repeatedly reload the full video |
| **Observation before interpretation** | Facts, interpretations, unknowns, and evidence are kept separate |
| **Human direction stays explicit** | Narrative decisions happen in two Direct stages instead of being hidden inside execution |
| **Deep analysis is selective** | High-density multimodal analysis is concentrated only on candidate regions |
| **Source evidence remains traceable** | Structured records retain frame IDs, timestamps, scene IDs, and evidence references |
| **Cuts respect semantic and action boundaries** | `protected_ranges`, edit boundaries, audio continuity, and must-keep ranges constrain execution |
| **Approved decisions are protected** | Execution authorization and integrity checks prevent silent editorial drift |
| **Technical success is not final approval** | Rendering, decoding, silence checks, cut inspection, and human watch-through remain separate QA layers |

---

# Quick Start

## 1. Clone the repository

```bash
git clone <repository-url>
cd long-video-remix
```

## 2. Create a project

Copy the project template:

```text
assets/project-template.json
```

into a separate working project directory and register:

- source media;
- source version information;
- available multimodal models;
- ASR / subtitle sources;
- video tools or MCPs;
- rendering environment.

---

## 3. Run Broad Structure

Broad Structure creates the reusable observation layer.

Typical outputs include:

```text
frames.jsonl
frame-observations.csv
action-node-candidates.csv
structure-questions.csv
overview.md
content-map.md
```

If your task only requires structured video understanding, search, research, or content analysis, the workflow may stop here.

---

## 4. Confirm Narrative Direction

Direct 1 determines:

- what the edit is trying to say;
- the narrative spine;
- candidate regions;
- questions that Detail Structure still needs to verify;
- confirmed editorial decisions;
- protected creative constraints.

Direct 1 should not pretend that candidate material has already been fully verified.

---

## 5. Run Directed Deep / Detail Structure

Only the selected regions are examined at higher density.

This stage verifies:

- continuous visual context;
- original audio;
- dialogue completeness;
- speaker attribution;
- action and reaction boundaries;
- before / after state;
- supporting and contradicting evidence;
- safe edit boundaries;
- `context_ranges`;
- `protected_ranges`.

---

## 6. Confirm the Editorial Execution Plan

Direct 2 decides:

- which verified units are finally selected;
- their order;
- narrative function;
- dialogue / action that must remain complete;
- text treatment;
- sound treatment;
- transitions;
- timing allocation;
- what may be changed;
- what must not be changed.

Final material selection belongs here.

Execute should not independently rewrite the editorial direction.

---

## 7. Validate and compile

```bash
python3 scripts/validate_project.py PROJECT

python3 scripts/compile_render_manifest.py PROJECT

python3 scripts/check_render_authorization.py \
  PROJECT \
  PROJECT/render-manifest.json
```

The repository provides:

- project validation;
- timeline compilation;
- execution authorization;
- evidence binding;
- source-range validation;
- render-manifest generation;
- export auditing.

Actual media rendering may be handled by FFmpeg, a video MCP, editing software, or another renderer adapter.

---

## 8. Render and audit

After rendering:

```bash
python3 scripts/audit_render.py \
  OUTPUT.mp4 \
  PROJECT/render-manifest.json \
  --outdir AUDIT_DIR \
  --contacts
```

Rendering success alone does not mean the edit has passed final review.

---

# Workflow

## Stage 1 — Broad Structure

Broad Structure prioritizes **coverage**.

Its job is not to produce the final edit.

Its job is to make a long, difficult-to-browse multimodal source usable by humans and agents.

Typical work includes:

- registering source media and versions;
- sampling the full video;
- collecting subtitle / ASR coverage;
- identifying scenes and segments;
- observing visual facts;
- recording actions and state changes;
- capturing visible text;
- recording emotional or relational signals carefully;
- tracking uncertainties;
- generating source-order overview;
- building the Content Map.

Broad Structure should preserve enough detail that later work can search and reason over the video without constantly reopening the source.

---

# Structured Observation Layer

The Structured Observation Layer is the core reusable output of Structure.

It should not collapse into a short summary.

For each analyzed or sampled frame, the project may preserve information such as:

- frame ID;
- source timestamp;
- scene / segment ID;
- visual facts;
- person positions;
- action / state;
- facial expression or gaze;
- spatial relationships;
- objects;
- visible text;
- motif tags;
- audio notes;
- change from previous frame;
- content description;
- interpretation;
- uncertainty;
- evidence basis;
- topic judgment.

The purpose is not to claim that every 25 / 30 fps source frame has been semantically analyzed.

“Frame-level” here means **each analyzed / sampled frame**.

---

## Action Node Candidates

Important movement or relational changes should not remain buried inside general observations.

Candidate events such as:

- gaze changes;
- standing / sitting transitions;
- object handoffs;
- physical approach;
- separation;
- embrace;
- turning away;
- entrance / exit;
- visible reaction;

may enter a separate action-node table.

High-value nodes can then be inspected using denser local sampling, for example around a 4 fps window.

This allows the system to distinguish:

> “something changed around here”

from:

> “this is the actual start, peak, and completion of the action.”

---

## Structure Questions

Important uncertainties should be explicit.

Examples:

- Who is speaking?
- Is the subtitle synchronized with the original audio?
- Did this reaction happen before or after the dialogue?
- Is this scene causally connected to the previous one?
- Does the candidate clip omit important context?
- Is a relationship interpretation supported by observable evidence?

Questions, answers, evidence, unresolved items, and follow-up requirements should be recorded rather than silently resolved through assumption.

---

# Content Map

The Content Map sits above the observation layer.

It is a creative navigation layer, not a replacement for raw observations.

It may organize:

- scenes;
- people;
- recurring actions;
- emotional shifts;
- relationships;
- objects;
- motifs;
- important dialogue;
- visual callbacks;
- unresolved questions;
- candidate storylines.

A Content Map helps a Director or another model explore the material without loading the complete source again.

---

# Direct 1 — Narrative Direction

The first Direct stage answers:

> **What are we trying to say?**

It consumes:

- Broad Structure;
- frame observations;
- action nodes;
- Structure Q&A;
- scenes;
- overview;
- Content Map;
- relevant external research if needed.

Outputs may include:

- core proposition;
- audience relationship;
- Narrative Spine;
- candidate scenes;
- candidate regions;
- expected emotional progression;
- verification questions;
- confirmed creative constraints.

Direct 1 is intentionally separate from Detail Structure.

At this stage, creative direction can use structured evidence, but it should not turn unverified assumptions into verified source facts.

A suggested template is:

```text
assets/narrative-direction-template.md
```

---

# Directed Deep / Detail Structure

Once the direction is known, the workflow returns to the original media.

This stage prioritizes **completeness and verification**, not coverage.

Instead of deeply analyzing the
