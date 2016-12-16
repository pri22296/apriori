"""
Classifies a List of Input Itemsets from file named
Input.txt and outputs them in a file named Output.txt
"""

import apriori

def classify(unclassified_inputs_file_name, output_file_name, **kwargs):
    """Classify data using ARM based classifier.

    Classify set of unclassified data from a user specified file and writes the predicted output
    to another user specified file.

    Parameters
    ----------
    unclassified_inputs_file_name : str
        Name of the file from which to read unclassified inputs.

    output_file_name : str
        Name of file where output of the classifer will be written.

    verbose : bool, optional
        Specifies whether to print logs of operation performed by the method
        to the console. Default is False.
    """
    verbose = kwargs.get('verbose', False)
    
    support_threshold = 0.2
    confidence_threshold = 0.2
    coverage_threshold = 10
    top_k_rules = 50

    if verbose:
        print("Support Threshold is " + str(support_threshold))
        print("Confidence Threshold is " + str(confidence_threshold))
        print("Coverage Threshold is " + str(coverage_threshold))
        print("top_k_rules is " + str(top_k_rules))

    default_class = apriori.learn(support_threshold, confidence_threshold, coverage_threshold)
    unclassified_inputs_file = open(unclassified_inputs_file_name, 'r')
    output_file = open(output_file_name, 'w')

    for line in unclassified_inputs_file:
        input_data = line.strip().rstrip('\n').split(',')
        output_file.write(apriori.classify(default_class, input_data, support_threshold, confidence_threshold, top_k_rules) + '\n')

    if verbose:
        apriori.display_items()
        apriori.display_rules()

    unclassified_inputs_file.close()
    output_file.close()

    if verbose:
        print("Output written to file named Output.txt in the current working directory")

def main():
    classify('Input.txt', 'Output.txt', verbose = True)

if __name__ == "__main__":
    main()
