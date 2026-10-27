"""Read-only PHP project and local runtime discovery."""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "vendor", "__pycache__", "dist", "build"}
CONFIG_NAMES = {"php.ini", ".user.ini"}


def _read(path, limit=1000000):
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def detect_cli_php_version():
    exe = shutil.which("php")
    if not exe:
        return {"available": False, "version": None, "executable": None, "source": "PATH"}
    try:
        result = subprocess.run([exe, "-v"], capture_output=True, text=True, timeout=4, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return {"available": False, "version": None, "executable": exe, "source": "php -v"}
    match = re.search(r"PHP\s+(\d+\.\d+\.\d+(?:[-+][\w.-]+)?)",
                      (result.stdout or "") + "\n" + (result.stderr or ""))
    return {"available": result.returncode == 0 and bool(match),
            "version": match.group(1) if match else None,
            "executable": exe, "source": "php -v"}


def _parse_ini_setting(text, key):
    found = []
    pattern = re.compile(r"^\s*" + re.escape(key) + r"\s*=\s*([^;#\s]+)", re.I)
    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith((";", "#")):
            continue
        match = pattern.match(line)
        if match:
            found.append(match.group(1).strip().strip('"\'').lower())
    return found[-1] if found else None


def inspect_project(path="."):
    root = Path(path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Project path is not a directory: {root}")
    files = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            if (name.endswith(".php") or name.endswith(".ini") or name in {
                "composer.json", "composer.lock", "Dockerfile", ".php-version",
                ".tool-versions", "compose.yaml", "compose.yml", "docker-compose.yml"
            }):
                files.append(Path(current) / name)
        if len(files) >= 10000:
            break

    cp = root / "composer.json"
    composer, error = {}, None
    if cp.is_file():
        try:
            parsed = json.loads(_read(cp))
            if isinstance(parsed, dict):
                composer = parsed
            else:
                error = "composer.json root must be an object"
        except json.JSONDecodeError as exc:
            error = f"Invalid composer.json: {exc.msg}"
    config = composer.get("config", {})
    platform = config.get("platform", {}) if isinstance(config, dict) else {}
    if not isinstance(platform, dict):
        platform = {}
        error = error or "composer.json config.platform must be an object"
    req = composer.get("require", {})
    if not isinstance(req, dict):
        req = {}
        error = error or "composer.json require must be an object"
    docker, pins, ini_files = [], {}, []
    settings = {"session.upload_progress.enabled": [], "session.serialize_handler": []}
    for file in files:
        if file.name == "Dockerfile":
            for line in _read(file).splitlines():
                match = re.match(r"\s*FROM\s+(?:--platform=\S+\s+)?php:([^\s]+)", line, re.I)
                if match:
                    docker.append({"file": str(file.relative_to(root)), "tag": match.group(1)})
        if file.name in CONFIG_NAMES or file.suffix.lower() == ".ini":
            text = _read(file)
            ini_files.append(str(file.relative_to(root)).replace(os.sep, "/"))
            for key in settings:
                value = _parse_ini_setting(text, key)
                if value is not None:
                    settings[key].append({"file": str(file.relative_to(root)).replace(os.sep, "/"),
                                           "value": value})
    for name in (".php-version", ".tool-versions"):
        p = root / name
        if p.is_file():
            pins[name] = _read(p, 10000).strip()
    names = sorted(str(p.relative_to(root)).replace(os.sep, "/") for p in files)
    return {
        "path": str(root),
        "is_php_project": bool(cp.is_file() or any(n.endswith(".php") for n in names) or docker),
        "php_file_count": sum(n.endswith(".php") for n in names),
        "files": names,
        "composer": {"present": cp.is_file(), "name": composer.get("name"),
                     "require_php": req.get("php") if isinstance(req, dict) else None,
                     "platform_php": platform.get("php") if isinstance(platform, dict) else None,
                     "error": error},
        "docker_php_images": docker,
        "pinned_versions": pins,
        "php_ini_files": sorted(set(ini_files)),
        "php_ini_settings": settings,
        "cli_runtime": detect_cli_php_version(),
        "runtime_warning": "CLI version may differ from PHP-FPM, Apache, containers, or production hosting.",
        "config_warning": "Discovered INI files are static project files; effective runtime configuration may differ."
    }
