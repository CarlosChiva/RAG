import {DomSanitizer, SafeHtml} from '@angular/platform-browser';

export interface messages{
    text: string | Promise<String> | SafeHtml;
    isUser: boolean;
    isTyping?: boolean;
    tableData?: any;
  }[] = [];