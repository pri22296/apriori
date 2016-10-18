from itertools import chain, combinations
from operator import itemgetter
from collections import namedtuple
import sys
import math
from progress_manager import ProgressManager
from printer_tools import BufferedPrinter, TablePrinter

#dict containing Itemsets as keys and their
#classwise counts as values
global_items = {}

#List of Rules where each rule is a namedtuple
#defined below
global_rules = []

Rule = namedtuple("Rule", ('antecedent', 'consequent', 'confidence', 'lift' , 'conviction', 'support'))
progress_mgr = ProgressManager(60, '>')

#Extract training datasets from file
def get_dataset_from_file(filename):
    file = open(filename, 'r')
    dataset = []
    for line in file:
        dataset.append(line.strip().rstrip('\n').split(','))
    return dataset

#Extract training classes for classification of dataset
def get_classes_from_file(filename):
    file = open(filename, 'r')
    classes = []
    for line in file:
        classes.append(line.strip().rstrip('\n'))
    return classes

#Returns a dict where itemsets are key and classes are values
def get_dataset_dict(dataset, classes):
    dataset_dict = {}
    for itemset, label in zip(dataset, classes):
        dataset_dict[tuple(itemset)] = label
    return dataset_dict

#Get all the Item Values present in the dataset
def get_initial_items(dataset, **kwargs):
    progress_mgr.allow_to_print(kwargs.get('publish_progress', False))
    l = []
    progress_mgr.begin()
    items = set(chain(*dataset))
    items_length = len(items)
    
    for index, item in enumerate(items):
        
        progress_percent = ((index + 1) / items_length) * 100
        progress_mgr.publish(progress_percent)
        
        l.append([item])
        
    progress_mgr.end()
    return sorted(l)

#Returns the count of items in the dataset irrespective of the class
def get_count(dataset, items):

    try:
        classwise_count = global_items[tuple(set(items))]
        return get_itemcount_from_classwise_count(classwise_count)
    except KeyError:
        pass
            
    count = 0
    for data in dataset:
        found = True
        for item in items:
            if item not in data:
                found = False
                break
            else:
                pass
        if found:
            count += 1
    return count

#Returns a dict of classes as keys and
#[count of items where class is 'key' in dataset, count of class 'key'] as value
def get_classwise_count(dataset, classes, items):
    count_class = dict()
    for key in set(classes):
        count_class[key] = [0,0]
    for i,data in enumerate(dataset):
        found = True
        for item in items:
            if item not in data:
                found = False
                break
            else:
                pass
        if found:
            count_class[classes[i]][0] += 1
        count_class[classes[i]][1] += 1
    return count_class

def get_support(dataset, items):
    return round(get_count(dataset, items)/len(dataset), 3)

def new_get_support(dataset, classes, items, label):
    if label is not None:
        cnt = get_classwise_count(dataset, classes, items)[label]
        return cnt[0]/cnt[1]
    else:
        c1,c2 = 0,0
        for it in get_classwise_count(dataset, classes, items).values():
            c1 += it[0]
            c2 += it[1]
        return c1/c2

#returns the count of the class 'label' in training classes
def get_class_count(classes, label):
    count = 0
    for c in classes:
        if c == label:
            count += 1
    return count

#returns True if l1 and l2 differ by their last element
def should_join_candidate(candidate1, candidate2):
    length = len(candidate1)
    for i in range(length-1):
        if candidate1[i] != candidate2[i]:
            return False
    #if candidate1[length-1] == candidate2[length-1]:
        #return False
    #If both candidates belong to same class then they should not join
    #If classwise data is not available then this just compares equality
    if candidate1[length-1].split('-')[0] == candidate2[length-1].split('-')[0]:
        return False
    return True

