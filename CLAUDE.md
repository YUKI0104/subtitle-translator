# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-file HTML application (`index.html`, 6050 lines / 281KB) for translating short-drama subtitles with AI. Pure client-side, no build step, no server, no dependencies. Run directly in browser via `file://` or any static HTTP server.

## File Structure

| File | Purpose |
|---|---|
| `index.html` | The entire application (CSS lines 8–487 · HTML 488–855 · JS 856–6050) |
| `version.json` | Version metadata for update checking (`APP_VERSION` constant also in JS line 857) |
| `CLAUDE.md` | This file |
| `_fix_*.py` | One-off Python scripts used for specific past edits — not part of the app |
| `korean-minimal-*` | Design exploration artifacts, not part of the active app |
| `skills/` | Claude Code skill definitions |

## Development

```bash
# No build step — just open in browser
python3 -m http.server 8000      # then open http://localhost:8000
# or
npx serve .                       # if you prefer
```

No tests, no linter, no package.json, no build pipeline. Manual QA only.

## Key Architecture (JS lines 856–6050)

### State Model (line 862)

Global `state` object:
- `projects[]` — Array of projects
- `activeProjectIdx`, `activeEpisodeIdx` — Current selection
- `phase` — Workflow phase: `editing → proofreading → review → submitted`

