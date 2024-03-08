import { Component, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { DeskService } from '../desk.service';
import { DeskReservationService } from '../desk-reservation.service';
import { Desk, DeskReservation, User, DeskEntry } from '../models';
import { permissionGuard } from '../permission.guard';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';
import { AdminDeskDialogComponent } from '../admin-desk-dialog/admin-desk-dialog.component';

export interface TypeSelector {
  value: string;
}

@Component({
  selector: 'app-admin-reservation',
  templateUrl: './admin-reservation.component.html',
  styleUrls: ['./admin-reservation.component.css']
})
export class AdminReservationComponent implements OnInit {

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


  public static Route: Route = {
    path: 'admin-reservation',
    component: AdminReservationComponent,
    title: 'Reservation Administration',
    canActivate: [permissionGuard('admin/', '*')]
  }


  public links = [
    { label: 'Users', path: '/admin/users' },
    { label: 'Roles', path: '/admin/roles' },
    { label: 'Reservations', path: '/admin-reservation' },
  ];


  selectedType!: string;

  displayedColumns: string[] = ['pid', 'name', 'email', 'time', 'desk_tag', 'desk_type', 'included_resource', 'remove'];
  displayedColumnsDesks: string[] = ['desk_tag', 'desk_type', 'included_resource', 'available', 'update', 'reserve'];

  futureDeskReservationsList: [DeskReservation, Desk, User][] = [];
  pastDeskReservationsList: [DeskReservation, Desk, User][] = [];

  filteredDeskReservationsList: [DeskReservation, Desk, User][] = [];
  filteredFutureDeskReservationsList: [DeskReservation, Desk, User][] = [];
  filteredPastDeskReservationsList: [DeskReservation, Desk, User][] = [];

  searchByPid!: string;

  allDesks: Desk[] = [];

  newDeskTag: FormControl
  newDeskType: FormControl
  newDeskIncludedResource: FormControl

  constructor(
    private deskService: DeskService,
    private deskReservationService: DeskReservationService,
    private router: Router,
    protected snackBar: MatSnackBar,
    public dialog: MatDialog,
  ) {
    this.newDeskTag = new FormControl('',
      [Validators.required,
      this.existingDeskTagValidator.bind(this),
      ]);

    this.newDeskType = new FormControl('', [Validators.required]);
    this.newDeskIncludedResource = new FormControl('',);
  }


  ngOnInit(): void {
    this.getFutureDeskReservations();
    this.getPastDeskReservations();
    this.getAllDesks();
  }


  /**
   * FOR ADMIN:
   * Filter the desk reservations
   * by PID. 
   *
   */
  filterByPid() {
    this.getFutureDeskReservations();
    this.getPastDeskReservations();
  }


  existingDeskTagValidator(control: FormControl): { [key: string]: boolean } | null {
    if (this.allDesks.find(desk => desk.tag.toLowerCase() === control.value.toLowerCase())) {
      return { existingDeskTag: true };
    }
    return null;
  }


  /**
   * Create a new desk in the database.
   * Only available to Admin or users who have permission.
   * 
   */
  createDesk() {
    this.newDeskTag.setValue(this.newDeskTag.value.toUpperCase());
    let deskTag: string = this.newDeskTag.value;
    let deskType: string = this.newDeskType.value;
    let includedResource: string = this.newDeskIncludedResource.value;
    let deskForm: DeskEntry = { tag: deskTag, desk_type: deskType, included_resource: includedResource, available: true };

    // Sorts the desk by tag when the desk is being created.
    this.deskService.createDesk(deskForm).subscribe(() => {
      this.getAllDesks();
      this.allDesks.sort((a, b) => a.tag.localeCompare(b.tag));
    });

    this.snackBar.open(`Desk ${deskTag} Added`, "", { duration: 4000, panelClass: ['center-text'] })
  }


  /**
   * Remove a desk in the database.
   * Only available to Admin or users who have permission.
   */
  removeDesk(desk: Desk) {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: { message: `Are you sure you want to remove Desk ${desk.tag}?` }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deskService.removeDesk(desk).subscribe(() => {
          this.getFutureDeskReservations()
          this.getPastDeskReservations()
          this.getAllDesks()
        });
        this.snackBar.open(`Desk ${desk.tag} Removed.`, "", { duration: 4000, panelClass: ['center-text'] })
      }
    })
  }


  /**
   * Retrieve all desks that are in the database.
   * The lists are sorted by Desk Tag.
   */
  getAllDesks(): void {
    this.deskService.getAllDesks().subscribe(
      desks => {
        this.allDesks = desks.sort((a, b) => a.tag.localeCompare(b.tag));
      })
  }


  /**
   * FOR ADMIN:
   * Retrieve future desk reservations for admin view.
   */
  getFutureDeskReservations(): void {
    this.deskReservationService.getFutureDeskReservations().subscribe(
      deskReservations => {
        this.futureDeskReservationsList = deskReservations;
        if (this.searchByPid) {
          this.futureDeskReservationsList = this.futureDeskReservationsList.filter(
            reservation => reservation[2].pid.toString().startsWith(this.searchByPid)
          );
        }
      }
    )
  }


  /**
   * FOR ADMIN:
   * Retrieve past desk reservations for admin view.
   */
  getPastDeskReservations(): void {
    this.deskReservationService.getPastDeskReservations().subscribe(
      deskReservations => {
        this.pastDeskReservationsList = deskReservations;
        if (this.searchByPid) {
          this.pastDeskReservationsList = this.pastDeskReservationsList.filter(
            reservation => reservation[2].pid.toString().startsWith(this.searchByPid)
          );
        }
      }
    )
  }


  /**
   * ADMIN SIDE:
   * Remove Past Desk Reservations & Cancel/Unreserve a Desk Reservation.
   * 
   * STUDENT SIDE:
   * Cancel/Unreserve a Desk Reservation.
   *
   */
  removeDeskReservation(deskReservationsListItem: [DeskReservation, Desk, User], buttonType: string): void {

    let reservationDate = new Date(deskReservationsListItem[0].date);
    let reservationTime = reservationDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    let pid = deskReservationsListItem[2].pid;

    let formattedDate = reservationDate.toLocaleDateString('en-US',
      {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      })

    this.deskReservationService.removeDeskReservation(deskReservationsListItem[1], deskReservationsListItem[0]).subscribe(() => {
      if (reservationDate > new Date()) {
        this.getFutureDeskReservations();
      } else {
        this.getPastDeskReservations();
      }
    });

    let message;
    if (buttonType === 'cancel') {
      message = `Desk Reservation on ${formattedDate} at ${reservationTime} Canceled. \n (Admin Override - PID: ${pid})`;
    } else {
      message = `Expired Desk Reservation by PID: ${pid} \n on ${formattedDate} at ${reservationTime} \n Deleted From History.`;
    }

    this.snackBar.open(message, '', { duration: 4000, panelClass: ['center-text', 'success-snackbar'] });

  }


  /**
   * FOR ADMIN:
   * Update Desk Type and Desk Included Resources
   * for a specific desk.
   *
   */
  updateDesk(desk: Desk) {
    const dialogRef = this.dialog.open(AdminDeskDialogComponent, {
      data: { myDesk: desk },
    });

    dialogRef.afterClosed().subscribe(result => {

      desk.desk_type = result.new_type;
      desk.included_resource = result.new_resource;
      this.deskService.updateDesk(desk).subscribe(() => {
        this.getAllDesks();
      });
      this.snackBar.open(`Desk ${desk.tag} Successfully Updated`, '', { duration: 4000, panelClass: ['center-text', 'success-snackbar'] });


    });

  }


  /**
   * FOR ADMIN:
   * Confirmation prompt for removing a desk reservation.
   */
  singularRemoveConfirm(deskReservationsListItem: [DeskReservation, Desk, User], buttonType: string): void {
    let resDate = new Date(deskReservationsListItem[0].date)
    let date = resDate.toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: { message: "Are you sure you want to remove the reservation for " + deskReservationsListItem[1].tag + " on " + date + "?" },
    })
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.removeDeskReservation(deskReservationsListItem, buttonType);
      }
    })
  }


  /**
   * FOR ADMIN:
   * Confirmation prompt for removing all future desk reservations.
   */
  pastRemoveConfirm(): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: { message: "Are you sure you want to remove reservations older than 30 days?" },
    })
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deskReservationService.removeOldDeskReservations().subscribe(() => {
          this.getPastDeskReservations()
        });
        let message = "Removed old reservations."
        this.snackBar.open(message, '', { duration: 4000, panelClass: ['center-text', 'success-snackbar'] })
      }
    })
  }


  /**
   * FOR ADMIN:
   * Confirmation prompt for toggling the availability of a desk.
   */
  toggleAvailability(desk: Desk): void {
    if (desk.available) {
      const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
        data: { message: "Are you sure you want to make " + desk.tag + " unavailable and remove any current reservations?" },
      })
      dialogRef.afterClosed().subscribe(result => {
        if (result) {
          desk.available = !desk.available;
          this.deskService.toggleAvailability(desk).subscribe(() => {
            this.getAllDesks()
          });
          this.snackBar.open(desk.tag + " is now unavailable.", '', { duration: 4000, panelClass: ['center-text', 'success-snackbar'] })

        }
      })
    } else {
      const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
        data: { message: "Are you sure you want to make " + desk.tag + " available?" },
      })
      dialogRef.afterClosed().subscribe(result => {
        if (result) {
          desk.available = !desk.available;
          this.deskService.toggleAvailability(desk).subscribe(() => {
            this.getAllDesks()
          });
          this.snackBar.open(desk.tag + " is now available.", '', { duration: 4000, panelClass: ['center-text', 'success-snackbar'] })
        }
      })
    }
  }
}