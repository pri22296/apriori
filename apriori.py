from itertools import chain, combinations
from operator import itemgetter
import sys

global_items = []
global_rules = []

def get_dataset_from_file(filename):
    file = open(filename, 'r')
    dataset = []
    for line in file:
        dataset.append(line.strip().rstrip('\n').split(','))
    return dataset

def get_classes_from_file(filename):
    file = open(filename, 'r')
    classes = []
    for line in file:
        classes.append(line.strip().rstrip('\n'))
    return classes

def get_initial_items(dataset):
    l = []
    for item in set(chain(*dataset)):
        l.append([item])
    return sorted(l)

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

def get_class_count(classes, label):
    count = 0
    for c in classes:
        if c == label:
            count += 1
    return count

def is_join_candidate(l1, l2):
    l = len(l1)
    for i in range(l-1):
        if l1[i] != l2[i]:
            return False
    if l1[l-1] == l2[l-1]:
        return False
    return True

def generate_new_items(items):
    new_items = []
    for i in range(len(items)):
        for j in range(i,len(items)):
            if is_join_candidate(items[i], items[j]):
                new_items.append(sorted(list(set(items[i]).union(set(items[j])))))
    return new_items

def prune_items(dataset, items, support_threshold):
    to_be_pruned = []
    for item in items:
        if get_count(dataset, item) < len(dataset)*support_threshold:
            to_be_pruned.append(item)
    for item in to_be_pruned:
        items.remove(item)
    return items

def get_subsets(arr):
    return chain(*[combinations(arr, i+1) for i in range(len(arr)-1)])

def run(dataset,classes, items, confidence_threshold):
    global global_rules
    for item in items:
        global_items.append((item, get_support(dataset, item)))
        if len(item) > 1:
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

def match_rule_data(data, rule):
    if set(rule[0]).issubset(set(data)):
        return True
    else:
        return False

def new_match_rule_data(data, rule, label):
    if set(rule[0]).issubset(set(data)) and rule[1] == label:
        return True
    else:
        return False
    
def get_default_class(dataset, classes):
    global global_rules
    c = dict.fromkeys(set(classes), 0)
    for i,data in enumerate(dataset):
        is_match = False
        for rule in global_rules:
            if new_match_rule_data(data, rule, classes[i]):
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
            if new_match_rule_data(data, rule, classes[i]) and data_count[i]>=0:
                rule_add = True
                data_count[i] += 1
                if data_count[i] >= coverage_threshold:
                    data_count[i] = -1
        if rule_add:
            pruned_rules.append(rule)
    return pruned_rules
                

def classify(dataset, classes, input_data, top_k_rules):
    matching_rules = []
    for rule in global_rules:
        if match_rule_data(input_data,rule):
           matching_rules.append(rule)
        if len(matching_rules) == top_k_rules:
            break
    if len(matching_rules) > 0:
        score = dict()
        for rule in matching_rules:
            score[rule[1]] = score.get(rule[1], 0) + rule[2]
        return max(score.items(), key=itemgetter(1))[0]
    else:
        return get_default_class(dataset, classes)

def learn(support_threshold, confidence_threshold, coverage_threshold):
    global global_rules
    global_rules = []
    try:
        dataset = get_dataset_from_file('Itemset_train.txt')
        classes = get_classes_from_file('Classes_train.txt')
    except(FileNotFoundError):
        print("\nrun DataGen.py first")
        sys.exit(0)

    items = get_initial_items(dataset)
    while len(items) > 0:
        items = prune_items(dataset, items, support_threshold)
        run(dataset, classes, items, confidence_threshold)
        items = generate_new_items(items)

    global_rules = sorted(global_rules, key=itemgetter(2), reverse=True)
    global_rules = prune_rules(dataset, classes, coverage_threshold)
    return (dataset, classes)

def test(dataset, classes, top_k_rules):
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
        c = classify(dataset, classes, test_data, top_k_rules)
        if(c == test_classes[i]):
            correct_output_counter += 1
        else:
            incorrect_output_counter += 1
            pass
            #print("{!s:80} \tExpected: {:<10} \tOutput: {:<10}".format(test_data, test_classes[i], c))
    return round((correct_output_counter/(incorrect_output_counter + correct_output_counter))*100, 3)

def main():
    global global_rules

    support_threshold = 0.0874
    confidence_threshold = 0.3171
    coverage_threshold = 5
    top_k_rules = 20
    
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    print("Coverage Threshold is " + str(coverage_threshold))

    training_data = learn(support_threshold, confidence_threshold, coverage_threshold)
    
    for i in global_items:
        print("item: {!s:30} \tsupport: {:<10}".format(i[0],i[1]))
        
    print("\n\nRules Left After Pruning\n")
    
    for i in global_rules:
        print("rule: {!s:>20} ==> {:<10} \tconfidence = {:<10} \tlift = {:<10} \tconviction = {:<10}".format(i[0], i[1], i[2], i[3], i[4]))

    print("\n\nOverall Accuracy: {}%".format(test(*training_data, top_k_rules)))

if __name__ == '__main__':
    main()
