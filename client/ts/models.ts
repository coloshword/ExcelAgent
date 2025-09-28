export interface FileData {
    filename: string;
    fileContent: string; // the b64 file content
}

export interface ModifySheetsIn {
    sheet_name: string;
    sheet_status: string[][]
}

export interface ModifySheetsOut {
    sheet_id: number
    sheet_name: string
}

export interface Sheet {
    id: number
    sheet_name: string 
    sheet_status: string[][]
    last_update_time: string,
    user_id: number    
}