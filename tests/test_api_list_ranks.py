from tests.base_api import BaseAPITestCase
from tests.base import rank_data
from flask import json


class ListRanksAPITestCase(BaseAPITestCase):
    def test_list_ranks(self):
        """Test listing all ranks."""
        res = self.get(url='/ranks')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        assert 'ranks' in data
        ranks = data['ranks']
        self.assertEqual(len(ranks), 4)
        for index, rank in enumerate(ranks):
            self.assertEqual(rank['name'], rank_data[index]['name'])
            self.assertEqual(rank['id'], index + 1)
