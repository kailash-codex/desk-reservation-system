import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthenticationService } from './authentication.service';
import { Desk, DeskEntry } from './models';

@Injectable({
  providedIn: 'root'
})
export class DeskService {

  public desk$!: Observable<Desk | undefined>;

  constructor(
    private http: HttpClient,
    private auth: AuthenticationService,
  ) { }

  /**
   * Retrieve all desks that are in the database.
   * 
   * @returns observable array of Desk objects.
   */
  getAllDesks(): Observable<Desk[]> {
    return this.http.get<Desk[]>('/api/desk');
  }

  /**
   * Retrieve all desks that are available.
   * 
   * @returns observable array of Desk objects.
   */
  getAvailableDesks(): Observable<Desk[]> {
    return this.http.get<Desk[]>('/api/desk/available');
  }

  /**
   * Create a new desk in the database.
   * Only available to Admin or users who have permission.
   * 
   * @returns observable Desk object.
   */
  createDesk(desk: DeskEntry): Observable<Desk> {
    return this.http.post<Desk>('/api/desk/admin/create_desk', desk);
  }

  /**
   * Remove a desk in the database.
   * Only available to Admin or users who have permission.
   * 
   * @returns observable Desk object.
   */
  removeDesk(desk: Desk): Observable<Desk> {
    return this.http.post<Desk>('/api/desk/admin/remove_desk', desk);
  }

  
  /**
   * FOR ADMIN:
   * Toggle the ability to reserve a desk.
   * 
   * @returns observable DeskReservation object.
   */
  toggleAvailability(desk: Desk): Observable<Desk> {
    return this.http.put<Desk>('/api/desk/admin/toggle_availability', desk);
  }


  /**
   * Get a desk by desk ID in the database.
   * Only available to Admin or users who have permission.
   * 
   * @returns observable Desk object.
   */
  getDeskByID(desk: Desk): Observable<Desk> {
    return this.http.get<Desk>(`/api/desk/${desk.id}`)
  }


  /**
   * Update a desk in the database.
   * Only available to Admin or users who have permission.
   * 
   * @returns observable Desk object.
   */
  updateDesk(desk: Desk): Observable<Desk> {
    return this.http.put<Desk>(`/api/desk/admin/update_desk/${desk.id}`, desk)
  }

}
