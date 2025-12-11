/**
 * TypeScript module declaration for importing SVGs as React components.
 *
 * Allows importing SVG files with the `?react` suffix in two ways:
 * 1. As a React component (`ReactComponent`) with standard SVG props.
 * 2. As a string URL (`default export`) pointing to the SVG file.
 *
 * Usage examples:
 *
 * import { ReactComponent as Logo } from './logo.svg?react';
 * import logoPath from './logo.svg?react';
 *
 * <Logo width={50} height={50} />
 * <img src={logoPath} alt="Logo" />
 */

declare module "*.svg?react" {
    import React = require("react");

    /**
     * React component version of the SVG file.
     * Can be used directly in JSX and accepts standard SVG props.
     */
    export const ReactComponent: React.FC<React.SVGProps<SVGSVGElement>>;

    /**
     * Default export as string URL pointing to the SVG file.
     */
    const src: string;
    export default src;
}