#generates k+1 sized itemsets from k sized itemsets
def generate_new_items(items, **kwargs):
    new_items = []

    progress_mgr.allow_to_print(kwargs.get('publish_progress', False))
    progress_mgr.begin()
    items_length = len(items)
    
    for i in range(items_length):
        for j in range(i, items_length):
            
            progress_percent = 100 * ((i + 1) * items_length + (j + 1)) / (items_length * (items_length + 1))
            progress_mgr.publish(progress_percent)
            
            if should_join_candidate(items[i], items[j]):
                new_items.append(sorted(list(set(items[i]).union(set(items[j])))))
    progress_mgr.end()
    return new_items

def get_itemcount_from_classwise_count(classwise_count):
    net_itemcount = 0
    for itemcount, class_count in classwise_count.values():
        net_itemcount += itemcount
    return net_itemcount

#To remove itemsets having support less than support Threshold
def prune_items(dataset, classes, items, support_threshold, **kwargs):

    progress_mgr.allow_to_print(kwargs.get('publish_progress', False))
    progress_mgr.begin()
    
    to_be_pruned = []
    items_length = len(items)
    
    for index, item in enumerate(items):
        progress_percent = ((index + 1) / items_length) * 100
        progress_mgr.publish(progress_percent)

        classwise_count = get_classwise_count(dataset, classes, item)
        item_count = get_itemcount_from_classwise_count(classwise_count)
        item_support = round(item_count / len(dataset), 3)
        
        if item_support < support_threshold:
            to_be_pruned.append(item)
        else:
            global_items[tuple(set(item))] = classwise_count

    progress_mgr.end()
    
    for item in to_be_pruned:
        items.remove(item)
    return items

#Unused function
#Just here so that if needed in future
#Handy function to generate subsets
def get_subsets(arr):
    return chain(*[combinations(arr, i+1) for i in range(len(arr))])

def generate_rules(dataset, classes, items, confidence_threshold, support_threshold, **kwargs):
    global global_rules

    items_length = len(items)
    progress_mgr.allow_to_print(kwargs.get('publish_progress', False))
    progress_mgr.begin()
    
    for index, item in enumerate(items):
        
        progress_percent = ((index + 1)/ items_length) * 100
        progress_mgr.publish(progress_percent)
            
        if len(item) > 0:
            
            classwise_count = global_items[tuple(set(item))]
            item_count = get_itemcount_from_classwise_count(classwise_count)
            
            for label in set(classes):
                
                count = classwise_count[label]
                rule_support = round(count[0]/len(dataset), 3)
                item_support = round(item_count/len(dataset), 3)
                
                try:
                    confidence = round(count[0]/item_count, 3)
                    confidence_expected = count[1]/len(dataset)
                    lift = round(confidence/confidence_expected, 3)
                    conviction = round((1 - (confidence/lift))/(1-confidence), 3)
                except (ZeroDivisionError):
                    confidence = 0
                    lift = 1
                    conviction = 1
                    
                if confidence >= confidence_threshold:
                    rule = Rule(tuple(item), label, confidence, lift, conviction, item_support)
                    global_rules.append(rule)
                    
    progress_mgr.end()
    global_rules = list(set(global_rules))

#Returns True if data is a superset of antecedent of rule,
#and label is the consequent of rule
#if label is None, then only data is checked
def match_rule_data(data, rule, label):
    if set(rule.antecedent).issubset(set(data)) and (label == rule.consequent or label is None):
        return True
    else:
        return False

#calculates the default class
#Dataset for which no rule matches will be classified using the default rule
def get_default_class(dataset, classes, support_threshold, confidence_threshold, **kwargs):
    global global_rules

    progress_mgr.allow_to_print(kwargs.get('publish_progress', False))
    progress_mgr.begin()

    dataset_length = len(dataset)
    global_rules_length = len(global_rules)
    
    c = dict.fromkeys(set(classes), 0)
    for i, data in enumerate(dataset):
        is_match = False
        for j, rule in enumerate(global_rules):

            progress_percent = 100 * (i * global_rules_length + (j + 1)) / (dataset_length * global_rules_length) 
            progress_mgr.publish(progress_percent)
            
            if rule.support < support_threshold or rule.confidence < confidence_threshold:
                continue
            if match_rule_data(data, rule, classes[i]):
                is_match = True
                break
        if is_match is False:
            c[classes[i]] += 1
            
    progress_mgr.end()
    
    return max(c.items(), key=itemgetter(1))[0]
    
