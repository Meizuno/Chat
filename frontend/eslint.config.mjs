import { createConfigForNuxt } from '@nuxt/eslint-config/flat'

export default createConfigForNuxt({
  features: {
    stylistic: true
  }
}).append({
  rules: {
    // Code Style & Formatting Rules
    semi: ['error', 'never'], // Disallows semicolons at the end of statements.
    '@stylistic/semi': ['error', 'never'],
    quotes: ['error', 'single'], // Enforces the use of single quotes for strings.
    '@stylistic/quotes': ['error', 'single'],
    'comma-dangle': 'off',
    '@stylistic/comma-dangle': ['error', 'never'],
    'vue/comma-dangle': ['error', 'never'],
    'arrow-parens': ['error', 'as-needed'], // Requires parens around arrow function arguments only when needed.
    '@stylistic/arrow-parens': ['error', 'as-needed'],
    'object-curly-spacing': ['error', 'always'], // Enforces consistent spacing inside object braces.
    '@stylistic/object-curly-spacing': ['error', 'always'],
    indent: ['warn', 2, { SwitchCase: 1 }], // Enforces a consistent 2-space indentation.
    '@stylistic/indent': ['warn', 2, { SwitchCase: 1 }],
    '@stylistic/operator-linebreak': ['error', 'after'],
    '@stylistic/brace-style': ['error', '1tbs'],
    '@stylistic/indent-binary-ops': ['warn', 2],
    '@stylistic/quote-props': ['error', 'as-needed'],

    // Potential Errors & Best Practices
    'no-console': ['warn', { allow: ['error', 'warn'] }], // Warns on `console.log`, allows `console.warn` and `console.error`.
    'no-debugger': 'warn', // Warns on the use of `debugger` statements.
    'import/extensions': 'off', // Disables checking for file extensions in imports.
    'import/no-extraneous-dependencies': 'off', // Allows importing devDependencies.
    'import/no-unresolved': 'off', // Disables checking for unresolved module paths.
    'no-undef': 'off', // Disables flagging undeclared variables (for Nuxt auto-imports).
    '@typescript-eslint/no-non-null-assertion': 'off', // Allows the use of the non-null assertion operator (`!`).
    '@typescript-eslint/no-empty-function': 'off', // Allows empty function declarations.

    // Vue Specific Rules
    'vue/multi-word-component-names': 'off', // Allows single-word component names.
    'vue/max-attributes-per-line': [
      'error',
      {
        singleline: { max: 1 },
        multiline: { max: 1 }
      }
    ], // Enforces only one attribute per line.
    'vue/html-indent': [
      'warn',
      2,
      {
        attribute: 1,
        baseIndent: 1,
        closeBracket: 0,
        alignAttributesVertically: true
      }
    ], // Enforces 2-space indentation in the template.
    'vue/no-v-html': 'off', // Allows the use of the `v-html` directive.
    'vue/html-self-closing': 'off', // Does not enforce self-closing tags.
    'vue/singleline-html-element-content-newline': 'off', // Does not require newlines around content in single-line elements.
    'vue/html-closing-bracket-newline': ['off', { multiline: 'never' }], // Does not enforce newline for closing brackets in multi-line elements.

    // Nuxt Specific Rules
    'nuxt/nuxt-config-keys-order': 'off'
  }
})
