from unittest import TestCase
from .utils import data_post_handler
from typing import Dict, List
from decouple import config


def create_participant(country_name: str, gold: int, sliver: int, bronze: int) -> Dict:
    return {"country": country_name, "medal": {"gold": gold, "silver": sliver, "bronze": bronze}}


def create_verify_body(sport_name: str, participants: List) -> Dict:
    return {"sport_name": sport_name, "participants": participants}


class TestRecordMedal(TestCase):
    def setUp(self):
        self.VERIFY_PATH = 'api/record/verify'
        self.TOKEN = config("DEV_TOKEN")
        self.default_verify = create_verify_body("Archery", [create_participant("Thailand", 1, 0, 0),
                                                             create_participant("China", 0, 1, 0),
                                                             create_participant("Japan", 0, 0, 1)])
        self.repechage_verify = create_verify_body("Boxing", [create_participant("Thailand", 1, 0, 0),
                                                              create_participant("India", 0, 1, 0),
                                                              create_participant("China", 0, 0, 1),
                                                              create_participant("Japan", 0, 0, 1)])
        self.tie_gold_medal_verify = create_verify_body("Archery", [create_participant("Thailand", 1, 0, 0),
                                                                    create_participant("China", 1, 0, 0),
                                                                    create_participant("Japan", 0, 0, 1)])
        self.tie_silver_medal_verify = create_verify_body("Boxing", [create_participant("Thailand", 1, 0, 0),
                                                                     create_participant("India", 0, 0, 1),
                                                                     create_participant("China", 0, 1, 0),
                                                                     create_participant("Japan", 0, 1, 0)])
        self.exceeded_medal_verify = create_verify_body("Archery", [create_participant("Thailand", 1, 0, 0),
                                                                    create_participant("India", 0, 0, 1),
                                                                    create_participant("China", 0, 0, 1),
                                                                    create_participant("Japan", 0, 1, 0)])
        self.exceeded_repechage_medal_verify = create_verify_body("Boxing", [create_participant("Thailand", 1, 0, 0),
                                                                             create_participant("India", 0, 0, 1),
                                                                             create_participant("China", 0, 0, 1),
                                                                             create_participant("Japan", 0, 1, 0),
                                                                             create_participant("Laos", 0, 0, 1), ])
        self.impossible_silver_and_bronze_medal_verify = create_verify_body("Archery",
                                                                            [create_participant("Thailand", 1, 0, 0),
                                                                             create_participant("China", 1, 1, 0),
                                                                             create_participant("Japan", 1, 0, 1)])
        self.impossible_silver_medal_verify = create_verify_body("Archery", [create_participant("Thailand", 1, 0, 0),
                                                                             create_participant("China", 1, 0, 0),
                                                                             create_participant("Japan", 0, 1, 0)])
        self.impossible_bronze_medal_verify = create_verify_body("Boxing", [create_participant("Thailand", 1, 0, 0),
                                                                            create_participant("India", 0, 1, 1),
                                                                            create_participant("China", 0, 1, 0),
                                                                            create_participant("Japan", 0, 1, 0)])
        self.impossible_10_gold_medal_verify = create_verify_body("Archery", [create_participant("Thailand", 10, 0, 0),
                                                                             create_participant("China", 0, 0, 0),
                                                                             create_participant("Japan", 0, 0, 0)])
        self.impossible_10_silver_medal_verify = create_verify_body("Archery", [create_participant("Thailand", 0, 0, 0),
                                                                             create_participant("China", 0, 10, 0),
                                                                             create_participant("Japan", 0, 0, 0)])
        self.impossible_10_bronze_medal_verify = create_verify_body("Archery", [create_participant("Thailand", 0, 0, 0),
                                                                             create_participant("China", 0, 0, 0),
                                                                             create_participant("Japan", 0, 0, 10)])
        self.mono_sport_verify = create_verify_body("Archery", [create_participant("Thailand", 1, 0, 0), ])
        self.zero_medal_verify = create_verify_body("Boxing", [create_participant("Thailand", 0, 0, 0),
                                                               create_participant("India", 0, 0, 0),
                                                               create_participant("China", 0, 0, 0),
                                                               create_participant("Japan", 0, 0, 0)])
        self.empty_verify = create_verify_body("Archery", [])

    def test_success_medal_allocation(self):
        """Test if the success medal allocation return message correctly."""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.default_verify)
        self.assertEqual(200, request.status_code)
        self.assertEqual('{"Message":"Medal allocation successful."}', request.text)

    def test_tie_medal_warning(self):
        """Test if the tie medal scenario allocation return message correctly."""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.tie_gold_medal_verify)
        self.assertEqual(200, request.status_code)
        self.assertEqual('{"Message":"Medal allocation successful.","Warning":"There are 2 gold medals awarded, '
                         'Do you want to confirm this record?"}', request.text)
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.tie_silver_medal_verify)
        self.assertEqual(200, request.status_code)
        self.assertEqual('{"Message":"Medal allocation successful.","Warning":"There are 2 silver medals awarded, '
                         'Do you want to confirm this record?"}', request.text)

    def test_exceeded_default_logic_medal_allocation(self):
        """Test if the returned warning message is correct if the total amount is exceeded."""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.exceeded_medal_verify)
        self.assertEqual(200, request.status_code)
        self.assertEqual( '{"Message":"Medal allocation successful.","Warning":"There are 4 medals awarded, '
                          'Do you want to confirm this record?"}', request.text)
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.exceeded_repechage_medal_verify)
        self.assertEqual(200, request.status_code)
        self.assertEqual('{"Message":"Medal allocation successful.","Warning":"There are 5 medals awarded, '
                         'Do you want to confirm this record?"}', request.text)

    def test_mono_sport_medal_allocation_warning(self):
        """Test if the mono sport message return when only one country participated in the event."""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.mono_sport_verify)
        self.assertEqual(200, request.status_code)
        self.assertEqual('{"Message":"Medal allocation successful.","Monosport":"There are only 1 country in this '
                         'medal allocation, Do you want to confirm this record?"}', request.text)

    def test_400_bad_request_return_when_the_inputted_body_is_invalid(self):
        """Test if HTTP400 returned when inputting invalid body"""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.impossible_silver_and_bronze_medal_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"There are 3 gold medals awarded, No silver or bronze medal will be given."}', request.text)
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.impossible_silver_medal_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"There are 2 gold medals awarded, No silver medal will be given."}', request.text)
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.impossible_bronze_medal_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"There are 3 silver medals awarded, No bronze medal will be given."}', request.text)

    def test_400_bad_request_return_when_the_total_medal_given_is_zero(self):
        """Test if HTTP400 returned when the inputted total medals is 0"""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.zero_medal_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"There are 0 medals awarded, no need to record this body."}', request.text)

    def test_400_bad_request_return_when_the_inputted_body_is_empty(self):
        """Test if HTTP400 returned when inputting empty body"""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.empty_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"The participants can not be empty"}', request.text)

    def test_400_bad_request_return_when_any_specific_medals_given_exceed_the_limit_of_10(self):
        """Test if HTTP400 returned when inputting more than 10 medals of a specific type"""
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.impossible_10_gold_medal_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"There are 10 or more medals of a specific type awarded to a single country, '
                         'This should not be possible."}', request.text)
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.impossible_10_silver_medal_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"There are 10 or more medals of a specific type awarded to a single country, '
                         'This should not be possible."}', request.text)
        request = data_post_handler(self.VERIFY_PATH, self.TOKEN, data=self.impossible_10_bronze_medal_verify)
        self.assertEqual(400, request.status_code)
        self.assertEqual('{"detail":"There are 10 or more medals of a specific type awarded to a single country, '
                         'This should not be possible."}', request.text)
