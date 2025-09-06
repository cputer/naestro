/**
 * Conventional Commits config for Naestro
 * Types commonly used in JS/TS repos; scope optional
 */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  ignores: [(msg) => msg.includes('dependabot[bot]')],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert'
      ]
    ],
    'subject-case': [2, 'never', ['sentence-case', 'start-case', 'pascal-case', 'upper-case']],
    'body-max-line-length': [2, 'always', 0]
  }
};
