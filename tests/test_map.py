from pprint import pprint
from time import sleep
import habil
from habil.sub.tag import HabiTag
from habil_base.exceptions import HabiRequestException
from habil_base.habiToken import HabiToken
import habil_case
from habil_map.habiMapResponse import HabiMapResponse
import tests

from habil_map.habiMapMeta import HabiMapMeta

class t_case_base(tests.base_case):
    def setUp(self) -> None:
        self.case_res = None
        self.token = HabiToken.from_json("config.json", set_global=True)

    def tearDown(self) -> None:
        if self.case_res is not None:
            pprint(
                self.case_res
            )
            print("=============next limit==============")
            print(HabiMapMeta.RATE_LIMIT_REMAINING)


class t_case(t_case_base):
    def test_api_up(self):
        self.case_res = habil_case.get_api_status()
        self.assertTrue(self.case_res.status)

class t_case_user(t_case_base):
    def test_map_get_user(self):
        self.case_res = habil_case.user.get_user_profile(headers=self.token)
        pprint(self.case_res.json_data)


    def test_map_get_user_only_stats(self):
        self.case_res = habil_case.user.get_user_profile_stats(headers=self.token)
        self.assertGetAttr(self.case_res.repo, "job",["warrior", "rogue", "mage", "healer"])
        self.assertGetAttrMin(self.case_res.repo, "con", 0, allow_equal=True)
        self.assertGetAttrMin(self.case_res.repo, "str", 0, allow_equal=True)
        self.assertGetAttrMin(self.case_res.repo, "int", 0, allow_equal=True)
        self.assertGetAttrMin(self.case_res.repo, "per", 0, allow_equal=True)
        self.assertGetAttrMin(self.case_res.repo, "lvl", 0)
        self.assertGetAttrMin(self.case_res.repo, "exp", 0)
        self.assertGetAttrMin(self.case_res.repo, "hp", 0, allow_equal=True)
        self.assertGetAttrMax(self.case_res.repo, "hp", 50, allow_equal=True)
        self.assertGetAttrMin(self.case_res.repo, "mp", 0, allow_equal=True)

class t_case_tag(t_case_base):
    def test_map_create_and_delete_tag(self):
        HabiTag.get_all(token=self.token, force_pull=True)
        for tag in HabiTag._instances[HabiTag].values():
            tag : HabiTag
            if tag.name == "TEST_TAG":
                self.fail("TEST_TAG already exists")
        pprint(HabiMapMeta.get_last_log())

        self.case_res : HabiMapResponse = habil_case.tag.create_new_tag(name="TEST_TAG", headers=self.token)
        pprint(self.case_res)
        if self.case_res.fail:
            raise HabiRequestException(self.case_res)

        tag = HabiTag.from_res(self.case_res)
        pprint(tag)
        sleep(10)
        self.case_res : HabiMapResponse = habil_case.tag.delete_a_user_tag(tagId=tag.id, headers=self.token)
        if self.case_res.fail:
            raise HabiRequestException(self.case_res)