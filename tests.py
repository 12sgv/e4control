from otree.api import Bot, Submission
import random

from otree.app_template import pages


#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        #instructions app
        # Enter 'bot' in the prolificID field and submit the page
        yield Submission(pages.ProlificID, {'prolificID': 'bot'})
        yield Submission(pages.Consent)
        yield Submission(pages.GeneralInstructions)

        #Voting app
        yield pages.GroupAssignment
        yield pages.NoGroup
        #randomly vote for either the office or remote policy on the vote page
        vote = random.choice(['Office', 'Remote'])
        yield Submission*(pages.Voting, {'policy_vote': vote})
        yield pages.MyPolicyVoteWaitPage
        yield pages.GroupTimeoutPage
        yield Submission(pages.VoteOutcome)

        #dictator app
        yield pages.PairGroupWait
        #answer the partner check question correctly
        yield Submission(pages.PartnerCheck, {'partner_check': self.player.manipulation_check_correct_answer})
        #randomly offer between 0-100 in the offer page
        offer = random.randint(0, 100)
        yield Submission(pages.Offer, {'giving': offer})
        yield pages.MyResultsWaitPage

        #survey app
        # On the PEQ page, enter the specified values and submit the page
        yield Submission(pages.PEQ, {
            'vote_preference': 1,
            'positive_affect': 1,
            'negative_affect': 1,
            'group_id1': 1,
            'group_id2': 1,
            'group_id3': 1,
            'group_id4': 1,
            'group_id5': 1,
            'company_care': 1
        })
        # On the Demographics1 page, enter the specified values and submit the page
        yield Submission(pages.Demographics1, {
            'employed_field': 1,
            'work_location': 1,
            'location_preference': 1,
            'team_size': 1,
            'industry': 1,
            'work_experience': 0,
            'firm_allow_input': True
        })
        # On the Demographics2 page, enter the specified values and submit the page
        yield Submission(pages.Demographics2, {
            'firm_input': 1,
            'firm_input_other': "bot is here",
            'firm_feel_input': 1,
            'firm_full_remote_pandemic': True,
            'firm_adjust_post_pandemic': 1
        })
        # On the Demographics3 page, enter the specified values and submit the page
        yield Submission(pages.Demographics3, {
            'age': 55,
            'gender': 1,
            'education': 1
        })

        #payment_info app
        yield pages.ResultsComplete
        yield pages.ResultsNotPaired
        yield pages.ResultsTimedOut
        yield Submission(pages.PaymentInfor, {'feedback': 'bot'})