from . import *


#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.player.participant.vars['r23'] == False:
            yield Submission(a22, check_html=False)
            yield a23
            
            #for main group
 #           if not self.participant.vars['is_out'] == 1:
  #              #get vars for a24
  #              if self.player.participant.vars['treatment'] == 1:
#                    wrong1 = 4
 #                   wrong2 = 2
  #                  wrong3 = 3
  #                  manipulation_answer = 1
  #              elif self.player.participant.vars['treatment'] == 2:
#                    wrong1 = 1
#                   wrong2 = 4
#                  wrong3 = 3
  #                  manipulation_answer = 2
  #              elif self.player.participant.vars['treatment'] == 3:
#                    wrong1 = 1
#                   wrong2 = 2
#                  wrong3 = 4
  #                  manipulation_answer = 3
  #              else:
#                    wrong1 = 1
 #                   wrong2 = 2
  #                  wrong3 = 3
  #                  manipulation_answer = 4
                #Check that the wrong answers are, in fact, wrong
#                yield SubmissionMustFail(pages.a24, dict(partner_check=wrong1)
#                yield SubmissionMustFail(pages.a24, dict(partner_check=wrong2)
#                yield SubmissionMustFail(pages.a24, dict(partner_check=wrong3)
  #              yield a24, dict(partner_check=manipulation_answer)
  #              #vars for a25
  #              offer = random.randint(0, 100)
  #              yield Submission(a25, {'giving': offer}, check_html=False)
  #          #for 5th person
  #          if self.participant.vars['not_paired'] == 1:
  #              yield a26
  #              offer = random.randint(0, 100)
  #              yield Submission(a27, {'giving': offer}, check_html=False)
  #              # generate random responses for PEQ 5th Person
  #              vp = random.randint(-3, 3)
  #              vv = random.randint(-3, 3)
  #              a = random.randint(-3, 3)
  #              expectation_choices = ['Remote'] * 86 + ['Office'] * 14
  #              ev = random.choice(expectation_choices)
  #              es = random.randint(-3, 3)
  #              # On the PEQ page, enter the specified values and submit the page
  #              yield a28, dict(
  #                  vote_preference=vp,
  #                  vote_valued=vv,
  #                  affect=a,
  #                  expectation_valence=ev,
  #                  expectation_strength=es,
  #              )


