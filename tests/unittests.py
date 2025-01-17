import unittest


class UnitTests(unittest.TestCase):
    def test_check_for_weekend(self) :
        for weekday in day_update.day_update.weekdays:
            self.assertEqual(day_update.check_for_weekend(weekday.name.lower()), weekday.value)
            self.assertEqual(day_update.check_for_weekend(weekday.name.upper()), weekday.value)

if __name__ == '__main__':
    unittest.main()
