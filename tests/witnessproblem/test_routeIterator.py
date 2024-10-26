import unittest

from src.witnessproblem import Route, RouteIterator, is_route_valid


TEST_ROUTE = Route()
TEST_ROUTE.vertex = [1, 2, 3]
TEST_ROUTE.time = [10, 10, 10]
TEST_ROUTE.leaveTime = [10, 20, 30]

def get_route_in_creation():
    route = Route()
    route.vertex = [4]
    route.time = [0]
    route.leaveTime = [0]
    return route

class TestRouteIterator(unittest.TestCase):


    def test_init(self):
        # Act
        iterator = RouteIterator(TEST_ROUTE)

        # Assert
        self.assertEqual(iterator.index, 0)
        self.assertEqual(iterator.vertex, 1)
        self.assertEqual(iterator.a, 0)
        self.assertEqual(iterator.b, 10)
        

    def test_init_copying_to_route(self):
        # Arrange
        route_in_creation = Route()

        # Act
        iterator = RouteIterator(TEST_ROUTE, copy_to=route_in_creation)

        # Assert
        self.assertEqual(route_in_creation.vertex, [1])
        self.assertEqual(route_in_creation.time, [10])
        self.assertEqual(route_in_creation.leaveTime, [10])


    def test_next(self):
        # Arrange
        iterator = RouteIterator(TEST_ROUTE)
        route_in_creation = get_route_in_creation()

        # Act
        iterator.next(TEST_ROUTE, copy_to=route_in_creation)

        # Assert
        self.assertEqual(iterator.index, 1)
        self.assertEqual(iterator.vertex, 2)
        self.assertEqual(iterator.a, 10)
        self.assertEqual(iterator.b, 20)

        self.assertEqual(route_in_creation.vertex, [4, 2])
        self.assertEqual(route_in_creation.time, [0, 10])
        self.assertEqual(route_in_creation.leaveTime, [0, 20])


    def test_advance_copies_the_route_until_given_point(self):
        # Arrange
        route_in_creation = Route()
        iterator = RouteIterator(TEST_ROUTE, copy_to=route_in_creation)

        # Act
        iterator.advance(TEST_ROUTE, 1, copy_to=route_in_creation)

        # Assert
        self.assertEqual(iterator.index, 1)

        self.assertEqual(route_in_creation.vertex, [1, 2])
        self.assertEqual(route_in_creation.time, [10, 10])
        self.assertEqual(route_in_creation.leaveTime, [10, 20])


    def test_advance_to_end_copies_the_whole_route(self):
        # Arrange
        route_in_creation = Route()
        iterator = RouteIterator(TEST_ROUTE, copy_to=route_in_creation)

        # Act
        iterator.advance_to_end(TEST_ROUTE, copy_to=route_in_creation)


        # Assert
        self.assertEqual(iterator.index, 2)
        self.assertEqual(route_in_creation, TEST_ROUTE)


if __name__ == '__main__':
    unittest.main()