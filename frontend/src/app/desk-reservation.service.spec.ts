import { TestBed } from '@angular/core/testing';

import { DeskReservationService } from './desk-reservation.service';

describe('DeskReservationService', () => {
  let service: DeskReservationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DeskReservationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
