import apriori

dataset = apriori.get_dataset_from_file('Itemset_train.txt')
classes = apriori.get_classes_from_file('Classes_train.txt')

chi2_dist = [5.024, 7.378, 9.348, 11.143, 12.833, 14.449, 16.013, 17.535, 19.023,
20.483, 21.920, 23.337, 24.736, 26.119, 27.488, 28.845, 30.191,31.526, 32.852, 34.170]

feature_options_list = list(map(set, zip(*dataset)))
classes_list = list(set(classes))

def weird_sum(l,index):
    s = 0
    for i in l:
        s += i[index]
    return s

for feature_options in feature_options_list:
    degree = (len(feature_options) - 1) * (len(classes_list) - 1)
    #print(degree)
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
        #print(l)
    #print(chi)
    chi_diff = abs(chi - chi2_dist[degree-1])
    print("Chi Difference = " + str(chi_diff))
        
