from datetime import datetime
from datetime import date

import rooms as rooms
import room_inventory as room_inv
import bookings as book
import datetime as dt

r = rooms.Rooms()
ri = room_inv.RoomInventory()
bk = book.Bookings()

def list_rooms(room_id=None, room_type=None):
    #basically call the CRUD routine fetch
    print("*** Room Listing ***")
    for item in r.fetch(room_id=None, room_type=None):
        print(item)

def list_room_types():
    return ri.get_cursor.execute("select room_type from Rooms group by room_type;").fetchall()

def add_room_to_inventory(room_type, floor, room_number,room_status) :
    #basically call the CRUD routine
    # We can have multiples of the same room type on the same floor
    
    ri.add(room_type,floor,room_number,room_status)

def update_room_in_inventory(room_number,room_availability):
    # Might want to think about this further.  The rooms in inventory are a specific type and have a room number so
    # I don't think that we can change room types or number unless we have a total hotel renovation which we won't address
    # The status flag (integer) could be updated to indicate the room is temporarily not available (wild band party destroyed it...
    # needs maintenance)
    # Leaving it here for now.....
    #basically call the CRUD routine
    ri.update(room_number,room_availability)
    print("Room",room_number,"updated.")

def delete_room_in_inventory(room_number):
    # Might want to think about this further.  The rooms in inventory are a specific type and have a room number so
    # I don't think that we can change room types or number unless we have a total hotel renovation which we won't address
    # The status flag (integer) could be updated to indicate the room is temporarily not available (wild band party destroyed it...
    # needs maintenance)
    # Leaving it here for now.....
    #basically call the CRUD routine
    ri.delete(room_number)


def list_rooms_in_inventory(room_number=None,floor=None, room_type=None):
    # probably a join select
    # we need a few flavors for different selects - assumes a single value on select!!
    # Returned data is all the same row format
    if room_number == None and floor == None and room_type == None:
        sql_all = """
            select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate, case ri.available when 0 then 'Available' else 'Not Available' end Available
             from Room_inventory ri JOIN Rooms r on ri.room_id = r.id;
            """
        # Should we preformat the list or just deliver raw data...?
        return ri.get_cursor.execute(sql_all).fetchall()
    elif room_number != None and floor == None and room_type == None:
        sql = """
            select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate from Room_inventory ri JOIN Rooms r on ri.room_id = r.id where ri.room_number = ?;
            """
        # Should we preformat the list or just deliver raw data...?
        return ri.get_cursor.execute(sql,(room_number,)).fetchone()
    elif room_number == None and floor != None and room_type == None:
        sql = """
            select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate from Room_inventory ri JOIN Rooms r on ri.room_id = r.id where ri.floor = ?;
            """
        # Should we preformat the list or just deliver raw data...?
        return ri.get_cursor.execute(sql,(floor,)).fetchall()
    elif room_number == None and floor == None and room_type != None:
        sql = """
            select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate from Room_inventory ri JOIN Rooms r on ri.room_id = r.id where r.room_type = ?;
            """
        # Should we preformat the list or just deliver raw data...?
        return ri.get_cursor.execute(sql,(room_type,)).fetchall()

## Booking routines
######################################################################################

def book_room(room_number,start_date,end_date):
    # just insert the room - the ui has hopefully handled the selection and avialability
    # UI is passing strings, make sure they are the correct types
    # UI is collecting and grabbing the list and formatted the dates (maybe)

    bk.add(room_number,start_date,end_date)

# Availability basic logic:
    # The kicker is that the date selection is the toughest part and needs to be part of a left join
    #  So we'll need a CTE to select the rooms that are UN-available for the dates, left join with
    # Inventory and select those records with a null room number which indicates that room IS available
    # The CTE is our "unavailable" table and will be used across the "availability" logic.

def list_available_rooms_by_floor(floor,start_date,end_date):
    # The inbound dates should be in YYYY-MM-DD format but they aren't
    #so convert the strings into date tuples and then format them back (weird but the only way I could get it to work)

    s_date = datetime.strptime(start_date,'%m-%d-%Y')
    e_date = datetime.strptime(end_date,'%m-%d-%Y')

    start_date = datetime.strftime(s_date,'%Y-%m-%d')
    end_date = datetime.strftime(e_date,'%Y-%m-%d')

    sql = """
        with Unavailable as 
        (select room_number, start_date, end_date from Bookings 
        where (date(?) between start_date and end_date or date(?) between start_date and end_date)
        OR start_date between date(?) and date(?) or end_date between date(?) and date(?))
        select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate from Room_inventory ri 
        JOIN Rooms r on ri.room_id = r.id LEFT JOIN Unavailable bk on ri.room_number = bk.room_number where ri.floor = ?
         and bk.room_number is NULL and ri.available = 0 ORDER BY ri.floor, ri.room_number;
    """
    # Run it
    result = bk.get_cursor.execute(sql,(start_date,end_date,start_date,end_date,start_date,end_date,floor)).fetchall()

    return result


