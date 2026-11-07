# Campus

Campus helps store projects in a systematic, well-organized order using categories and timestamps.

## Usage

Create a project entry:

```bash
python organizer.py add "Project Name" --category "Category Name" --description "Optional description"
```

This creates a folder in the structure:

```text
projects/<category>/<YYYY-MM-DD>/<YYYYMMDDTHHMMSSZ>-<project-name>/
```

Each project folder contains `metadata.json`.

List stored projects:

```bash
python organizer.py list
```