def prune_rules(dataset, classes, coverage_threshold, **kwargs):
    global global_rules
    global global_items
    pruned_rules = []
    data_count = [0]*len(dataset)

    progress_mgr.allow_to_print(kwargs.get('publish_progress', False))
    progress_mgr.begin()
    global_rules_length = len(global_rules)
    dataset_length = len(dataset)
    
    for rule_index, rule in enumerate(global_rules):
        rule_add = False
        for i,data in enumerate(dataset):
            progress_percent = 100 * (rule_index * dataset_length + (i + 1)) / (global_rules_length * dataset_length)
            progress_mgr.publish(progress_percent)
            
            if match_rule_data(data, rule, classes[i]) and data_count[i] >= 0:
                rule_add = True
                data_count[i] += 1
                if data_count[i] >= coverage_threshold:
                    data_count[i] = -1
        if rule_add:
            pruned_rules.append(rule)

    progress_mgr.end()
    
    return pruned_rules
                
def get_score(rule):
    return rule.lift

def classify(default_class, input_data, support_threshold, confidence_threshold, top_k_rules):
    matching_rules = []
    for rule in global_rules:
        if rule.support < support_threshold or rule.confidence < confidence_threshold:
            continue
        if match_rule_data(input_data, rule, None):
           matching_rules.append(rule)
        if len(matching_rules) == top_k_rules:
            break
    if len(matching_rules) > 0:
        score = dict()
        for rule in matching_rules:
            score[rule.consequent] = score.get(rule.consequent, 0) + get_score(rule)
        return max(score.items(), key=itemgetter(1))[0]
    else:
        return default_class

def print_if_verbose(verbose, *args, **kwargs):
    if verbose:
        print(*args, **kwargs)
        
def learn(support_threshold, confidence_threshold, coverage_threshold, **kwargs):
    global global_rules
    global_rules = []
    
    try:
        #Get dataset from file
        dataset = get_dataset_from_file('Itemset_train.txt')

        #Get training classes from file
        classes = get_classes_from_file('Classes_train.txt')
    except(FileNotFoundError):
        print("\nUnable to open Training Dataset")
        sys.exit(0)

    verbose = kwargs.get('verbose', False)

    #Get items present in dataset
    print_if_verbose(verbose, "Finding candidate Itemsets of size 1")
    items = get_initial_items(dataset, publish_progress = verbose)
    print_if_verbose(verbose, "Found {} candidate Itemsets".format(len(items)))
    
    itemset_size = 1
    while len(items) > 0:
        
        print_if_verbose(verbose, "Finding frequent Itemsets from candidates")
        items = prune_items(dataset, classes, items, support_threshold, publish_progress = verbose)
        print_if_verbose(verbose, "Found {} frequent Itemsets".format(len(items)))
        
        print_if_verbose(verbose, "Generating rules from those Itemsets")
        itemset_size += 1
        prev_rule_len = len(global_rules)
        generate_rules(dataset, classes, items, confidence_threshold, support_threshold, publish_progress = verbose)
        rule_gen_count = len(global_rules) - prev_rule_len
        print_if_verbose(verbose, "{} rule(s) generated".format(rule_gen_count))
        
        print_if_verbose(verbose, "\n\nFinding candidate Itemsets of size {}".format(itemset_size))
        items = generate_new_items(items, publish_progress = verbose)
        print_if_verbose(verbose, "Found {} candidate Itemsets".format(len(items)))

    print_if_verbose(verbose, "\n\nRule Generation complete")
    print_if_verbose(verbose, "Total {} rules generated".format(len(global_rules)))

    global_rules = sorted(global_rules, key=lambda rule: get_score(rule), reverse=True)
    
    print_if_verbose(verbose, "\n\nPruning rules based on coverage_threshold")
    global_rules = prune_rules(dataset, classes, coverage_threshold, publish_progress = verbose)
    print_if_verbose(verbose, "{} rules left after pruning".format(len(global_rules)))

    print_if_verbose(verbose, "\n\nCalculating default class")
    default_class = get_default_class(dataset, classes, support_threshold, confidence_threshold, publish_progress = verbose)
    print_if_verbose(verbose, "default class is {}".format(default_class))
    
    return default_class

