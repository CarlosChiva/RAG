import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadMCPComponent } from './upload_mcp.component';

describe('UploadComponent', () => {
  let component: UploadMCPComponent;
  let fixture: ComponentFixture<UploadMCPComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadMCPComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadMCPComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
