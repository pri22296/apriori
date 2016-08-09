from itertools import chain, combinations

support_threshold = 0.25
confidence_threshold = 0.1

global_items = []
global_rules = []

def get_dataset_from_file(filename):
    file = open(filename, 'r')
    dataset = []
    for line in file:
        dataset.append(line.strip().rstrip('\n').split(','))
    return dataset

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

def prune_items(dataset, items):
    to_be_pruned = []
    for item in items:
        if get_count(dataset, item) < len(dataset)*support_threshold:
            to_be_pruned.append(item)
    for item in to_be_pruned:
        items.remove(item)
    return items

def get_subsets(arr):
    return chain(*[combinations(arr, i+1) for i in range(len(arr)-1)])

def display(dataset, items):
    print()
    for item in items:
        if len(item) > 1:
            item_set = set(item)
            for subset in get_subsets(item):
                confidence = round(get_count(dataset, item)/get_count(dataset, subset), 3)
                if confidence >= confidence_threshold:
                    global_rules.append("rule: " + str(sorted(subset)) + " ==> " + str(sorted(list(item_set.difference(subset)))) + " , " + str(confidence))
        global_items.append("item: " + str(item) + " , " + str(round(get_count(dataset, item)/len(dataset), 3)))

def main():
    dataset = get_dataset_from_file('dataset_custom.txt')
    print("Support Threshold is " + str(support_threshold))
    print("Confidence Threshold is " + str(confidence_threshold))
    items = get_initial_items(dataset)
    while len(items) > 0:
        items = prune_items(dataset, items)
        display(dataset, items)
        items = generate_new_items(items)
    for i in global_items:
        print(i)
    print()
    for i in global_rules:
        print(i)

if __name__ == '__main__':
    main()
