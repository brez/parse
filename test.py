import unittest
from factories import factory, AlphaEntry, BetaEntry, GammaEntry
from exceptions import UnknownOrAmbiguousPattern


class PatternFactoryTest(unittest.TestCase):

    def test_provides_class_alpha_for_alpha_pattern(self):
        alpha = factory('Lastname, Firstname, (703)­742­0996, Blue, 10013')
        self.assertIsInstance(alpha, AlphaEntry)

    def test_provides_class_beta_for_beta_pattern(self):
        beta = factory('Firstname, Lastname, 10013, 646 111 0101, Green')
        self.assertIsInstance(beta, BetaEntry)

    def test_provides_class_gamma_for_gamma_pattern(self):
        gamma = factory('Firstname, Lastname, Red, 11237, 703 955 0373')
        self.assertIsInstance(gamma, GammaEntry)

    def test_throws_exception_for_unknown_pattern(self):
        with self.assertRaises(UnknownOrAmbiguousPattern):
            factory('Firstname Lastname, Red, 11237, 703 955 0373')

    def test_throws_exception_for_nonsense(self):
        with self.assertRaises(UnknownOrAmbiguousPattern):
            factory('nonsense')


class EntityParseTest(unittest.TestCase):

    def test_alpha_pattern_parse(self):
        expected = {
            "color": "Blue",
            "firstname": "Firstname",
            "lastname": "Lastname",
            "phonenumber": "703-742-0996",
            "zipcode": "10013",
            }
        alpha = factory('Lastname, Firstname, (703)­742­0996, Blue, 10013')
        self.assertDictEqual(expected, alpha.parse())

    def test_beta_pattern_parse(self):
        expected = {
            "color": "Green",
            "firstname": "Firstname",
            "lastname": "Lastname",
            "phonenumber": "646-111-0101",
            "zipcode": "10013",
            }
        beta = factory('Firstname, Lastname, 10013, 646 111 0101, Green')
        self.assertDictEqual(expected, beta.parse())

    def test_gamma_pattern_parse(self):
        expected = {
            "color": "Red",
            "firstname": "Firstname",
            "lastname": "Lastname",
            "phonenumber": "703-955-0373",
            "zipcode": "11237",
            }
        gamma = factory('Firstname, Lastname, Red, 11237, 703 955 0373')
        self.assertDictEqual(expected, gamma.parse())

    def test_throws_invalid_exception_for_invalid_zipcode(self):
        alpha = factory('Lastname, Firstname, (703)­742­0996, Blue, 100135')
        with self.assertRaises(UnknownOrAmbiguousPattern):
            alpha.parse()


class EntityIntegrationTest(unittest.TestCase):

    def test_booker_t(self):
        expected = {
            "color": "yellow",
            "firstname": "Booker T.",
            "lastname": "Washington",
            "phonenumber": "373-781-7380",
            "zipcode": "87360",
            }
        result = factory('Booker T., Washington, 87360, 373 781 7380, yellow')
        self.assertDictEqual(expected, result.parse())

    def test_james(self):
        expected = {
            "color": "yellow",
            "firstname": "James",
            "lastname": "Murphy",
            "phonenumber": "018-154-6474",
            "zipcode": "83880",
            }
        result = factory('James, Murphy, yellow, 83880, 018 154 6474')
        self.assertDictEqual(expected, result.parse())

    def test_throws_invalid_exception_for_invalid_zipcode(self):
        alpha = factory('Chandler, Kerri, (623)­668­9293, pink, 12312312')
        with self.assertRaises(UnknownOrAmbiguousPattern):
            alpha.parse()

    def test_throws_invalid_exception_for_invalid_zipcode(self):
        with self.assertRaises(UnknownOrAmbiguousPattern):
            factory('asdfawefawea')

if __name__ == '__main__':
    unittest.main()
