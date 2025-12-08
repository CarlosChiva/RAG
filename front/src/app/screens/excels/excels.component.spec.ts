import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Excels } from './excels.component';

describe('Excels', () => {
  let component: Excels;
  let fixture: ComponentFixture<Excels>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Excels]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Excels);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
