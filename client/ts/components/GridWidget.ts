import canvasDatagrid from 'canvas-datagrid';
import type {CanvasDataGrid}  from 'canvas-datagrid';

export class GridWidget {
    private parent: HTMLDivElement;
    private initRows: number = 100;
    private initColumns: number = 26;
    private data: string[][] = [];
    private grid: CanvasDataGrid | null = null;

    constructor(
        parent: HTMLDivElement
    ) 
    {
        this.parent = parent;
        this.setup();
    }

    private toDOM() {
        const gridElement: HTMLDivElement = document.createElement('div');
        this.grid = canvasDatagrid({
            parentNode: gridElement,
        });
        this.parent.append(gridElement);
        this.grid.attributes.columnHeaderClickBehavior = 'select';
        this.grid.style.columnHeaderCellHorizontalAlignment = 'center';
        this.grid.style.height = '100%';
        this.grid.style.width = '100%';
        // make sure the gridElement is fully long as well
        gridElement.style.height = '100%';
        this.initializeGrid();
    }

    /**
     * initializes the grid, either with prefilled data or just an empty
     */
    private initializeGrid() {
        // empty data
        // Array(l) creates an array of length l, and with map we initialize this.initRows number of Array(this.initColumns)
        this.data = [...Array(this.initRows)].map(e => new Array(this.initColumns).fill(""));
        this.grid!.data = this.data;
    }

    private setup() {
        this.toDOM();
    }
}