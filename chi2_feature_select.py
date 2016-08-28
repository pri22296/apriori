import apriori

chi2 = [3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919,
        18.307, 19.675, 21.026, 22.362, 23.685, 24.996, 26.296, 27.587, 28.869,
        30.144, 31.410, 32.671, 33.924, 35.172, 36.415, 37.652, 38.885, 40.113,
        41.337, 42.557, 43.773]

dataset = apriori.get_dataset_from_file('Itemset_train.txt')
classes = apriori.get_classes_from_file('Classes_train.txt')

feature_options_list = list(map(set, zip(*dataset)))
classes_list = list(set(classes))

def weird_sum(l,index):
    s = 0
    for i in l:
        s += i[index]
    return s

for feature_options in feature_options_list:
    degree = (len(feature_options) - 1) * (len(classes_list) - 1)
    print(feature_options)
    expect = []
    chi = 0
    for feature_option in feature_options:
        t = apriori.new_get_count(dataset, classes, [feature_option])
        l = list(t.values())
        ws0 = weird_sum(l,0)
        ws1 = weird_sum(l,1)
        for k in l:
            expected = k[1]*ws0/ws1
            observed = k[0]
            chi += (observed-expected)**2/expected
        print(l)
    chi_critical = chi2[degree-1]
    print(round(chi, 3), chi_critical)
    if(chi > chi_critical):
        print("Important\n")
    else:
        print("Not Important\n")
        
