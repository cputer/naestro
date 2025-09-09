# No Proxy Configuration in This Repository

This project must not set proxy configuration in `.npmrc` or environment variables. If you need a
proxy for your network, configure it **outside** of this repo (e.g., your shell profile) and never
commit proxy settings here.

### Disallowed in repo

- `.npmrc` keys: `proxy`, `http-proxy`, `https-proxy`
- ENV vars in CI or checked-in files: `http_proxy`, `https_proxy`, `HTTP_PROXY`, `HTTPS_PROXY`,
  `npm_config_*proxy*`

### CI behavior

CI unsets all proxy-related env vars before any `npm` step.
