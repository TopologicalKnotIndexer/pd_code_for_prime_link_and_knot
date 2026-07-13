import unittest

import prime_link_knot_10 as catalogue


class CatalogueTests(unittest.TestCase):
    def test_catalogue_counts_and_trefoil_record(self):
        records = catalogue.load_pd_code()
        self.assertEqual(len(records), 1312)
        self.assertEqual(len(catalogue.load_amphicheiral()), 20)
        self.assertEqual(
            records["K3a1"],
            [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]],
        )

    def test_small_combination_counts_are_complete_and_unique(self):
        expected = {2: 2, 3: 4, 4: 10, 5: 20}
        for bound, count in expected.items():
            combinations = catalogue.get_all_combination(bound)
            self.assertEqual(len(combinations), count)
            self.assertEqual(len({tuple(item) for item in combinations}), count)
            for item in combinations:
                indices = [catalogue.get_link_name_sort_index(name) for name in item]
                self.assertEqual(indices, sorted(indices))
                self.assertLessEqual(sum(index[0] for index in indices), bound)

    def test_invalid_crossing_bounds_are_rejected(self):
        for value in (True, 2.5, "5"):
            with self.assertRaises(TypeError):
                catalogue.get_all_combination(value)
        with self.assertRaises(ValueError):
            catalogue.get_all_combination(-1)


if __name__ == "__main__":
    unittest.main()
