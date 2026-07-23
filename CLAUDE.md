# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-file HTML application (`index.html`, ~8700 lines / 404KB) for translating short-drama subtitles with AI. Pure client-side, no build step, no server, no dependencies. Run directly in browser via `file://` or any static HTTP server.

**App name:** Dramalator (title in `<head>`)
**Version:** `APP_VERSION` constant at line 1602, also in `version.json`

## File Structure

| File | Purpose |
|---|---|
| `index.html` | Entire application (CSS lines 8–1143, HTML 1146–1599, JS 1601–8721) |
| `version.json` | Version metadata for update checking |
| `CLAUDE.md` | This file |
| `_fix_*.py` | One-off Python scripts for targeted edits — not part of the app |
| `korean-minimal-*` | Design exploration artifacts, not part of the active app |
| `kuaipao-worker.js` | Cloudflare Worker proxy for kuaipao.pro API (CORS bypass) |
| `kuaipao-deno.ts` | Deno variant of the kuaipao proxy |
| `server.py` | Local dev server with CORS proxy for kuaipao.pro |
| `skills/` | Claude Code skill definitions |

## Development

```bash
# No build step — just open in browser
python3 -m http.server 8000      # then open http://localhost:8000
# or
npx serve .                       # if you prefer
```

No tests, no linter, no package.json, no build pipeline. Manual QA only.

## Key Architecture (JS lines 1601–8721)

### State Model (line 1762)

Global `state` object with `_saveDirty` flag for debounced persistence:

```js
const state = {
  projects: [],           // Array of project objects
  activeProjectIdx: -1,
  activeEpisodeIdx: -1,
  sidebarTab: 'dashboard',  // 'dashboard' | 'episodes' | 'aisettings'
  sidebarOpen: true,
  phase: 'editing',         // editing → proofreading → review → submitted
  // search, filter, currentSubIdx, _saveDirty
};
```

