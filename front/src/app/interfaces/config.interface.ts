// config.interface.ts
export interface Config {
    credentials: string;
    conversation: string;
    modelName: string;
    userInput: string;
    tools:any;
}
export interface ToolConfigPayload {
  type: 'image' | 'mcp'| null;          
  config: any;                    
}