Per project:
- `episodes[]` — Each has `subtitles[]` (array of `{index, startMs, endMs, text, translation, status, styleName}`)
- `glossary[]` — Project-scoped glossary (synced to project's `glossary.tbx`)
- `memoryBank[]` — Translation memory (synced to libraries dir's `memory.tbx`)
- `globalGlossary[]` — Global glossary (synced to libraries dir's `glossary.tbx`)
- `knowledgeBase[]` — Knowledge base entries (synced to `*.md` files in libraries dir)

State persisted to `localStorage` under key `st_state`; also serializable to `project.json` for folder-backed projects.

### Key JS Sections (line-number anchored)

| Section | Lines | Description |
|---|---|---|
| Constants & Globals | 857–884 | `APP_VERSION`, `state`, `PHASES`, `STATUS_LABELS`, CPS_LIMIT, dir handles |
| Init & Persistence | 998–1060 | `initDefault()`, `saveState()`, `markDirty()` (500ms debounced auto-save) |
| Sidebar Panel System | 1062–1635 | `switchSidebar()`, `renderSidebarPanel()` dispatches to 5 panels |
| Dashboard Panel | 1635–1725 | Overview counts, status, save/load/new folder actions |
| Episodes Panel | 1090–1120 | Episode list in sidebar |
| **Libraries Panel** | 1121–1193 | 4 library cards + dir config UI |
| Library Dir Picker | 1195–1210 | `pickLibrariesDir()` via File System Access API |
| Library Disk Loading | 1212–1250 | `loadLibrariesFromDisk()` — reads TBX/MD files |
| AI Settings Panel | 1252–1628 | Platform selection, model config, task definitions |
| Tools Panel | 1629–1634 | (deprecated, shows migration notice) |
| Library Modal | 1827–2205 | 4-tab modal (记忆库/全局术语库/项目术语库/知识库) with add/delete/import/search |
| **TBX Utilities** | 2207–2289 | `_tbxEscape`, `_tbxBuild`, `_tbxParse`, `loadTBX`, `saveTBX` |
| **MD Utilities** | 2293–2346 | `loadKnowledgeMD`, `saveKnowledgeMD`, `deleteKnowledgeMD` |
| **File Sync** | 2351–2381 | `saveMemoryBankToFile`, `saveGlobalGlossaryToFile`, `saveProjectGlossaryToFile` |
| Phase Workflow | 2384–2425 | 4-stage pipeline with clickable phase steps |
| Subtitle Parsing | 2467–2865 | `parseSRT()`, `extractTags()`, `parseASS()`, `parseASSStyles()` |
| Folder Project I/O | 2936–3265 | `importFolder()`, `openProjectFromFolder()`, `saveProjectToFolder()`, `createProjectInFolder()`, `readDirFiles()`, readDirVideoFiles, unbind |
| CAT Table | 3280–3515 | `renderSubtitles()` — the main editing grid with contenteditable cells |
| Video Player | 3532–3790 | Video element, seek bar, playback controls, segment looping |
| AI Platforms | 3872–4340 | Built-in platform definitions (DeepSeek, OpenAI, GLM, etc.) |
| Custom Platforms | 4351–4760 | User-defined API platforms, balance check, model fetching |
| Model Config | 1450–1600 | Per-task model selection, key visibility toggle, platform picker |
| Term Extraction | 4817–5163 | Local n-gram extraction + AI term extraction flow |
| Bulk Translation | 5171–5500 | Term translate flow with confirmation modal, batch episode translate |
| Translation Engine | 5368–5515 | `translateAll()` — progressive batch translation |
| Batch Translate | 5527–5626 | Cross-episode batch translation modal |
| Batch Translate Core | 5614–5780 | `batchTranslateEpisodes()` — multi-episode AI translation with marker-based result parsing |
| Export | 5825–5975 | SRT/ASS export with mode (all/draft/confirmed) and range options |
| Settings | 5983–6035 | `loadSettings()`, `saveSettings()`, font size, language, video panel width |

### File Persistence — Library System

**Directory layout** (user picks once via `showDirectoryPicker()`):

```
/downloads/Dramalator/            ← Libraries dir (_librariesDirHandle)
├── memory.tbx                    ← 记忆库 (TBX)
├── glossary.tbx                  ← 全局术语库 (TBX)
├── how-to-translate.md           ← 知识库 (any .md files)
├── style-guide.md
└── 项目/                         ← Project dir (_projectDirHandle)
    ├── project.json
    ├── glossary.tbx              ← 项目术语库 (TBX)
    └── subtitles...
```

**TBX format**: Minimal valid TBX (TermBase eXchange) XML with `<martif>`, `<termEntry>`, `<langSet>`, `<tig>`, `<term>` elements. Each entry: `{id, source, target}`.

**MD format**: Each knowledge-base entry is one `.md` file. The filename (with `.md` removed) is the entry's display title.

**Fallback**: When no library/project directory handles are available, all data works in-memory and serializes to localStorage/project.json.

### Effect Tag System

ASS effect tags (`\k`, `\pos`, `\fad`, etc.) extracted to `{t1}`, `{t2}` style placeholders in source text → rendered as 🏷️ `T1`, `T2` chips. Translation column shows same placeholders; restored on export.

### AI Translation Flow

1. Batch subtitles according to model's context budget (CPS_LIMIT=15, per-model limits in `MODEL_CONTEXT_LIMITS` at line 4763)
2. Send to OpenAI-compatible API with glossary as few-shot examples
3. Parse response — supports markers `[E{n}][{m}]` for parallel translation, with positional fallback for unmarked lines
4. Apply translation to subtitle rows, set status = 'draft'
5. Try fallback model on 401 errors

### Subtitling Data Flow

1. Load subtitles (SRT/ASS file drag-drop, or folder import) → parse → create episodes
2. Each subtitle row rendered in CAT table (source + editable translation)
3. User translates manually, via term extraction + batch term translate, or full AI translation
4. Export as SRT or ASS (with effect tags restored)
5. State persisted to localStorage and/or `project.json` in folder

## Important Gotchas

- **Edit tool often fails on large CSS/JS blocks** due to match uniqueness issues. For big changes, use Python scripts or `sed` to make targeted string replacements. Always verify with `node -e "new Function(scriptContent)"` after any JS structural change.
- `Edit` tool `old_string` must match file exactly including indentation. Use a Read first.
- Single-file means CSS selectors can conflict — use specificity carefully.
- ASS parsing regex is fragile — unusual ASS syntax may break.
- File System Access API requires secure context (localhost or HTTPS).
- `_projectDirHandle` and `_librariesDirHandle` are session-scoped globals (line 3546–3547). Directory names persisted in localStorage (`st_lastFolder`, `st_librariesDir`) for display, but handles must be re-acquired on refresh.
- Library file operations (`saveTBX`, `saveKnowledgeMD`) are async and called on every add/delete.
- Chinese numeral sorting for episode names uses `extractNumber()`.
