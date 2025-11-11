module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Type is required and must be one of the allowed types
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation only changes
        'style',    // Changes that do not affect the meaning of the code
        'refactor', // A code change that neither fixes a bug nor adds a feature
        'perf',     // A code change that improves performance
        'test',     // Adding missing tests or correcting existing tests
        'build',    // Changes that affect the build system or external dependencies
        'ci',       // Changes to our CI configuration files and scripts
        'chore',    // Other changes that don't modify src or test files
        'revert',   // Reverts a previous commit
      ],
    ],

    // Scope is required for this project
    'scope-enum': [
      2,
      'always',
      [
        'lib',     // Core library (todowrite package)
        'cli',     // Command-line interface (todowrite-cli package)
        'web',     // Web interface (todowrite-web package)
        'tests',   // Test suite and testing infrastructure
        'docs',    // Documentation
        'build',   // Build system and packaging
        'config',  // Configuration files and settings
      ],
    ],

    // Scope is required
    'scope-empty': [2, 'never'],

    // Subject cannot be empty
    'subject-empty': [2, 'never'],

    // Subject must be in sentence case (first letter capitalized)
    'subject-case': [2, 'always', ['sentence-case']],

    // Subject must not end with a period
    'subject-full-stop': [2, 'never', '.'],

    // Subject max length
    'subject-max-length': [2, 'always', 72],

    // Body max line length
    'body-max-line-length': [2, 'always', 72],

    // Footer max line length
    'footer-max-line-length': [2, 'always', 72],

    // No leading/trailing whitespace in subject
    'subject-trailing-whitespace': [2, 'never'],
  },
};
