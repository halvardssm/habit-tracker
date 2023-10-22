import unittest
from datetime import datetime
from duration import Duration


class TestDuration(unittest.TestCase):
    def test_class_duration_simple(self):
        """Test the Duration class with simple parameters"""

        start_time = datetime(2023, 10, 19, 13, 43, 12)

        duration1 = Duration("PT1H", start_time)
        self.assertEqual(duration1.start_time, start_time)
        self.assertEqual(duration1.duration.total_seconds(), 3600)

        self.assertEqual(
            duration1.find_next_instance(start_time), datetime(2023, 10, 19, 14, 43, 12)
        )

        self.assertEqual(str(duration1.duration), "1:00:00")

    def test_class_duration_complex(self):
        """Test the Duration class with complex parameters"""

        start_time = datetime(2023, 10, 19, 13, 43, 12)

        duration2 = Duration("P1Y2M3DT4H5M6S", start_time)
        self.assertEqual(duration2.start_time, start_time)
        self.assertEqual(duration2.duration.total_seconds(), 273906)

        self.assertEqual(
            duration2.find_next_instance(start_time), datetime(2024, 12, 22, 17, 48, 18)
        )

        self.assertEqual(str(duration2.duration), "1 years, 2 months, 3 days, 4:05:06")


if __name__ == "__main__":
    unittest.main()
