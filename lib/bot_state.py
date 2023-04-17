from collections import namedtuple
from lib.transition_functions import *
# from transitions import transitions
import lib.transitions as transitions
import lib.var as var
import configparser
import lib.timer_related as timer_related


class BotState():
    tok_next_t = namedtuple('tok_next_t', ['func', 'next_state'])

    def __init__(self):
        self.tok_next = {}
        # super().__init__(early_retreats,emu)
        self.early_retreats = var.early_retreats
        self.emu = var.emu
        self.transitions = transitions.transitions
        self.transitions_retreat = self.transitions
        self.transitions_retreat['IN_BATTLE'].append(
            (retreat_transition, 'RETREAT'))

        self.add_state()

    def add_state(self):
        if (self.emu):
            trans = self.transitions_retreat
        else:
            trans = self.transitions
        for state in trans:
            if state not in self.tok_next:
                self.tok_next[state] = []
            for tuple in trans[state]:
                self.tok_next[state].append(
                    self.tok_next_t(tuple[0], tuple[1]))

    def print_state(self):
        print(f"State: {var.current_state}")

    def run_state(self):
        state_transitions = self.tok_next[var.current_state]
        for condition_function, target_state in state_transitions:
            # Check the condition
            if condition_function():
                # timer_related.TimerManager.record_timer()
                var.current_state = target_state
                self.print_state()
                break

    def update_state(self):
        # print("Update current state")
        if (imgSearch.check_retreat_button()
                or imgSearch.check_collect_button()):
            var.current_state = 'IN_BATTLE'
            print(f"State updated: {var.current_state}")
            return
        if (imgSearch.check_mission_text()):
            var.current_state = 'NEXT'
            print(f"State updated: {var.current_state}")
            return
        if (imgSearch.check_next_button()):
            var.current_state = 'COLLECT_REWARDS'
            print(f"State updated: {var.current_state}")
            return
