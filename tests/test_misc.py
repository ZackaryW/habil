from pprint import pprint
import unittest
import requests
import json
from habil_base.habiToken import HabiToken
import habil_map.habil_case as habil_case

class t_map_cases(unittest.TestCase):
    def setUp(self) -> None:
        HabiToken.from_json("config.json", set_global=True)

    def test_api_up(self):
        self.assertTrue(habil_case.get_api_status.request().status)
        
    