def list_all_available_rooms(start_date,end_date):
    # The inbound dates should be in YYYY-MM-DD format but they aren't
    # so convert the strings into date tuples and then format them back (weird but the only way I could get it to work)

    s_date = datetime.strptime(start_date, '%m-%d-%Y')
    e_date = datetime.strptime(end_date, '%m-%d-%Y')

    start_date = datetime.strftime(s_date, '%Y-%m-%d')
    end_date = datetime.strftime(e_date, '%Y-%m-%d')

    sql = """
        with Unavailable as 
        (select room_number, start_date, end_date from Bookings 
        where (date(?) between start_date and end_date or date(?) between start_date and end_date)
        OR start_date between date(?) and date(?) or end_date between date(?) and date(?))
        select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate from Room_inventory ri 
        JOIN Rooms r on ri.room_id = r.id LEFT JOIN Unavailable bk on ri.room_number = bk.room_number where 
         bk.room_number is NULL ORDER BY ri.floor, ri.room_number;
    """
    # Run it
    result = bk.get_cursor.execute(sql, (start_date, end_date, start_date, end_date, start_date, end_date)).fetchall()

    return result


def list_available_rooms_by_type(room_type,start_date,end_date):
    # The inbound dates should be in YYYY-MM-DD format but they aren't
    # so convert the strings into date tuples and then format them back (weird but the only way I could get it to work)

    s_date = datetime.strptime(start_date, '%m-%d-%Y')
    e_date = datetime.strptime(end_date, '%m-%d-%Y')

    start_date = datetime.strftime(s_date, '%Y-%m-%d')
    end_date = datetime.strftime(e_date, '%Y-%m-%d')

    sql = """
        with Unavailable as 
        (select room_number, start_date, end_date from Bookings 
        where (date(?) between start_date and end_date or date(?) between start_date and end_date)
        OR start_date between date(?) and date(?) or end_date between date(?) and date(?))
        select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate from Room_inventory ri 
        JOIN Rooms r on ri.room_id = r.id LEFT JOIN Unavailable bk on ri.room_number = bk.room_number where r.room_type = ?
         and bk.room_number is NULL and ri.available = 0 ORDER BY ri.floor, ri.room_number;
    """
    # Run it
    result = bk.get_cursor.execute(sql,(start_date, end_date, start_date, end_date, start_date, end_date, room_type)).fetchall()
    return result

def list_available_rooms_by_price_range(low_price,high_price,start_date,end_date):

    # The inbound dates should be in YYYY-MM-DD format but they aren't
    # so convert the strings into date tuples and then format them back (weird but the only way I could get it to work)

    s_date = datetime.strptime(start_date, '%m-%d-%Y')
    e_date = datetime.strptime(end_date, '%m-%d-%Y')

    start_date = datetime.strftime(s_date, '%Y-%m-%d')
    end_date = datetime.strftime(e_date, '%Y-%m-%d')

    sql = """
        with Unavailable as 
        (select room_number, start_date, end_date from Bookings 
        where (date(?) between start_date and end_date or date(?) between start_date and end_date)
        OR start_date between date(?) and date(?) or end_date between date(?) and date(?))
        select ri.floor,ri.room_number,r.room_description,r.room_type,r.room_rate from Room_inventory ri 
        JOIN Rooms r on ri.room_id = r.id LEFT JOIN Unavailable bk on ri.room_number = bk.room_number 
        where r.room_rate BETWEEN ? and ? 
         and bk.room_number is NULL and ri.available = 0 ORDER BY ri.floor, ri.room_number;
    """
    # Run it
    result = bk.get_cursor.execute(sql, (start_date, end_date, start_date, end_date, start_date, end_date, low_price,high_price)).fetchall()
    return result

def list_booked_rooms(start_date,end_date):

    # The inbound dates should be in YYYY-MM-DD format but they aren't
    # so convert the strings into date tuples and then format them back (weird but the only way I could get it to work)

    s_date = datetime.strptime(start_date, '%m-%d-%Y')
    e_date = datetime.strptime(end_date, '%m-%d-%Y')

    start_date = datetime.strftime(s_date, '%Y-%m-%d')
    end_date = datetime.strftime(e_date, '%Y-%m-%d')

    sql = """
        with Unavailable as (
    select 
        b.id,
        b.room_number, 
        b.start_date, 
        b.end_date 
    from 
        Bookings b
    where 
        (date(?) between b.start_date and b.end_date or date(?) between b.start_date and b.end_date)
        OR b.start_date between date(?) and date(?) or b.end_date between date(?) and date(?)
        )
        select 
            ua.id,
            ri.floor,
            ri.room_number,
            r.room_description,
            r.room_type,
            r.room_rate,
            STRFTIME('%m-%d-%Y', ua.start_date),
            STRFTIME('%m-%d-%Y', ua.end_date) 
        from 
            Room_inventory ri 
        JOIN 
            Rooms r on ri.room_id = r.id 
        LEFT JOIN 
            Unavailable ua on ri.room_number = ua.room_number 
        where 
            ua.room_number is not NULL 
        ORDER BY 
            ri.floor, ri.room_number;

    """
    # Run it
    result = bk.get_cursor.execute(sql, (start_date, end_date, start_date, end_date, start_date, end_date)).fetchall()
    return result

def update_booking(booking_id, room_number, start_date, end_date):
    # basically call the CRUD routine - The booking ID is the booking dates ID

    bk.update(booking_id, room_number, start_date, end_date)
    print("Booking",booking_id,"updated.")

def cancel_booking(booking_id):
    # basically call the CRUD routine

    bk.delete(booking_id)

    



