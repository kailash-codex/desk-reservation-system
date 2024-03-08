import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Desk } from '../models';
import { FormControl, Validators } from '@angular/forms';

export interface TypeSelector {
  value: string;
}

@Component({
  selector: 'app-admin-desk-dialog',
  templateUrl: './admin-desk-dialog.component.html',
  styleUrls: ['./admin-desk-dialog.component.css']
})
export class AdminDeskDialogComponent {

  typeoptions: TypeSelector[] = [
    { value: 'Computer Desk' },
    { value: 'Standing Desk' },
    { value: 'Open Study Desk' },
    { value: 'Enclosed Study Desk' },
    { value: 'Enclosed Study Office' },
  ];

  inc_resource_options: TypeSelector[] = [
    { value: '' },
    { value: 'Windows Desktop i5' },
    { value: 'Windows Desktop i7' },
    { value: 'Windows Desktop i9' },
    { value: 'iMac 24 w/ Mac Mini' },
    { value: 'iMac 24 w/ Mac Pro' },
    { value: 'iMac 24 w/ Mac Studio' },
    { value: 'Studio Display w/ Mac Mini' },
    { value: 'Studio Display w/ Mac Pro' },
    { value: 'Studio Display w/ Mac Studio' },
    { value: 'Pro Display XDR w/ Mac Mini' },
    { value: 'Pro Display XDR w/ Mac Pro' },
    { value: 'Pro Display XDR w/ Mac Studio' },
  ];

  chosenDesk: Desk;
  newDeskType: FormControl
  newDeskIncludedResource: FormControl

  constructor(
    public dialogRef: MatDialogRef<AdminDeskDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Desk
  ) {
    this.chosenDesk = data;
    this.newDeskType = new FormControl('', [Validators.required]);
    this.newDeskIncludedResource = new FormControl('',);
  }


  onNoClick(): void {
    this.dialogRef.close();

  }

  /**
   * Passing the new Desk Type and new resources from the 
   * dialog upon the admin clicking "Update".
   * 
   */
  onUpdateClick(): void {
    const new_type = this.newDeskType.value;
    const new_resource = this.newDeskIncludedResource.value;
    this.dialogRef.close({ new_type, new_resource });

  }

  isOptionDisabled(option: TypeSelector): boolean {
    return this.chosenDesk.included_resource === option.value;
  }


}
