from shopdb.api import *
import shopdb.exceptions as exc
from tests.base_api import BaseAPITestCase
from flask import json
from copy import copy


class CreatePayoffAPITestCase(BaseAPITestCase):
    def test_create_payoff(self):
        """Create a payoff"""
        data = {'amount': 1000, 'comment': 'Test payoff'}
        res = self.post(url='/payoffs', data=data, role='admin')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        assert 'message' in data
        self.assertEqual(data['message'], 'Created payoff.')
        payoffs = Payoff.query.all()
        self.assertEqual(len(payoffs), 1)
        self.assertEqual(payoffs[0].amount, 1000)
        self.assertEqual(payoffs[0].comment, 'Test payoff')
        self.assertFalse(payoffs[0].revoked)

    def test_create_payoff_invalid_amount(self):
        """Create a payoff with a negative should raise an exception."""
        for amount in [-1000, 0]:
            data = {'amount': amount, 'comment': 'Test payoff'}
            res = self.post(url='/payoffs', data=data, role='admin')
            self.assertEqual(res.status_code, 401)
            self.assertException(res, exc.InvalidAmount)

    def test_create_payoff_wrong_type(self):
        """Create a payoff with wrong type(s)."""
        data = {'amount': 1000, 'comment': 'Test payoff'}

        for field in data:
            copy_data = copy(data)
            copy_data[field] = 100.0
            res = self.post(url='/payoffs', data=copy_data, role='admin')
            self.assertEqual(res.status_code, 401)
            self.assertException(res, exc.WrongType)

        self.assertEqual(len(Payoff.query.all()), 0)

    def test_create_payoff_unknown_field(self):
        """Create a payoff with an unknown field."""
        data = {'amount': 1000, 'comment': 'Test payoff', 'foo': 'bar'}
        res = self.post(url='/payoffs', role='admin', data=data)
        self.assertEqual(res.status_code, 401)
        self.assertException(res, exc.UnknownField)
        self.assertEqual(len(Payoff.query.all()), 0)

    def test_create_payoff_missing_data(self):
        """Create a payoff with a missing field should raise an error"""
        data = {'amount': 1000}
        res = self.post(url='/payoffs', role='admin', data=data)
        self.assertEqual(res.status_code, 401)
        self.assertException(res, exc.DataIsMissing)
        self.assertEqual(len(Payoff.query.all()), 0)
