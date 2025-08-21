import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadComfyComponent } from './upload_comfy.component';

describe('UploadComponent', () => {
  let component: UploadComfyComponent;
  let fixture: ComponentFixture<UploadComfyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadComfyComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadComfyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
