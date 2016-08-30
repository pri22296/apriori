from itertools import chain, combinations
from operator import itemgetter
import sys

global_items = []
global_rules = []

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
    for item in set(chain(*dataset)):
        l.append([item])
    return sorted(l)

#Returns the count of items in the dataset irrespective of the class
def get_count(dataset, items):
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
def new_get_count(dataset, classes, items):
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
    for global_item in global_items:
        if(len(global_item[0]) == len(items)):
            if(len(set(items).intersection(set(global_item[0]))) == len(global_item[0])):
                return global_item[1]
    return round(get_count(dataset, items)/len(dataset), 3)

def new_get_support(dataset, classes, items, label):
    if label is not None:
        cnt = new_get_count(dataset, classes, items)[label]
        return cnt[0]/cnt[1]
    else:
        c1,c2 = 0,0
        for it in new_get_count(dataset, classes, items).values():
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
    if l1[l-1] == l2[l-1]:
        return False
    return True

#generates k+1 sized itemsets from k sized itemsets
def generate_new_items(items):
    new_items = []
    for i in range(len(items)):
        for j in range(i,len(items)):
            if should_join_candidate(items[i], items[j]):
                new_items.append(sorted(list(set(items[i]).union(set(items[j])))))
    return new_items

#To remove itemsets having support less than support Threshold
def prune_items(dataset, items, support_threshold):
    to_be_pruned = []
    for item in items:
        if get_count(dataset, item) < len(dataset)*support_threshold:
            to_be_pruned.append(item)
    for item in to_be_pruned:
        items.remove(item)
    return items

def get_subsets(arr):
    return chain(*[combinations(arr, i+1) for i in range(len(arr))])

def run(dataset, classes, items, confidence_threshold):
    global global_rules
    global global_items
    
    for item in items:
        global_items.append((item, get_support(dataset, item)))
        if len(item) > 0:
            item_set = set(item)
            for subset in get_subsets(item):
                for label in set(classes):
                    confidence = round(new_get_count(dataset, classes, subset)[label][0]/get_count(dataset, subset), 3)
                    lift = round(confidence*len(dataset)/ get_class_count(classes, label), 3)
                    try:
                        conviction = round((1 - (confidence/lift))/(1-confidence), 3)
                    except(ZeroDivisionError):
                        conviction = 1
                    if confidence >= confidence_threshold:
                        global_rules.append((tuple(subset), label, confidence, lift, conviction))
    global_rules = list(set(global_rules))

#Returns True if data is a superset of antecedent of rule,
#and label is the consequent of rule
#if label is None, then only data is checked
def match_rule_data(data, rule, label):
    if set(rule[0]).issubset(set(data)) and (label == rule[1] or label is None):
        return True
    else:
        return False

#calculates the default class
#Dataset for which no rule matches will be classified using the default rule
def get_default_class(dataset, classes):
    global global_rules
    c = dict.fromkeys(set(classes), 0)
    for i,data in enumerate(dataset):
        is_match = False
        for rule in global_rules:
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
    for rule in global_rules:
        rule_add = False
        for i,data in enumerate(dataset):
            if match_rule_data(data, rule, classes[i]) and data_count[i]>=0:
                rule_add = True
                data_count[i] += 1
                if data_count[i] >= coverage_threshold:
                    data_count[i] = -1
        if rule_add:
            pruned_rules.append(rule)
    return pruned_rules
                

def classify(default_class, input_data, top_k_rules):
    matching_rules = []
    for rule in global_rules:
        if match_rule_data(input_data, rule, None):
           matching_rules.append(rule)
        if len(matching_rules) == top_k_rules:
            break
    if len(matching_rules) > 0:
        score = dict()
        for rule in matching_rules:
            score[rule[1]] = score.get(rule[1], 0) + rule[2]
        return max(score.items(), key=itemgetter(1))[0]
    else:
        return default_class

#It is assumed that the learning data has more than 1 columns
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
        print("\nrun DataGen.py first")
        sys.exit(0)

    #Get items present in dataset
    items = get_initial_items(dataset)

    #Calculate confidence, lift and suport for items
    while len(items) > 0:
        items = prune_items(dataset, items, support_threshold)
        run(dataset, classes, items, confidence_threshold)
        items = generate_new_items(items)

    global_rules = sorted(global_rules, key=itemgetter(2), reverse=True)
    global_rules = prune_rules(dataset, classes, coverage_threshold)
    return get_default_class(dataset, classes)

def test(default_class, top_k_rules):
    global global_rules
    try:
        test_dataset = get_dataset_from_file('Itemset_test.txt')
        test_classes = get_classes_from_file('Classes_test.txt')
    except(FileNotFoundError):
        print("\nrun DataGen.py first")
        sys.exit(0)
        
    correct_output_counter, incorrect_output_counter = 0, 0
    global_rules = sorted(global_rules, key=itemgetter(2), reverse=True)
    #print("\nIncorrectly Labelled Itemsets\n")
    for i,test_data in enumerate(test_dataset):
        c = classify(default_class, test_data, top_k_rules)
        if(c == test_classes[i]):
            correct_output_counter += 1
        else:
            incorrect_output_counter += 1
            pass
            #print("{!s:80} \tExpected: {:<10} \tOutput: {:<10}".format(test_data, test_classes[i], c))
    return round((correct_output_counter/(incorrect_output_counter + correct_output_counter))*100, 3)

def display_items():
    for i in global_items:
        print("item: {!s:30} \tsupport: {:<10}".format(i[0],i[1]))

def display_rules():
    for i in global_rules:
        print("rule: {!s:>20} ==> {:<10} \tconfidence = {:<10} \tlift = {:<10} \tconviction = {:<10}".format(i[0], i[1], i[2], i[3], i[4]))


def main():
    global global_rules

    support_threshold = 0.07
    confidence_threshold = 0.3
    coverage_threshold = 5
    top_k_rules = 20
    
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    print("Coverage Threshold is " + str(coverage_threshold))

    default_rule = learn(support_threshold, confidence_threshold, coverage_threshold)

    #Printing itemsets with support
    for i in global_items:
        print("item: {!s:30} \tsupport: {:<10}".format(i[0],i[1]))
        
    print("\n\nRules Left After Pruning\n")
    
    for i in global_rules:
        print("rule: {!s:>20} ==> {:<10} \tconfidence = {:<10} \tlift = {:<10} \tconviction = {:<10}".format(i[0], i[1], i[2], i[3], i[4]))

    print("\n\nOverall Accuracy: {}%".format(test(default_rule, top_k_rules)))

if __name__ == '__main__':
    main()
