import unittest
from router.record import verify_medal
from models import VerifyBody


class TestRecordMedal(unittest.TestCase):
    def setUp(self):
        self.default_verify = VerifyBody(sport_name="Archery", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "China", "medal": {"gold": 0, "silver": 1, "bronze": 0}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 0, "bronze": 1}}, ])
        self.repechage_verify = VerifyBody(sport_name="Boxing", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "India", "medal": {"gold": 0, "silver": 1, "bronze": 0}},
            {"country": "China", "medal": {"gold": 0, "silver": 0, "bronze": 1}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 0, "bronze": 1}}, ])
        self.tie_gold_medal_verify = VerifyBody(sport_name="Archery", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "China", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 0, "bronze": 1}}, ])
        self.tie_silver_medal_verify = VerifyBody(sport_name="Boxing", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "India", "medal": {"gold": 0, "silver": 0, "bronze": 1}},
            {"country": "China", "medal": {"gold": 0, "silver": 1, "bronze": 0}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 1, "bronze": 0}}, ])
        self.exceeded_medal_verify = VerifyBody(sport_name="Archery", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "India", "medal": {"gold": 0, "silver": 0, "bronze": 1}},
            {"country": "China", "medal": {"gold": 0, "silver": 0, "bronze": 1}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 1, "bronze": 0}}, ])
        self.exceeded_repechage_medal_verify = VerifyBody(sport_name="Archery", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "India", "medal": {"gold": 0, "silver": 0, "bronze": 1}},
            {"country": "China", "medal": {"gold": 0, "silver": 0, "bronze": 1}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 1, "bronze": 0}},
            {"country": "Laos", "medal": {"gold": 0, "silver": 0, "bronze": 1}}, ])
        self.impossible_silver_and_bronze_medal_verify = VerifyBody(sport_name="Archery", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "China", "medal": {"gold": 1, "silver": 0, "bronze": 1}},
            {"country": "Japan", "medal": {"gold": 1, "silver": 1, "bronze": 0}}, ])
        self.impossible_silver_medal_verify = VerifyBody(sport_name="Archery", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "China", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 1, "bronze": 0}}, ])
        self.impossible_bronze_medal_verify = VerifyBody(sport_name="Boxing", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 0, "bronze": 0}},
            {"country": "India", "medal": {"gold": 0, "silver": 1, "bronze": 1}},
            {"country": "China", "medal": {"gold": 0, "silver": 1, "bronze": 0}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 1, "bronze": 0}}, ])
        self.mono_sport_verify = VerifyBody(sport_name="Archery", participants=[
            {"country": "Thailand", "medal": {"gold": 1, "silver": 1, "bronze": 1}}, ])
        self.zero_medal_verify = VerifyBody(sport_name="Boxing", participants=[
            {"country": "Thailand", "medal": {"gold": 0, "silver": 0, "bronze": 0}},
            {"country": "India", "medal": {"gold": 0, "silver": 0, "bronze": 0}},
            {"country": "China", "medal": {"gold": 0, "silver": 0, "bronze": 0}},
            {"country": "Japan", "medal": {"gold": 0, "silver": 0, "bronze": 0}}, ])
        self.empty_verify = VerifyBody(sport_name="Archery", participants=[])

    def test_success_medal_allocation(self):
        """Test if the success medal allocation return message correctly."""
        message = verify_medal(self.default_verify)
        self.assertEqual(message, {"Message": "Medal allocation successful."})
        message = verify_medal(self.repechage_verify)
        self.assertEqual(message, {"Message": "Medal allocation successful."})

    def test_tie_medal_warning(self):
        """Test if the tie medal scenario allocation return message correctly."""
        message = verify_medal(self.tie_gold_medal_verify)
        self.assertEqual(message, {"Message": "Medal allocation successful.",
                                   "Warning": f"There are 2 gold medals awarded, Do you want to confirm this record?"})
        message = verify_medal(self.tie_silver_medal_verify)
        self.assertEqual(message, {"Message": "Medal allocation successful.",
                                   "Warning": f"There are 2 silver medals awarded, Do you want to confirm this record?"})

    def test_exceeded_default_logic_medal_allocation(self):
        """Test if the returned warning message is correct if the total amount is exceeded."""
        message = verify_medal(self.exceeded_medal_verify)
        self.assertEqual(message, {"Message": "Medal allocation successful.",
                                   "Warning": f"There are 4 medals awarded, Do you want to confirm this record?"})
        message = verify_medal(self.exceeded_repechage_medal_verify)
        self.assertEqual(message, {"Message": "Medal allocation successful.",
                                   "Warning": f"There are 5 medals awarded, Do you want to confirm this record?"})

    def test_mono_sport_medal_allocation_warning(self):
        """Test if the mono sport message return when only one country participated in the event."""
        message = verify_medal(self.mono_sport_verify)
        self.assertEqual(message, {"Message": "Medal allocation successful.",
                                   "Monosport": 'There are only 1 country in this medal allocation, '
                                                'Do you want to confirm this record?'})

    def test_400_bad_request_return_when_the_inputted_body_is_invalid(self):
        """Test if HTTP400 returned when inputting invalid body"""
        message = verify_medal(self.impossible_silver_and_bronze_medal_verify)
        self.assertEqual(message, {'status': 'error', 'message': "(400, 'There are 3 gold medals awarded, "
                                                                 "No silver or bronze medal will be given.')"})
        message = verify_medal(self.impossible_silver_medal_verify)
        self.assertEqual(message, {'status': 'error', 'message': "(400, 'There are 2 gold medals awarded, "
                                                                 "No silver medal will be given.')"})
        message = verify_medal(self.impossible_bronze_medal_verify)
        self.assertEqual(message, {'status': 'error', 'message': "(400, 'There are 3 silver medals awarded, "
                                                                 "No bronze medal will be given.')"})

    def test_400_bad_request_return_when_the_total_medal_given_is_zero(self):
        """Test if HTTP400 returned when the inputted total medals is 0"""
        message = verify_medal(self.zero_medal_verify)
        self.assertEqual(message, {'status': 'error', 'message': "(400, 'There are 0 medals awarded, "
                                                                 "no need to record this body.')"})

    def test_400_bad_request_return_when_the_inputted_body_is_empty(self):
        """Test if HTTP400 returned when inputting empty body"""
        message = verify_medal(self.empty_verify)
        self.assertEqual(message, {'status': 'error', 'message': "(400, 'The participants can not be empty')"})
