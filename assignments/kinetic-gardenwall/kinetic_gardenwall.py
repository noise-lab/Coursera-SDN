'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 8 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pyretic.lib.corelib import *
from pyretic.lib.std import *

from pyretic.kinetic.fsm_policy import *
from pyretic.kinetic.drivers.json_event import JSONEvent
from pyretic.kinetic.smv.model_checker import *
from pyretic.kinetic.util.rewriting import *
from pyretic.kinetic.apps.mac_learner import *

#####################################################################################################
# Author: Hyojoon Kim
# * App launch
#   - pyretic.py pyretic.kinetic.apps.gardenwall
#
# * Mininet Generation (in "~/pyretic/pyretic/kinetic" directory)
#   - sudo mn --controller=remote,ip=127.0.0.1 --mac --arp --switch ovsk --link=tc --topo=single,3
#
# * Start ping from h1 to h2 
#   - mininet> h1 ping h2
#
# * Send Event to block traffic "h1 ping h2" (in "~/pyretic/pyretic/kinetic" directory)
#   - python json_sender.py -n infected -l True --flow="{srcip=10.0.0.1}" -a 127.0.0.1 -p 50001
#
# * Now, make h1's flow not be affected by IDS infection event(in "~/pyretic/pyretic/kinetic" directory)
#   h1's traffic will be forwarded to 10.0.0.3.
#   - python json_sender.py -n exempt -l True --flow="{srcip=10.0.0.1}" -a 127.0.0.1 -p 50001
#
# * Events to now allfow traffic again (in "~/pyretic/pyretic/kinetic" directory)
#   - python json_sender.py -n infected -l False --flow="{srcip=10.0.0.1}" -a 127.0.0.1 -p 50001
#####################################################################################################

class gardenwall(DynamicPolicy):
    def __init__(self):

        # Garden Wall
        def redirectToGardenWall():
            client_ips = [IP('10.0.0.1'), IP('10.0.0.2')]
            rewrite_policy = rewriteDstIPAndMAC(client_ips, '10.0.0.3')
            return rewrite_policy

        ### DEFINE THE LPEC FUNCTION

        def lpec(f):
            # Your logic here
            # return match =

        ## SET UP TRANSITION FUNCTIONS

        @transition
        def exempt(self):
            self.case(occurred(self.event),self.event)

        @transition
        def infected(self):
            self.case(occurred(self.event),self.event)

        @transition
        def policy(self):
            # If exempt, redirect to gardenwall. 
            #  - rewrite dstip to 10.0.0.3
            self.case(test_and_true(V('exempt'),V('infected')), C(redirectToGardenWall()))

            # If infected, drop
            # Your logic here
            # self.case ()

            # Else, identity    
            self.default(C(identity))


        ### SET UP THE FSM DESCRIPTION

        self.fsm_def = FSMDef(
            infected=FSMVar(type=BoolType(), 
                            init=False, 
                            trans=infected),
            # Your logic here
            # exempt =
            # policy =
            )

        ### SET UP POLICY AND EVENT STREAMS

        fsm_pol = FSMPolicy(lpec,self.fsm_def)
        json_event = JSONEvent()
        json_event.register_callback(fsm_pol.event_handler)

        super(gardenwall,self).__init__(fsm_pol)


def main():
    pol = gardenwall()

    # For NuSMV
    smv_str = fsm_def_to_smv_model(pol.fsm_def)
    mc = ModelChecker(smv_str,'gardenwall')  

    ## Add specs
    mc.add_spec("FAIRNESS\n  infected;")
    mc.add_spec("FAIRNESS\n  exempt;")

    # Now, traffic is dropped only when exempt is false and infected is true
    mc.add_spec("SPEC AG (infected & !exempt -> AX policy=policy_2)")

    # If exempt is true, next policy state to redirect to gardenwall, even if infected
    mc.add_spec("SPEC AG (infected & exempt -> AX policy=policy_1)")

    # If infected is false, next policy state is always 'allow'
    mc.add_spec("SPEC AG (!infected -> AX policy=policy_3)")

    ### Policy state is 'allow' until infected is true.
    mc.add_spec("SPEC A [ policy=policy_3 U infected ]")

    # Save NuSMV file
    mc.save_as_smv_file()

    # Verify
    mc.verify()

    return pol >> mac_learner()
