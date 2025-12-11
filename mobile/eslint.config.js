// ==============================================================================
// ESLint configuration for Expo projects
// ==============================================================================
// This configuration extends the default Expo ESLint setup.
// It also specifies files/folders to ignore during linting.
//
// Reference: https://docs.expo.dev/guides/using-eslint/
// ==============================================================================

const { defineConfig } = require('eslint/config');
const expoConfig = require('eslint-config-expo/flat');

module.exports = defineConfig([
    // Extend Expo's recommended ESLint configuration
    expoConfig,
    {
        // Ignore files/folders from linting
        ignores: ['dist/*'],
    },
]);
