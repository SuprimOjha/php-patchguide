# Architecture

## Data flow

1. The CLI validates arguments and selects a project path.
2. Project inspection reads selected Composer metadata, PHP filenames, Dockerfile tags, version pins, and INI settings. It can run `php -v` with a timeout to identify the local CLI runtime.
3. The advisory loader validates local JSON records. Version-based records require branch-specific fixed releases; mitigation-only records explicitly do not claim a fixed version.
4. The evaluator compares numeric versions or interprets observed INI settings for mitigation guidance.
5. Report builders produce text and JSON. Optional exit policies let CI fail on affected, unknown, or mitigation-required results.

## Safety boundaries

Local checks do not execute application PHP, modify project files, make network requests, or upload project data. The scheduled monitor is separate: it fetches the public PHP archive and creates a snapshot for human review.

## Evidence limits

CLI version is not proof of the serving runtime. A repository INI file may not be loaded in production. Static scanning cannot reliably infer runtime `ini_set()` calls, effective per-worker configuration, vendor backports, or every vulnerability. Treat findings as evidence to investigate, not a certification that an application is safe.
