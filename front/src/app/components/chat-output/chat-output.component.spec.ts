import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatOutputComponent } from './chat-output.component';

describe('ChatOutputComponent', () => {
  let component: ChatOutputComponent;
  let fixture: ComponentFixture<ChatOutputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChatOutputComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChatOutputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
