import sqlite3

db_url = 'mileage.db'   # Assumes the table miles have already been created.

"""
    Before running this test, create test_miles.db
    Create expected miles table
    create table miles (vehicle text, total_miles float);
"""


class MileageError(Exception):
    pass


def add_miles(vehicle, new_miles):
    """If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise MileageError"""
    vehicle = all_chars_upper_case(vehicle)

    if not vehicle:
        raise MileageError('Provide a vehicle name')
    if not isinstance(new_miles, (int, float)) or new_miles < 0:
        raise MileageError('Provide a positive number for new miles')

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    rows_mod = cursor.execute('UPDATE MILES SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, vehicle))
    if rows_mod.rowcount == 0:
        cursor.execute('INSERT INTO MILES VALUES (?, ?)', (vehicle, new_miles))
    conn.commit()
    conn.close()


def all_chars_upper_case(string):
    # had this in add_miles, but decided to make it more modular and easier to test.
    return string.upper()


def get_mileage(vehicle):
    # Next 4 lines basically copied from 'add_miles' function
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    result_set = cursor.execute('SELECT total_miles FROM MILES WHERE vehicle = ?', (vehicle,)).fetchall()
    conn.close()
    # there should be one or zero results
    if len(result_set) is 1:
        # The first item of the only row should be total_miles
        return str(result_set[0][0])
    # since there were no results, the car was not found: return 'None'.
    return None


def main():
    while True:
        vehicle = input("To search for an existing vehicle's mileage, enter 'Search'.\n"
                        "To add mileage to a new or existing vehicle, enter a vehicle name.\n"
                        "To quit, press 'enter' without a name:\n")
        if not vehicle:
            break
        vehicle = all_chars_upper_case(vehicle)
        # if user takes instructions too literally and puts ''search''
        # since I did .upper() earlier in the code, this should catch all cases like 'Search' or 'search'
        if vehicle == "SEARCH" or vehicle == "'SEARCH'":
            vehicle = all_chars_upper_case(input("Enter name of vehicle to search for it.\n"
                                                 "Press 'enter' without a name to exit.\n"))
            if not vehicle:
                break
            mileage = get_mileage(vehicle)
            if not mileage:
                print('Vehicle was not found.')
            else:
                print("Mileage for that vehicle is: \n" + mileage)
        else:
            miles = float(input('Enter new miles for %s: ' % vehicle))  # TODO input validation
            add_miles(vehicle, miles)


if __name__ == '__main__':
    main()
