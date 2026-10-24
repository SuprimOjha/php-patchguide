# Data privacy

Local checks do not make network requests. They read selected metadata and may run php -v; they do not execute application scripts, inspect environment variable values, or upload project files. The scheduled workflow fetches the public PHP archive and uploads a JSON snapshot containing public identifiers and a timestamp.
