import apriori
from scipy.stats.distributions import chi2

significance_level = 0.005

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
        t = apriori.get_classwise_count(dataset, classes, [feature_option])
        l = list(t.values())
        ws0 = weird_sum(l,0)
        ws1 = weird_sum(l,1)
        for k in l:
            expected = k[1]*ws0/ws1
            observed = k[0]
            chi += (observed-expected)**2/expected
    chi_critical = round(chi2.isf(significance_level, degree), 3)
    print("chi2_stats = {}, chi2_critical_value = {}".format(round(chi, 3), chi_critical))
    if(chi > chi_critical):
        print("Important\n")
    else:
        print("Not Important\n")
        
