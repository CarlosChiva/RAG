import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RagDdbbComponent } from './rag-ddbb.component';

describe('RagDdbbComponent', () => {
  let component: RagDdbbComponent;
  let fixture: ComponentFixture<RagDdbbComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RagDdbbComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RagDdbbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
