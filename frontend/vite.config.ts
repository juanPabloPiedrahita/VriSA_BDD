/**
 * vite.config.ts
 *
 * Vite configuration for the Tailadmin React project.
 *
 * Plugins:
 *   - @vitejs/plugin-react: Enables React Fast Refresh and JSX support.
 *   - vite-plugin-svgr: Allows importing SVGs as React components.
 *
 * SVGR Options:
 *   - icon: true → scales SVGs to match current font-size when used as icons.
 *   - exportType: "named" → exports SVGs as named exports.
 *   - namedExport: "ReactComponent" → the named export to use for React components.
 *
 * Note:
 *   This configuration sets up Vite to handle React and SVG imports efficiently.
 */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react(),
        svgr({
            svgrOptions: {
                icon: true,
                exportType: "named",
                namedExport: "ReactComponent",
            },
        }),
    ],
});
