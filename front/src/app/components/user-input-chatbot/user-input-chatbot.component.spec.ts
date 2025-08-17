import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserInputChatbotComponent } from './user-input-chatbot.component';

describe('UserInputComponent', () => {
  let component: UserInputChatbotComponent;
  let fixture: ComponentFixture<UserInputChatbotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserInputChatbotComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserInputChatbotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
