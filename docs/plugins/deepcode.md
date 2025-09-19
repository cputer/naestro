# DeepCode Plugin

## Goal
Provide a concise plan for integrating the DeepCode static analysis plugin into Naestro.

## Flow
1. Expose the repository path to the DeepCode adapter through the plugin interface.
2. Submit the workspace to DeepCode for analysis and capture the issue feed it returns.
3. Normalize the DeepCode findings into Naestro's insight format and surface them in the UI.

## Validation
- Add unit coverage for the DeepCode adapter translation layer.
- Run the plugin against a sample repository to confirm issues appear with correct metadata.

## PR
- Wire the adapter into the plugin registry and configuration knobs.
- Document usage expectations and configuration secrets in the repo.

## Safety
Ensure repository contents and credentials are handled according to Naestro's security policies when communicating with DeepCode.

## Status
Blocked – DeepCode adapter is not wired yet.
