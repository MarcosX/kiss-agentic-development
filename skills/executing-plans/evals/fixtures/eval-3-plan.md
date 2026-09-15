# Search Feature Implementation Plan

**Goal:** Add full-text search across skill content.

---

## Task 1: Search index building

**Status:** DONE

**Category:** Coding

**Files:**

- Create: search.py

**Contract:**

- `build_index(content_dir: str) -> dict[str, list[str]]` scans `content_dir` recursively for `.md` files and returns a dict mapping each normalized term to the list of file paths containing it.
- Terms are normalized by lowercasing and splitting on any run of non-alphanumeric characters.
- The returned dict MUST include files in nested subdirectories, not only the top level.
- Edge case: an empty or nonexistent content dir returns an empty dict.

**Done when:** contract behavior verified through the test-first loop; full suite passes.

## Task 2: Search query endpoint

**Status:** DONE

**Category:** Coding

**Files:**

- Create: search_api.py

**Contract:**

- `app` is a FastAPI application exposing `POST /search`.
- Request body is JSON `{"query": "<term>"}`; query matching is case-insensitive.
- Returns HTTP 200 with JSON body `{"results": ["<file-path>", ...]}` listing files whose index contains the query term.
- Unknown or empty query returns HTTP 200 with JSON body `{"results": []}`.

**Done when:** contract behavior verified through the test-first loop; full suite passes.

## Task 3: Advanced search filters

**Status:** BLOCKED — depends on external search library decision not yet made

## Task 4: Search result ranking

**Status:** UNSTARTED — blocked by Task 3
