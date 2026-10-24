import unittest

from py_log_sample import LogSampler


class TestLogSampler(unittest.TestCase):
    def setUp(self):
        self.sampler = LogSampler()

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(self.sampler.sample([]), [])

    def test_single_line_returns_one_group_count_one(self):
        self.assertEqual(self.sampler.sample(["hello"]), [("hello", 1)])

    def test_all_same_returns_one_group(self):
        self.assertEqual(
            self.sampler.sample(["error", "error", "error"]),
            [("error", 3)],
        )

    def test_all_distinct_each_count_one(self):
        self.assertEqual(
            self.sampler.sample(["a", "b", "c"]),
            [("a", 1), ("b", 1), ("c", 1)],
        )

    def test_repeated_then_distinct(self):
        self.assertEqual(
            self.sampler.sample(["x", "x", "x", "y", "y", "z"]),
            [("x", 3), ("y", 2), ("z", 1)],
        )

    def test_groups_separated_by_distinct_lines(self):
        self.assertEqual(
            self.sampler.sample(["a", "a", "b", "a", "a", "a"]),
            [("a", 2), ("b", 1), ("a", 3)],
        )

    def test_last_line_repeated(self):
        self.assertEqual(
            self.sampler.sample(["a", "b", "b", "b"]),
            [("a", 1), ("b", 3)],
        )

    def test_first_line_repeated(self):
        self.assertEqual(
            self.sampler.sample(["a", "a", "a", "b", "c"]),
            [("a", 3), ("b", 1), ("c", 1)],
        )

    def test_alternating_pattern(self):
        self.assertEqual(
            self.sampler.sample(["x", "y", "x", "y", "x"]),
            [("x", 1), ("y", 1), ("x", 1), ("y", 1), ("x", 1)],
        )

    def test_long_run(self):
        self.assertEqual(
            self.sampler.sample(["ok"] * 1000),
            [("ok", 1000)],
        )

    def test_accepts_generator(self):
        def gen():
            yield "a"
            yield "a"
            yield "b"

        self.assertEqual(self.sampler.sample(gen()), [("a", 2), ("b", 1)])

    def test_returns_list_of_tuples(self):
        result = self.sampler.sample(["a", "a"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertIsInstance(item, tuple)
        self.assertEqual(item, ("a", 2))


if __name__ == "__main__":
    unittest.main()
