#!/usr/bin/env python3
from copy import deepcopy
from frozenlist import FrozenList

class AprioriAlgorithm:
    def __init__(self):
        self.observations = [
            {"milk", "bread"},
            {"bread", "sugar"},
            {"bread", "butter"},
            {"milk", "bread", "sugar"},
            {"milk", "bread", "butter"},
            {"milk", "bread", "butter"},
            {"milk", "sugar"},
            {"milk", "sugar"},
            {"sugar", "butter"},
            {"milk", "sugar", "butter"},
            {"milk", "bread", "butter"}
        ]

    def gen_association_rules(self, min_support):
        events = self.unique_events()
        one_itemsets = self.freq_itemsets(events, min_support)
        max_k = self.max_items()

        print(f"One item sets: {one_itemsets}")
        candidates = one_itemsets
        print(f"max_k: {max_k}")
        for i in range(2, max_k+1):
            next_candidates = self.generate_candidates(candidates, events, min_support)
            print("Candidates: ", next_candidates)

            if len(next_candidates) > 0:
                candidates = deepcopy(next_candidates)
            else:
                break
        
        for candidate in candidates:
            for event in candidate:
                lhs = set(candidate)
                rhs = event
                lhs.remove(event)
                confidence = self.confidence(lhs, rhs)
                print(f"{lhs} -> {rhs}: Confidence={confidence}")

    def confidence(self, lhs, rhs):
        itemset = deepcopy(lhs)
        itemset.update(rhs)

        return self.support(itemset) / self.support(lhs)

    def support(self, events):
        n = len(self.observations)
        count = 0
        for ob in self.observations:
            condition_met = True
            for event in events:
                if event not in ob:
                    condition_met = False
            if condition_met:
                count += 1

        return count * 1.0 / n

    def unique_events(self):
        events = set([])
        for ob in self.observations:
            for event in ob:
                events.add(event)
        
        return events

    def freq_itemsets(self, events, min_support):
        one_itemsets = set([])
        for event in events:
            support = self.support({event})
            if support > min_support:
                one_itemsets.add(event)

        return list(one_itemsets)

    def max_items(self):
        return max([len(ob) for ob in self.observations])

    def generate_candidates(self, itemsets, unique_items, min_support):
        candidate_list = set([])
        for x in itemsets:
            for y in unique_items:
                candidate = deepcopy(x)
                if type(candidate) is str:
                    candidate = {candidate}
                else:
                    candidate = set(candidate)

                print("Before add: ", candidate)
                candidate.add(y)
                print("After add: ", candidate)
                eligible_candidate = FrozenList(candidate)
                eligible_candidate.freeze()

                if eligible_candidate not in candidate_list and self.support(eligible_candidate) > min_support:
                    print("Candidate found: ", eligible_candidate)
                    candidate_list.add(eligible_candidate)

        return candidate_list