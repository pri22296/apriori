import apriori

def main():
    support_threshold = 0.0001
    confidence_threshold = 0.0001
    coverage_threshold = 50
    top_k_rules = 100
    
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    print("Coverage Threshold is " + str(coverage_threshold))

    default_rule = apriori.learn(support_threshold, confidence_threshold, coverage_threshold)
    f = open('Itemset_train.txt', 'r')
    g = open('output.txt', 'w')

    for line in f:
        g.write(apriori.classify(default_rule, line.strip().rstrip('\n').split(','), top_k_rules) + '\n')

    apriori.display_items()
    apriori.display_rules()

    f.close()
    g.close()

    print("Output written to file named output.txt in the current working directory")

main()
