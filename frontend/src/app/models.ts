export interface Desk {
    id: number;
    tag: string;
    desk_type: string;
    included_resource: string;
    available: boolean;
  }

export interface DeskEntry {
    tag: string;
    desk_type: string;
    included_resource: string;
    available: boolean;
}


export interface DeskReservation {
    id: number;
    desk_id: number;
    user_id: number;
    date: Date;
}

export interface DeskReservationEntry {
    date: Date;
}

export interface User {
    id: number;
    pid: number;
    onyen: string;
    first_name: string;
    last_name: string;
    email: string;
    pronouns: string;
}
export interface DeskReservationTuple {
    item: [[DeskReservation, Desk]];
}

export interface Desk {
    id: number;
    tag: string;
    desk_type: string;
    included_resource: string;
    available: boolean;
  }