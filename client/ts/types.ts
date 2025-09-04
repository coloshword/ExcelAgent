declare module 'canvas-datagrid' {
    export interface CanvasDataGridStyle {
        gridBackgroundColor?: string;
        [key: string]: unknown;
    }

    export interface CanvasDatagridOptions {
        parentNode?: HTMLElement;
        data?: any[];
        style?: Partial<CanvasDataGridStyle>;
        [key: string]: unknown;
    }

    export interface CanvasDatagridInstance extends HTMLElement {
        data: any[];
        style: CanvasDataGridStyle;
        attributes: Record<string, any>;
        addEventListener(type: string, listener: (e: any) => void): void;
    }

    export default function canvasDatagrid(
        options?: CanvasDatagridOptions
    ): CanvasDatagridInstance;
}

