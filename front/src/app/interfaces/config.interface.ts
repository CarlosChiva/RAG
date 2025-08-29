// config.interface.ts
export interface Config {
    credentials: string;
    conversation: string;
    modelName: string;
    userInput: string;
    tools:Object;
}
export interface ToolConfigPayload {
  type: 'image' | 'mcp';          
  config: any;                    
}