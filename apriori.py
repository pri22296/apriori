from itertools import chain, combinations
from operator import itemgetter
from collections import namedtuple
import sys
import math
from progress_manager import ProgressManager

global_items = []
global_rules = []

Rule = namedtuple("Rule", ('antecedent', 'consequent', 'confidence', 'lift' , 'conviction', 'support'))
Item = namedtuple("Item", ('itemset', 'support'))
progress_mgr = ProgressManager(30, '.')

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

#Get all the Item Values present in the dataset
def get_initial_items(dataset):
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
    
    for global_item in global_items:
        if(len(global_item.itemset) == len(items)):
            if(len(set(items).intersection(set(global_item.itemset))) == len(global_item.itemset)):
                return int(round(global_item.support * len(dataset), 0))
            
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
def should_join_candidate(l1, l2):
    l = len(l1)
    for i in range(l-1):
        if l1[i] != l2[i]:
            return False
    #if l1[l-1] == l2[l-1]:
        #return False
    #If both candidates belong to same class then they should not join
    #If classwise data is not available then this just compares equality
    if l1[l-1].split('-')[0] == l2[l-1].split('-')[0]:
        return False
    return True

#generates k+1 sized itemsets from k sized itemsets
def generate_new_items(items):
    new_items = []

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

#To remove itemsets having support less than support Threshold
def prune_items(dataset, items, support_threshold):
    
    progress_mgr.begin()
    
    to_be_pruned = []
    items_length = len(items)
    
    for index, item in enumerate(items):
        progress_percent = ((index + 1) / items_length) * 100
        progress_mgr.publish(progress_percent)

        item_support = round(get_count(dataset, item) / len(dataset), 3)
        
        if item_support < support_threshold:
            to_be_pruned.append(item)
        else:
            item_namedtuple = Item(item, item_support)
            global_items.append(item_namedtuple)
        #if get_count(dataset, item) < len(dataset)*support_threshold:
            #to_be_pruned.append(item)

    progress_mgr.end()
    
    for item in to_be_pruned:
        items.remove(item)
    return items

#Unused function
#Just here so that if needed in future
#Handy function to generate subsets
def get_subsets(arr):
    return chain(*[combinations(arr, i+1) for i in range(len(arr))])

def run(dataset, classes, items, confidence_threshold, support_threshold):
    global global_rules
    global global_items

    items_length = len(items)
    progress_mgr.begin()
    
    for index, item in enumerate(items):
        
        #item_namedtuple = Item(item, get_support(dataset, item))
        #global_items.append(item_namedtuple)
        
        progress_percent = ((index + 1)/ items_length) * 100
        progress_mgr.publish(progress_percent)
            
        if len(item) > 0:
            for label in set(classes):
                count = get_classwise_count(dataset, classes, item)[label]
                support = round(count[0]/len(dataset), 3)
                try:
                    confidence = round(count[0]/get_count(dataset, item), 3)
                    confidence_expected = count[1]/len(dataset)
                    lift = round(confidence/confidence_expected, 3)
                    conviction = round((1 - (confidence/lift))/(1-confidence), 3)
                except (ZeroDivisionError):
                    confidence = 0
                    lift = 1
                    conviction = 1
                if confidence >= confidence_threshold and support >= support_threshold and lift > 1:
                    rule = Rule(tuple(item), label, confidence, lift, conviction, support)
                    global_rules.append(rule)
                    #global_rules.append((tuple(item), label, confidence, lift, conviction, support))
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
def get_default_class(dataset, classes, rule_filter = None):
    global global_rules
    c = dict.fromkeys(set(classes), 0)
    for i,data in enumerate(dataset):
        is_match = False
        for rule in global_rules:
            if (rule_filter is not None) and (rule_filter(rule) is False):
                continue
            if match_rule_data(data, rule, classes[i]):
                is_match = True
                break
        if is_match is False:
            c[classes[i]] += 1
    return max(c.items(), key=itemgetter(1))[0]
    
def prune_rules(dataset, classes, coverage_threshold):
    global global_rules
    pruned_rules = []
    data_count = [0]*len(dataset)

    progress_mgr.begin()
    global_rules_length = len(global_rules)
    dataset_length = len(dataset)
    
    for rule_index, rule in enumerate(global_rules):
        rule_add = False
        for i,data in enumerate(dataset):

            progress_percent = ((rule_index + 1) * (i + 1)) / (global_rules_length * dataset_length) * 100
            progress_mgr.publish(progress_percent)
            
            if match_rule_data(data, rule, classes[i]) and data_count[i]>=0:
                rule_add = True
                data_count[i] += 1
                if data_count[i] >= coverage_threshold:
                    data_count[i] = -1
        if rule_add:
            pruned_rules.append(rule)

    progress_mgr.end()
    
    return pruned_rules
                
