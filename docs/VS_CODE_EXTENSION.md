# VS Code Extension

## TL;DR
| Step | Command | Notes |
|------|---------|-------|
| Install extension | `code --install-extension naestro.vsix` | Load local VSIX package |
| Connect to API | Set `NAESTRO_API_URL` in settings | Points extension to running orchestrator |
| Run task | Use command palette "Naestro: Run Task" | Sends prompt to API |

## Overview
The VS Code extension provides an editor workflow for submitting tasks to Naestro and viewing responses.

## Steps
1. Install the extension from the packaged VSIX file.
2. Configure settings for API URL and authentication token if required.
3. Use command palette or sidebar to create and monitor tasks.

## Validation
Run a sample prompt and ensure responses appear in the output panel.

## Troubleshooting
| Issue | Resolution |
|-------|-----------|
| Extension not found | Check VSIX path or marketplace availability |
| Cannot reach API | Confirm `NAESTRO_API_URL` is set and service is running |
