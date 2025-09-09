# Releasing

1. Update `RELEASE_NOTES.md` with details for the new version.
2. Commit the changes to the repository.
3. Create and push a version tag in the form `vX.Y.Z`.
4. The release workflow will run automatically and:
   - build and push Docker images for the gateway and orchestrator to `ghcr.io` tagged with the
     version,
   - generate a GitHub Release using `RELEASE_NOTES.md` as the changelog.

The workflow is defined in `.github/workflows/release.yml`.