def get_score(rule):
    return rule.confidence

#rule_filter is a arbitrary function used to filter out unwanted rules
def classify(default_class, input_data, top_k_rules, rule_filter):
    matching_rules = []
    for rule in global_rules:
        if (rule_filter is not None) and (rule_filter(rule) is False):
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

def get_dataset_and_classes(file_name_itemset, file_name_classes):
    try:
        #Get dataset from file
        dataset = get_dataset_from_file('Itemset_train.txt')

        #Get training classes from file
        classes = get_classes_from_file('Classes_train.txt')
        return dataset, classes
    except(FileNotFoundError):
        return
        print("\nUnable to open Training Dataset")
        sys.exit(0)
        
def learn(support_threshold, confidence_threshold, coverage_threshold):
    global global_rules
    global global_items
    
    global_rules = []
    global_items = []
    try:
        #Get dataset from file
        dataset = get_dataset_from_file('Itemset_train.txt')

        #Get training classes from file
        classes = get_classes_from_file('Classes_train.txt')
    except(FileNotFoundError):
        print("\nUnable to open Training Dataset")
        sys.exit(0)

    #Get items present in dataset
    print("Finding candidate Itemsets of size 1")
    items = get_initial_items(dataset)
    print("Found {} candidate Itemsets".format(len(items)))
    
    #Calculate confidence, lift and support for items
    itemset_size = 1
    while len(items) > 0:
        print("Finding frequent Itemsets from candidates")
        items = prune_items(dataset, items, support_threshold)
        print("Found {} frequent Itemsets".format(len(items)))
        print("Generating rules from those Itemsets")
        itemset_size += 1
        run(dataset, classes, items, confidence_threshold, support_threshold)
        print("\nFinding candidate Itemsets of size {}".format(itemset_size))
        items = generate_new_items(items)
        print("Found {} candidate Itemsets".format(len(items)))

    print("\nRule Generation complete")
    print("Total {} rules generated".format(len(global_rules)))

    global_rules = sorted(global_rules, key=lambda rule: get_score(rule), reverse=True)
    print("\nPruning rules based on coverage_threshold")
    global_rules = prune_rules(dataset, classes, coverage_threshold)
    print("{} rules left after pruning".format(len(global_rules)))
    return get_default_class(dataset, classes)

#rule_filter is a arbitrary function used to filter out unwanted rules
def test(default_class, top_k_rules, rule_filter = None, **kwargs):
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
        print("-"*165)
        print("{!s:130} \t| {:^10} \t| {:^10}|".format("Itemset", "Expected", "Output"))
        print("-"*165)
    for i,test_data in enumerate(test_dataset):
        c = classify(default_class, test_data, top_k_rules, rule_filter)
        if(c == test_classes[i]):
            correct_output_counter += 1
        else:
            incorrect_output_counter += 1
            if kwargs.get('verbose', False) is True:
                print("{!s:130} \t| {:^10} \t| {:^10}|".format(", ".join(test_data), test_classes[i], c))
    if kwargs.get('verbose', False) is True:
        print("-"*165)
        print("\nClassified {} Inputs".format(len(test_dataset)))
        print("Correctly Classified {} Inputs".format(correct_output_counter))
    return round((correct_output_counter/(incorrect_output_counter + correct_output_counter))*100, 3)

def display_items():
    global global_items
    print("-"*165)
    print("{!s:^80} \t| {:^15}|".format("Itemset","Support"))
    print("-"*165)
    for item in global_items:
        print("{!s:<80} \t| {:^15}|".format(", ".join(item.itemset),item.support))
    print("-"*165)

def display_rules():
    global global_rules
    print("-"*165)
    print("{!s:^80} \t| {:^15} \t| {:^10} \t| {:^10} \t| {:^10}|".format("Antecedent","Consequent","Confidence","Lift","Conviction"))
    print("-"*165)
    for rule in global_rules:
        print("{!s:<80} \t| {:^15} \t| {:^10} \t| {:^10} \t| {:^10}|".format(", ".join(rule.antecedent), rule.consequent, rule.confidence, rule.lift, rule.conviction))
    print("-"*165)


def main():
    global global_rules

    support_threshold = 0.2
    confidence_threshold = 0.2
    coverage_threshold = 10
    top_k_rules = 25
    
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    print("Coverage Threshold is " + str(coverage_threshold))
    print("top_k_rules is " + str(top_k_rules))
    print()

    default_class = learn(support_threshold, confidence_threshold, coverage_threshold)

    print("\n\nFREQUENT ITEMSETS\n")
    
    #Printing itemsets with support greater than support threshold
    display_items()
        
    print("\n\nRULES LEFT AFTER PRUNING\n")

    display_rules()

    print("\n\nOverall Accuracy: {}%".format(test(default_class, top_k_rules, verbose = True)))

if __name__ == '__main__':
    main()
