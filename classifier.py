"""
Classifies a List of Input Itemsets from file named
Input.txt and outputs them in a file named Output.txt
"""

import apriori

def main():
    support_threshold = 0.02
    confidence_threshold = 0.1786
    coverage_threshold = 5
    top_k_rules = 10
    
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    print("Coverage Threshold is " + str(coverage_threshold))
    print("top_k_rules is " + str(top_k_rules))

    default_class = apriori.learn(support_threshold, confidence_threshold, coverage_threshold)
    f = open('Input.txt', 'r')
    g = open('Output.txt', 'w')

    for line in f:
        g.write(apriori.classify(default_class, line.strip().rstrip('\n').split(','), top_k_rules) + '\n')

    apriori.display_items()
    apriori.display_rules()

    f.close()
    g.close()

    print("Output written to file named Output.txt in the current working directory")

if __name__ == "__main__":
    main()
