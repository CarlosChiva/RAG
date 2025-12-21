import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SidebarExcelItemComponent } from './sidebar-excel-item.component';

describe('SidebarExcelItemComponent', () => {
  let component: SidebarExcelItemComponent;
  let fixture: ComponentFixture<SidebarExcelItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SidebarExcelItemComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SidebarExcelItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should emit deleteItem event when onDelete is called', () => {
    spyOn(component.deleteItem, 'emit');
    component.onDelete();
    expect(component.deleteItem.emit).toHaveBeenCalled();
  });

  it('should emit toggleShow event when onToggleShow is called', () => {
    spyOn(component.toggleShow, 'emit');
    component.onToggleShow();
    expect(component.toggleShow.emit).toHaveBeenCalled();
  });

  it('should emit selectItem event when onSelect is called', () => {
    spyOn(component.selectItem, 'emit');
    component.onSelect();
    expect(component.selectItem.emit).toHaveBeenCalled();
  });
});
