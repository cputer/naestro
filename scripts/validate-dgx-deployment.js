#!/usr/bin/env node
"use strict";

// Validate DGX deployment by running basic GPU checks.
const { execSync } = require("child_process");

function run(cmd, desc) {
  process.stdout.write(`Checking ${desc}... `);
  try {
    const out = execSync(cmd, { stdio: "pipe" }).toString().trim();
    console.log("ok");
    if (out) {
      console.log(out);
    }
    return true;
  } catch (err) {
    console.log("failed");
    if (err.stdout) {
      console.error(err.stdout.toString().trim());
    }
    if (err.stderr) {
      console.error(err.stderr.toString().trim());
    } else {
      console.error(err.message);
    }
    return false;
  }
}

let success = true;
success = run("nvidia-smi -L", "GPU visibility") && success;
success = run("nvidia-smi -i 0 -q | grep -i 'MIG Mode'", "MIG mode") && success;
success = run("nvidia-smi topo -m", "GPU topology") && success;

if (!success) {
  console.error("DGX deployment validation failed");
  process.exit(1);
} else {
  console.log("DGX deployment validation passed");
}
