import unittest

from src.witnessproblem import Route, createStaticRoute

class TestRoute(unittest.TestCase):


    def test_route_startAt(self):
        # Arrange
        route = Route()

        # Act
        route.startAt(1)

        # Assert
        self.assertEqual(route.vertex, [1])
        self.assertEqual(route.time, [0])
        self.assertEqual(route.leaveTime, [0])


    def test_route_sleep_for(self):
        # Arrange
        route = Route()
        route.startAt(1)

        # Act
        route.sleep_for(2)
        route.sleep_for(3)

        # Assert
        self.assertEqual(route.vertex, [1])
        self.assertEqual(route.time, [5])
        self.assertEqual(route.leaveTime, [5])


    def test_create_static_route(self):
        # Act
        route = createStaticRoute(1, 10)

        # Assert
        self.assertEqual(route.vertex, [1])
        self.assertEqual(route.time, [10])
        self.assertEqual(route.leaveTime, [10])
        self.assertEqual(len(route), 1)


if __name__ == '__main__':
    unittest.main()