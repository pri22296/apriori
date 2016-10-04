from itertools import chain, combinations
from operator import itemgetter
import sys
import math

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

#Checks if an itemset contains two possible options of the same column
#In case of tabular data count of such a itemset will be guaranteed to be 0
#Returns True for validity, False for invalidity
def check_validity_of_itemset_for_tabular_data(items):
    attr_list = []
    for item in items:
        attr_list.append(item.split('-')[0])
    if len(attr_list) == len(set(attr_list)):
        return True
    else:
        return False

#Returns the count of items in the dataset irrespective of the class
def get_count(dataset, items):
    count = 0
    if check_validity_of_itemset_for_tabular_data(items) is False:
        return count
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
    if check_validity_of_itemset_for_tabular_data(items) is False:
        return count_class
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

#Unused function
#Just here so that if needed in future
#Handy function to generate subsets
def get_subsets(arr):
    return chain(*[combinations(arr, i+1) for i in range(len(arr))])

def run(dataset, classes, items, confidence_threshold, support_threshold):
    global global_rules
    global global_items
    
    for item in items:
        global_items.append((item, get_support(dataset, item)))
        if len(item) > 0:
            for label in set(classes):
                count = get_classwise_count(dataset, classes, item)[label]
                support = round(count[0]/len(dataset), 3)
                try:
                    confidence = round(count[0]/get_count(dataset, item), 3)
                except (ZeroDivisionError):
                    confidence = 0
                confidence_expected = count[1]/len(dataset)
                lift = round(confidence/confidence_expected, 3)
                try:
                    conviction = round((1 - (confidence/lift))/(1-confidence), 3)
                except(ZeroDivisionError):
                    conviction = 1
                if confidence >= confidence_threshold and support >= support_threshold and lift > 1:
                    global_rules.append((tuple(item), label, confidence, lift, conviction))
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
                
def get_score(rule):
    return rule[2]

def get_cohesion(data, rule):
    if match_rule_data(data, rule, None) is False:
        return 0
    else:
        return 10/(1 + math.e**(-len(set(data).difference(set(rule[0])))))

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
            score[rule[1]] = score.get(rule[1], 0) + get_score(rule)*get_cohesion(input_data, rule)
        return max(score.items(), key=itemgetter(1))[0]
    else:
        return default_class

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
    
    #Calculate confidence, lift and support for items
    while len(items) > 0:
        items = prune_items(dataset, items, support_threshold)
        run(dataset, classes, items, confidence_threshold, support_threshold)
        items = generate_new_items(items)

    global_rules = sorted(global_rules, key=lambda rule: get_score(rule), reverse=True)
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
    global_rules = sorted(global_rules, key=lambda rule: get_score(rule), reverse=True)
    #print("\nIncorrectly Labelled Itemsets\n")
    for i,test_data in enumerate(test_dataset):
        c = classify(default_class, test_data, top_k_rules)
        if(c == test_classes[i]):
            correct_output_counter += 1
        else:
            incorrect_output_counter += 1
            pass
            #print("{!s:80} \tExpected: {:<10} \tOutput: {:<10}".format(test_data, test_classes[i], c))
    #print("\nClassified {} Inputs".format(len(test_dataset)))
    #print("Correctly Classified {} Inputs".format(correct_output_counter))
    return round((correct_output_counter/(incorrect_output_counter + correct_output_counter))*100, 3)

def display_items():
    global global_items
    print("{!s:^80} \t {:^15}\n".format("item","support"))
    for i in global_items:
        print("{!s:<80} \t {:^15}".format(i[0],i[1]))

def display_rules():
    global global_rules
    print("{!s:^80} \t {:^15} \t {:^10} \t {:^10} \t {:^10}\n".format("antecedent","consequent","confidence","lift","conviction"))
    for i in global_rules:
        print("{!s:<80} \t {:^15} \t {:^10} \t {:^10} \t {:^10}".format(i[0], i[1], i[2], i[3], i[4]))


def main():
    global global_rules

    support_threshold = 0.02
    confidence_threshold = 0.2
    coverage_threshold = 5
    top_k_rules = 10
    
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    print("Coverage Threshold is " + str(coverage_threshold))
    print("top_k_rules is " + str(top_k_rules))

    default_rule = learn(support_threshold, confidence_threshold, coverage_threshold)

    #Printing itemsets with support greater than support threshold
    display_items()
        
    print("\n\nRules Left After Pruning\n")

    display_rules()

    print("\n\nOverall Accuracy: {}%".format(test(default_rule, top_k_rules)))

if __name__ == '__main__':
    main()
