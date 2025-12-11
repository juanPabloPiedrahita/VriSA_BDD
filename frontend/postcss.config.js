/**
 * postcss.config.js
 *
 * PostCSS configuration for the Tailadmin React project.
 *
 * Plugins:
 *   - '@tailwindcss/postcss': Used to process Tailwind CSS classes.
 *
 * Note:
 *   This file allows PostCSS to apply the necessary transformations to CSS,
 *   enabling Tailwind and other potential plugins in the future.
 */
export default {
    plugins: {
        '@tailwindcss/postcss': {},
    },
}