Each project object:
- `episodes[]` — Each has `subtitles[]` (array of `{index, startMs, endMs, text, translation, status, styleName}`)
- `glossary[]` — Project-scoped glossary (synced to project's `glossary.tbx`)
- `memoryBank[]` — Translation memory (synced to libraries dir's `memory.tbx`)
- `globalGlossary[]` — Global glossary (synced to libraries dir's `glossary.tbx`)
- `knowledgeBase[]` — Knowledge base entries (synced to `*.md` files in libraries dir)
- `projectDirName` — Tracks which folder a project is bound to (prevents cross-contamination)

### Key JS Sections (line-number anchored)

| Section | Lines | Description |
|---|---|---|
| IndexedDB handle persistence | 1603–1662 | Store/load/delete File System Access handles |
| Language utilities | 1663–1759 | Language picker, TBX language mapping |
| State model & init | 1762–2002 | `state`, `PHASES`, `initDefault()`, `saveState()`, `markDirty()` |
| Sidebar panel system | 2014–2139 | `switchSidebar()`, `renderSidebarPanel()` → 3 panels |
| Libraries modal | 2923–3784 | 4-tab modal (memory/globalGlossary/projectGlossary/knowledge) with add/delete/import |
| **Theme system** | 2954–3016 | 8 themes (4 pairs × day/night), follow-system, `applyTheme()` |
| TBX utilities | 3787–3999 | `_tbxBuild`, `_tbxParse`, `loadTBX`, `saveTBX`, knowledge MD helpers |
| **Memory bank system** | 4001–4249 | Auto-matching, promotion, file sync to memory.tbx |
| Phase workflow | 4253–4293 | 4-stage pipeline with clickable phase steps |
| Subtitle parsing | 4336–4770 | `parseSRT()`, `extractTags()`, `placeholderToTag()`, `parseASS()`, `parseASSStyles()` |
| Folder project I/O | 4923–5192 | `importFolder()`, `openProjectFromFolder()`, `saveProjectToFolder()`, `createProjectInFolder()`, `readDirFiles()` |
| CAT Table | 5263–5484 | `renderSubtitles()` — contenteditable grid, memory highlighting, style display |
| Video Player | 5709–5864 | Video element, seek bar, playback controls, segment looping |
| AI Platforms | 6012–6393 | Built-in platform definitions (DeepSeek, OpenAI, GLM, etc.) with pricing |
| Custom Platforms | 6722–7116 | User-defined API platforms, balance check, model fetching |
| Term Extraction | 7142–7624 | Local n-gram extraction + AI term classification flow |
| AI Translation | 7722–8428 | `translateAll()` — progressive batch, marker-based result parsing, batch cross-episode |
| Export | 8439–8628 | SRT/ASS export with mode (all/draft/confirmed) and range options |
| Settings | 8629–8721 | Font size, language, video panel width, video skip mode |

### Theme System (line 2954)

CSS variable-based theming with 8 theme blocks (`:root.theme-1` through `.theme-8`):
- **Theme pairs:** 1=暖煦, 2=青岚, 3=赛博, 4=墨韵 (each with day/night variant)
- Variant calculation: `n = (pair - 1) * 2 + (dark ? 2 : 1)`
- `_followSystem` checkbox enables `prefers-color-scheme` media query
- Theme name mapping: `['暖煦日','暖煦夜','青岚日','青岚夜','赛博日','赛博夜','墨韵日','墨韵夜']`

### Effect Tag System

ASS effect tags (`\k`, `\pos`, `\fad`, etc.) extracted to `{T1}`, `{T2}` placeholders in source text → rendered as `🏷️ T1`, `T2` chips in CAT table. Translation column shows same placeholders. **On ASS export:** placeholders restored to original tags. **On SRT export:** both placeholders and tags stripped, leaving plain text.

Key functions: `extractTags()` (line 4373), `placeholderToTag()` (line 4382)

### File Persistence — Library System (lines 2067–2139)

User picks a libraries directory once via `showDirectoryPicker()`. Directory layout:

```
/user-chosen-dir/          ← Libraries dir (_librariesDirHandle)
├── memory.tbx             ← Translation memory
├── glossary.tbx           ← Global glossary
├── how-to-translate.md    ← Knowledge base (any .md files)
└── project-dir/           ← Project dir (_projectDirHandle)
    ├── project.json       ← Full project state
    ├── glossary.tbx       ← Project glossary
    └── subtitles...
```

TBX format: Minimal valid TermBase eXchange XML with `<martif>`, `<termEntry>`, `<langSet>`, `<tig>`, `<term>` elements. MD format: each entry is one `.md` file; filename (without `.md`) is the display title.

**Two persistence layers:**
1. `localStorage` key `st_state` — saves all projects (via `saveState()`, debounced 500ms via `markDirty()`)
2. `project.json` file in project folder (via `saveProjectToFolder()`) — only saves `activeProject()` to `_projectDirHandle`

**Critical:** `_projectDirHandle` is a global variable. Switching projects clears it (`_projectDirHandle = null` in `switchProject()`) to prevent auto-save from writing wrong project data into a folder. Per-project `projectDirName` field enables safe folder matching in `saveState()`.

### AI Translation Flow

1. Batch subtitles according to model's context budget (CPS_LIMIT=15, per-model limits in `MODEL_CONTEXT_LIMITS`)
2. Send to OpenAI-compatible API with glossary as few-shot examples
3. Parse response — supports markers `[E{n}][{m}]` for parallel translation, with positional fallback for unmarked lines
4. Apply translation to subtitle rows, set status = 'draft'
5. Try fallback model on 401 errors

### Important Gotchas

- **Edit tool often fails on large CSS/JS blocks** due to match uniqueness issues. For big changes, use Python scripts or `sed` to make targeted string replacements. The repo already has `_fix_*.py` examples.
- `Edit` tool `old_string` must match file exactly including indentation. Use `Read` first, then copy verbatim.
- **Indentation in index.html is mixed:** some sections use 2-space indent, others use tabs. Always check with `python3 -c "print(repr(line))"` before editing.
- Single-file means CSS selectors can conflict — use specificity carefully.
- ASS parsing regex is fragile — unusual ASS syntax may break.
- File System Access API requires secure context (localhost or HTTPS).
- `_projectDirHandle` and `_librariesDirHandle` are session-scoped globals (line 5726–5727). Directory names persisted in localStorage for display, but handles must be re-acquired on refresh.
- Library file operations (`saveTBX`, `saveKnowledgeMD`) are async and called on every add/delete.
- Chinese numeral sorting for episode names uses `extractNumber()`.
- The `kuaipao-worker.js` and `kuaipao-deno.ts` files are server-side proxies and are NOT part of the single-file app — they deploy separately to Cloudflare Workers / Deno. `server.py` is a local dev alternative.
