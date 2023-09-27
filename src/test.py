#/usr/bin/env python3
from apriori import AprioriAlgorithm

if __name__ == "__main__":
    apriori = AprioriAlgorithm()
    apriori.gen_association_rules(0.3)