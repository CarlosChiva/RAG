import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DdbbConfComponent } from './ddbb_conf.component';

describe('DdbbConfComponent', () => {
  let component: DdbbConfComponent;
  let fixture: ComponentFixture<DdbbConfComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DdbbConfComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DdbbConfComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
