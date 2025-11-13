import unittest
from main.configuration import Context


class TestTrimPrefix(unittest.TestCase):

    def setUp(self):
        self.service = Context.get_completions_infill_service()

    def test_custom_key(self):
        text = "let g:llama_config.new_key = v:true"
        prefix = "let g:llama_config."
        expected = "new_key = v:true"
        result = self.service._trim_overlap_with_prefix_words(prefix, text)
        self.assertEqual(result, expected)

    def test_prefix_present(self):
        text = "Hello, world!"
        prefix = "Hello, "
        expected = "world!" 
        result = self.service._trim_overlap_with_prefix_words(prefix, text)
        self.assertEqual(result, expected)

    def test_prefix_absent(self):
        text = "Hello, world!"
        prefix = "Hi, "
        expected = text
        result = self.service._trim_overlap_with_prefix_words(prefix, text)
        self.assertEqual(result, expected)

    def test_empty_text_nonempty_prefix(self):
        text = ""
        prefix = "Hello"
        expected = text
        result = self.service._trim_overlap_with_prefix_words(prefix, text)
        self.assertEqual(result, expected)

    def test_nonempty_text_empty_prefix(self):
        text = "Hello"
        prefix = ""
        expected = text
        result = self.service._trim_overlap_with_prefix_words(prefix, text)
        self.assertEqual(result, expected)

    def test_both_empty(self):
        text = ""
        prefix = ""
        expected = ""
        result = self.service._trim_overlap_with_prefix_words(prefix, text)
        self.assertEqual(result, expected)

    def test_prefix_longer_than_text(self):
        text = "Hi"
        prefix = "Hello"
        expected = text
        result = self.service._trim_overlap_with_prefix_words(prefix, text)
        self.assertEqual(result, expected)


class TestTrimSuffix(unittest.TestCase):

    def setUp(self):
        self.service = Context.get_completions_infill_service()

    def test_suffix_present(self):
        insertion = "world!"
        suffix = "!"
        expected = "world"
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

    def test_suffix_absent(self):
        insertion = "world!"
        suffix = "?"
        expected = insertion
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

    def test_empty_suffix_nonempty_insertion(self):
        insertion = "Hello"
        suffix = ""
        expected = insertion
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

    def test_empty_insertion_nonempty_suffix(self):
        insertion = ""
        suffix = "Hello"
        expected = insertion
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

    def test_both_empty(self):
        insertion = ""
        suffix = ""
        expected = ""
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

    def test_suffix_longer_than_insertion(self):
        insertion = "Hi"
        suffix = "Hello"
        expected = insertion
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

    def test_partial_overlap(self):
        insertion = "helloworld"
        suffix = "world!"
        expected = "hello"
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

    def test_full_overlap(self):
        insertion = "world"
        suffix = "world"
        expected = ""
        result = self.service._trim_overlap_with_suffix(suffix, insertion)
        self.assertEqual(result, expected)

