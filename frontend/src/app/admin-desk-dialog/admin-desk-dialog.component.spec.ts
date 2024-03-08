import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminDeskDialogComponent } from './admin-desk-dialog.component';

describe('AdminDeskDialogComponent', () => {
  let component: AdminDeskDialogComponent;
  let fixture: ComponentFixture<AdminDeskDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminDeskDialogComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminDeskDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
