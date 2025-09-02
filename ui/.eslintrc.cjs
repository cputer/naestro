module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
  ],
  rules: {
    "react/prop-types": "error",
    "react/no-unknown-property": "error",
  },
  ignorePatterns: ["dist/", "build/", "node_modules/"],
};
