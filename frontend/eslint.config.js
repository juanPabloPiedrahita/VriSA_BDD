/**
 * ESLint configuration for the VRISA frontend project
 *
 * This file sets up linting rules for TypeScript and React projects.
 * It integrates recommended settings for:
 *   - JavaScript (ESLint)
 *   - TypeScript (typescript-eslint)
 *   - React hooks (eslint-plugin-react-hooks)
 *   - React refresh (eslint-plugin-react-refresh)
 *
 * Features:
 *   - Ignores the "dist" folder
 *   - Applies to all .ts and .tsx files
 *   - Uses ECMAScript 2020 features
 *   - Includes browser globals
 *   - Enforces recommended rules for hooks and React refresh
 */

import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import tseslint from 'typescript-eslint';

export default tseslint.config(
    { ignores: ['dist'] },
    {
        extends: [js.configs.recommended, ...tseslint.configs.recommended],
        files: ['**/*.{ts,tsx}'],
        languageOptions: {
            ecmaVersion: 2020,
            globals: globals.browser,
        },
        plugins: {
            'react-hooks': reactHooks,
            'react-refresh': reactRefresh,
        },
        rules: {
            ...reactHooks.configs.recommended.rules,
            'react-refresh/only-export-components': [
                'warn',
                { allowConstantExport: true },
            ],
        },
    },
);
