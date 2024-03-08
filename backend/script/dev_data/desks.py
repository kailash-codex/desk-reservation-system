"""Sample Desk models to use in development environment"""

from ...models import Desk

a1 = Desk(id=1, tag='CD1', desk_type='Computer Desk', included_resource='iMac 24 w/ Mac Studio', available=True)
a2 = Desk(id=2, tag='CD2', desk_type='Computer Desk', included_resource='Pro Display XDR w/ Mac Pro', available=True)
a3 = Desk(id=3, tag='CD3', desk_type='Computer Desk', included_resource='Windows Desktop i9', available=True)
a4 = Desk(id=4, tag='SD1', desk_type='Standing Desk', included_resource='Windows Desktop i5', available=True)
a5 = Desk(id=5, tag='OSD1', desk_type='Open Study Desk', included_resource='iMac 24 w/ Mac Mini', available=True)
a6 = Desk(id=6, tag='OSD2', desk_type='Enclosed Study Desk', included_resource='Studio Display w/ Mac Mini', available=True)
a7 = Desk(id=7, tag='OSD3', desk_type='Enclosed Study Office', included_resource='iMac 24 w/ Mac Pro', available=True)
a8 = Desk(id=8, tag='CSC1', desk_type='Closed Study Carrel', included_resource='Studio Display w/ Mac Studio', available=True)
a9 = Desk(id=9, tag='CSC2', desk_type='Closed Study Carrel', included_resource='Pro Display XDR w/ Mac Studio', available=True)
a10 = Desk(id=10, tag='CSC3', desk_type='Closed Study Carrel', included_resource='Windows Desktop i7', available=True)
a11 = Desk(id=11, tag='CSC4', desk_type='Closed Study Carrel', included_resource='Studio Display w/ Mac Mini', available=True)



models = [
    a1,
    a2,
    a3,
    a4,
    a5,
    a6,
    a7,
    a8,
    a9,
    a10,
    a11
]