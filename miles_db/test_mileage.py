import mileage
from mileage import MileageError
import sqlite3
from unittest import TestCase


class TestMileageDB(TestCase):
    test_db_url = 'test_miles.db'

    """Before running this test, create test_miles.db
    Create expected miles table
    create table miles (vehicle text, total_miles float);"""
    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        conn.close()
# I wrote this part without a compiler after I completed my 'last' commit so
# if my code doesn't work, please use commit before this.
    def test_add_new_vehicle_check_name_AND_case_AND_mileage(self):
        mileage.add_miles('Blue Car', 100)
        expected = {'BLUE CAR': 100}
        self.compare_db_to_expected(expected)

        mileage.add_miles('GrEeN cAr', 50)
        expected['GREEN CAR'] = 50
        self.compare_db_to_expected(expected)

    def test_increase_miles_for_vehicle(self):
        mileage.add_miles('Red Car', 100)
        expected = {'RED CAR': 100}
        self.compare_db_to_expected(expected)

        mileage.add_miles('Red Car', 50)
        expected['RED CAR'] = 100 + 50
        self.compare_db_to_expected(expected)

    def test_add_new_vehicle_no_vehicle(self):
        with self.assertRaises(Exception):
            mileage.addMiles(None, 100)

    def test_add_new_vehicle_invalid_new_miles(self):
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', -100)
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', 'abc')
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', '12.def')

    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()


# when I put 'METHOD', it means the method name follows
class TestMETHODget_mileage(TestCase):
    # I don't think this is necessary, but it probably makes the code easier to follow.
    test_db_url = 'test_miles.db'

    # copied next few lines from setUp method at top of file
    def setUp(self):
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        conn.close()
        # This would be simpler in a list for looping over and
        # testing each return at end of loop, but instructions
        # say to keep it here. Probably to practice 'setUp' method.
        mileage.add_miles('Herbie', 25)
        mileage.add_miles('Mystery Machine', 27)
        mileage.add_miles('Bat Mobile', 29)

    # Here, 'METHOD' means I am testing the method in the test name
    def test_METHOD_search_for_existing_car_check_accurate_return(self):
        self.assertEqual(mileage.get_mileage('HERBIE'), '25.0')
        self.assertEqual(mileage.get_mileage('MYSTERY MACHINE'), '27.0')
        self.assertEqual(mileage.get_mileage('BAT MOBILE'), '29.0')

    def test_GET_MILEAGE_search_for_omitted_car_check_returns_None(self):
        self.assertEqual(mileage.get_mileage('UFO'), None)