def test(default_class, support_threshold, confidence_threshold, top_k_rules, **kwargs):
    global global_rules
    
    try:
        test_dataset = get_dataset_from_file('Itemset_test.txt')
        test_classes = get_classes_from_file('Classes_test.txt')
    except(FileNotFoundError):
        print("\nrun DataGen.py first")
        sys.exit(0)
        
    correct_output_counter, incorrect_output_counter = 0, 0
    global_rules = sorted(global_rules, key=lambda rule: get_score(rule), reverse=True)
    
    if kwargs.get('verbose', False) is True:
        print("\nINCORRECTLY LABELLED ITEMSETS\n")
        
        table_printer = TablePrinter(3)
        table_printer.set_column_headers("Itemset", "Expected", "Output")
        table_printer.set_column_alignments('<', '^', '^')
        table_printer.set_column_widths(120, 10, 10)
        table_printer.begin()
        
    for i,test_data in enumerate(test_dataset):
        c = classify(default_class, test_data, support_threshold, confidence_threshold, top_k_rules)
        if(c == test_classes[i]):
            correct_output_counter += 1
        else:
            incorrect_output_counter += 1
            if kwargs.get('verbose', False) is True:
                table_printer.append_row(", ".join(test_data), test_classes[i], c)
                
    if kwargs.get('verbose', False) is True:
        table_printer.end()
        print("\nClassified {} Inputs".format(len(test_dataset)))
        print("Correctly Classified {} Inputs".format(correct_output_counter))
    
    return round((correct_output_counter/(incorrect_output_counter + correct_output_counter))*100, 3)

def display_items():
    global global_items
    
    table_printer = TablePrinter(2)
    table_printer.set_column_headers("Itemset", "Support")
    table_printer.set_column_alignments('<', '^')
    table_printer.set_column_widths(100, 15)
    table_printer.begin()
    
    dataset_length = len(get_dataset_from_file('Classes_train.txt'))
    for item, classwise_count in global_items.items():
        itemcount = get_itemcount_from_classwise_count(classwise_count)
        table_printer.append_row(", ".join(item), round(itemcount/dataset_length, 3))

    table_printer.end()

def display_rules():
    global global_rules

    table_printer = TablePrinter(6)
    table_printer.set_column_headers("Antecedent","Consequent","Confidence","Lift","Conviction","Support")
    table_printer.set_column_alignments('<', '^', '^', '^', '^', '^')
    table_printer.set_column_widths(80, 10, 10, 10, 10, 10)
    table_printer.begin()
    
    for rule in global_rules:
        table_printer.append_row(", ".join(rule.antecedent), rule.consequent, rule.confidence, rule.lift, rule.conviction, rule.support)

    table_printer.end()


def main():
    global global_rules

    support_threshold = 0.4
    confidence_threshold = 0.4
    coverage_threshold = 10
    top_k_rules = 50
    
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    print("Coverage Threshold is " + str(coverage_threshold))
    print("top_k_rules is " + str(top_k_rules))
    print()

    default_class = learn(support_threshold, confidence_threshold, coverage_threshold, verbose = True)

    print("\n\nFREQUENT ITEMSETS\n")
    
    display_items()
        
    print("\n\nRULES INFERENCED FROM DATA\n")

    display_rules()

    print("\n\nOverall Accuracy: {}%".format(test(default_class, support_threshold, confidence_threshold, top_k_rules, verbose = True)))

if __name__ == '__main__':
    main()
