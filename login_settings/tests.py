from django.test import TestCase

# Then we create the unittest for this validator in tests.py:
# import datetime
# import mock
# from unittest2 import TestCase
# from django.core.exceptions import ValidationError
# from .. import validators


# class ValidationTests(TestCase):
#     @mock.patch('utils.date.today')
#     def test_validate_future_date(self, today_mock):
#         # Pin python's today to returning the same date
#         # always so we can actually keep on unit testing in the future :)
#         today_mock.return_value = datetime.date(2010, 1, 1)
#
#         # A future date should work
#         validators.validate_future_date(datetime.date(2010, 1, 2))
#
#         # The mocked today's date should fail
#         with self.assertRaises(ValidationError) as e:
#             validators.validate_future_date(datetime.date(2010, 1, 1))
#         self.assertEquals([u'Date should be in the future.'], e.exception.messages)
#
#         # Date in the past should also fail
#         with self.assertRaises(ValidationError) as e:
#             validators.validate_future_date(datetime.date(2009, 12, 31))
#         self.assertEquals([u'Date should be in the future.'], e.exception.messages)