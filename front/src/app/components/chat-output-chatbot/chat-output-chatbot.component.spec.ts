import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatOutputChatbotComponent } from './chat-output-chatbot.component';

describe('ChatOutputChatbotComponent', () => {
  let component: ChatOutputChatbotComponent;
  let fixture: ComponentFixture<ChatOutputChatbotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChatOutputChatbotComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChatOutputChatbotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
