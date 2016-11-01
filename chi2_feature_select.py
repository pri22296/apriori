import apriori
from printer_tools import TablePrinter
from scipy.stats.distributions import chi2

significance_level = 0.05

dataset = apriori.get_dataset_from_file('Itemset_train.txt')
classes = apriori.get_classes_from_file('Classes_train.txt')
assert len(dataset) == len(classes)

feature_options_list = list(map(set, zip(*dataset)))
classes_list = list(set(classes))

def main():
    print("Chi Square Feature Selection at {}% Confidence Interval\n".format((1-significance_level)*100))
    table_printer = TablePrinter(4, 1)
    table_printer.set_column_headers("Feature", "Chi2_stats", "Chi2_critical_value", "Importance")
    table_printer.set_column_alignments('^', '^', '^', '^')
    table_printer.set_column_widths(20, 20, 20, 20)
    table_printer.begin()

    for i, feature_options in enumerate(feature_options_list):
        degree = (len(feature_options) - 1) * (len(classes_list) - 1)
        #print(feature_options)
        chi = 0
        for feature_option in feature_options:
            classwise_count = apriori.get_classwise_count(dataset, classes, [feature_option])
            classwise_count_list = list(classwise_count.values())
            
            feature_option_count = apriori.get_itemcount_from_classwise_count(classwise_count)

            #item_count is the count of 'item' in the specific class
            #class_count is the count of the specific class
            for item_count, class_count in classwise_count_list:
                expected = class_count * feature_option_count / len(dataset)
                observed = item_count
                chi += (observed - expected)**2 / expected
                
        chi_critical = round(chi2.isf(significance_level, degree), 3)
        importance = "Important" if chi > chi_critical else "Not Important"
        table_printer.append_row("Feature {}".format(i+1), round(chi, 3), chi_critical, importance)

    table_printer.end()

if __name__ == "__main__":
    main()
        
