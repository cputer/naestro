import react from 'eslint-plugin-react';

export default [
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parserOptions: {
        ecmaFeatures: {
          jsx: true
        }
      },
      globals: {
        window: 'readonly',
        document: 'readonly',
        navigator: 'readonly'
      }
    },
    plugins: { react },
    settings: { react: { version: 'detect' } },
    rules: {
      // Adjust to your preference; we set off to avoid noisy CI. Component files can still use PropTypes/TS.
      'react/prop-types': 'off'
    }
  }
];
