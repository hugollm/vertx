from unittest import TestCase
from vertx.case_insensitive_dict import CaseInsensitiveDict


class CaseInsensitiveDictTestCase(TestCase):

    def test_can_be_created_without_arguments(self):
        CaseInsensitiveDict()

    def test_can_be_created_with_dict(self):
        data = CaseInsensitiveDict({'foo': 'bar'})
        self.assertEqual(data, {'foo': 'bar'})

    def test_can_be_created_with_key_value_tuples(self):
        data = CaseInsensitiveDict((('foo', 'bar'),))
        self.assertEqual(data, {'foo': 'bar'})

    def test_can_set_key(self):
        data = CaseInsensitiveDict()
        data['foo'] = 'bar'
        self.assertEqual(data, {'foo': 'bar'})

    def test_set_keys_can_be_accessed_insensitively(self):
        data = CaseInsensitiveDict()
        data['Foo'] = 'bar'
        self.assertEqual(data['foo'], 'bar')

    def test_creation_keys_can_be_accessed_insensitively(self):
        data = CaseInsensitiveDict({'Foo': 'bar'})
        self.assertEqual(data['foo'], 'bar')

    def test_can_delete_key_insensitively(self):
        data = CaseInsensitiveDict({'Foo': 'bar'})
        del data['foo']
        self.assertEqual(data, {})

    def test_original_keys_can_be_iterated(self):
        data = CaseInsensitiveDict({'Foo': 'bar', 'Bar': 'foo'})
        self.assertEqual(sorted(list(data)), ['Bar', 'Foo'])

    def test_can_get_length(self):
        data = CaseInsensitiveDict({'Foo': 'bar', 'Bar': 'foo'})
        self.assertEqual(len(data), 2)

    def test_string_representation_is_the_same_as_a_regular_dict(self):
        data = CaseInsensitiveDict({'Foo': 'bar', 'Bar': 'foo'})
        self.assertEqual(sorted(str(data)), sorted(str({'Foo': 'bar', 'Bar': 'foo'})))

    def test_compares_insensitively_against_another_insensitive_dict(self):
        data1 = CaseInsensitiveDict({'foo': 'bar', 'bar': 'foo'})
        data2 = CaseInsensitiveDict({'Foo': 'bar', 'Bar': 'foo'})
        self.assertEqual(data1, data2)

    def test_compares_sensitively_against_regular_dict(self):
        data1 = CaseInsensitiveDict({'foo': 'bar', 'bar': 'foo'})
        data2 = {'Foo': 'bar', 'Bar': 'foo'}
        self.assertNotEqual(data1, data2)
