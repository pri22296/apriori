import matplotlib.pyplot as plt
import apriori
import time
import math
import ga_optimize
import pso_optimize
import chi2_feature_select
from printer_tools import TablePrinter

def plot(xlabel, ylabel, xarray, yarray, axis):
    plt.plot(xarray, yarray)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.axis(axis)
    plt.show()

def bar(xlabel, ylabel, xarray, yarray, axis):
    plt.bar(xarray, yarray)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.axis(axis)
    plt.show()

def accuracy_vs_support(confidence_threshold, coverage_threshold, top_k_rules):
    print("\nPlotting accuracy vs support_threshold\n")
    print("top_k_rules is {}".format(top_k_rules))
    print("Confidence Threshold is {}".format(confidence_threshold))
    print("Coverage Threshold is {}\n".format(coverage_threshold))

    support_threshold_list = [i/10 for i in range(1,11)]
    accuracy_list = []

    table_printer = TablePrinter(2)
    table_printer.set_column_headers("Support Threshold", "Accuracy")
    table_printer.set_column_widths(30, 30)

    table_printer.begin()
    
    for sup_th in support_threshold_list:
        accuracy = apriori.test(apriori.learn(sup_th, confidence_threshold,
                                              coverage_threshold, verbose = True),
                                sup_th, confidence_threshold, top_k_rules)
        table_printer.append_row(sup_th, accuracy)
        accuracy_list.append(accuracy)

    table_printer.end()

    plot('support_threshold', 'accuracy(%)', support_threshold_list, accuracy_list, [0, 1, 0, 110])

def timetaken_vs_support(confidence_threshold, coverage_threshold, top_k_rules):
    print("\nPlotting time taken to extract rules vs support_threshold\n")
    print("top_k_rules is {}".format(top_k_rules))
    print("Confidence Threshold is {}".format(confidence_threshold))
    print("Coverage Threshold is {}\n".format(coverage_threshold))

    support_threshold_list = [i/10 for i in range(1,11)]
    timetaken_list = []

    table_printer = TablePrinter(2)
    table_printer.set_column_headers("Support Threshold", "Time Taken")
    table_printer.set_column_widths(30, 30)

    table_printer.begin()
    
    for sup_th in support_threshold_list:
        t = time.time()
        apriori.learn(sup_th, confidence_threshold, coverage_threshold, verbose = True)
        time_taken = time.time() - t
        table_printer.append_row(sup_th, round(time_taken*1000, 3))
        timetaken_list.append(time_taken)

    table_printer.end()

    plot('support_threshold', 'learning_time(seconds)', support_threshold_list, timetaken_list, [0, 1, 0, 50])

def accuracy_vs_confidence(support_threshold, coverage_threshold, top_k_rules):
    print("\nPlotting accuracy vs confidence_threshold\n")
    print("top_k_rules is {}".format(top_k_rules))
    print("Support Threshold is {}".format(support_threshold))
    print("Coverage Threshold is {}\n".format(coverage_threshold))

    accuracy_list = []
    confidence_threshold_list = [i/10 for i in range(1,11)]

    table_printer = TablePrinter(2)
    table_printer.set_column_headers("Confidence Threshold", "Accuracy")
    table_printer.set_column_widths(30, 30)

    table_printer.begin()

    for conf_th in confidence_threshold_list:
        accuracy = apriori.test(apriori.learn(support_threshold, conf_th,
                                              coverage_threshold, verbose = True),
                                support_threshold, conf_th, top_k_rules)
        table_printer.append_row(conf_th, accuracy)
        accuracy_list.append(accuracy)

    table_printer.end()

    plot('confidence_threshold', 'accuracy(%)', confidence_threshold_list, accuracy_list, [0, 1, 0, 110])

def accuracy_vs_ga_iteration(coverage_threshold, top_k_rules):
    print("\nPlotting accuracy vs ga_iteration_count\n")
    print("top_k_rules is {}".format(top_k_rules))
    print("Coverage Threshold is {}\n".format(coverage_threshold))

    gen, avg, mini, maxi = ga_optimize.main()

    plt.plot(gen, avg, 'g',label='average')
    plt.plot(gen, mini, 'r',label='minimum')
    plt.plot(gen, maxi, 'b',label='maximum')
    plt.ylabel('accuracy(%)')
    plt.xlabel('generation')
    plt.legend(loc='best')
    plt.axis([0 ,10 ,0 ,110])
    plt.show()

def accuracy_vs_pso_iteration(coverage_threshold, top_k_rules):
    print("\nPlotting accuracy vs pso_iteration_count\n")
    print("top_k_rules is {}".format(top_k_rules))
    print("Coverage Threshold is {}\n".format(coverage_threshold))

    gen, avg, mini, maxi = pso_optimize.main()

    plt.plot(gen, avg, 'g', label='average')
    plt.plot(gen, mini, 'r', label='minimum')
    plt.plot(gen, maxi, 'b', label='maximum')
    plt.ylabel('accuracy(%)')
    plt.xlabel('generation')
    plt.legend(loc='best')
    plt.axis([0 ,10 ,0 ,110])
    plt.show()

def chi2_stats_vs_feature():
    print("\nPlotting chi square statistics vs Features\n")
    
    features, chi2_critical, chi2_stats = chi2_feature_select.main()
    width = 0.8

    chi2_critical = list(map(math.log, chi2_critical))
    chi2_stats = list(map(math.log, chi2_stats))

    x = list(range(1, 3*len(chi2_critical) + 1, 3))
    plt.bar(x, chi2_stats, width, color = 'g', label = 'Log of chi2_stats')
    plt.bar([p + width for p in x], chi2_critical, width, color = 'r', label = 'Log of chi2_critical')
    plt.ylabel('Log of chi-square stats')
    plt.xlabel('features')
    plt.tight_layout()

    plt.xticks([p + width for p in x], features)
    plt.legend(loc='best')
    plt.axis([0 ,50 ,0 ,10])
    plt.show()

def timetaken_vs_size_of_dataset(support_threshold, confidence_threshold,coverage_threshold):
    print("\nPlotting time_taken vs size_of_dataset\n")
    print("Support Threshold is {}".format(support_threshold))
    print("Confidence Threshold is {}".format(confidence_threshold))
    print("Coverage Threshold is {}\n".format(coverage_threshold))
    print("Testing done on 25% of the dataset")

    dataset_percent_list = [i for i in range(10,110,10)]
    timetaken_list = []

    for dataset_percent in dataset_percent_list:
        dataset_size = (dataset_percent*10000)//100
        t = time.time()
        apriori.learn(support_threshold, confidence_threshold, coverage_threshold, verbose = True)
        time_taken = time.time() - t
        print("time taken for {}% dataset is {}ms".format(dataset_percent, round(time_taken*1000, 3)))
        timetaken_list.append(time_taken)
        
    plot('dataset_percent', 'learning_time(seconds)', dataset_percent_list, timetaken_list, [0, 110, 0, 5])

def main():
    support_threshold = 0.2
    confidence_threshold = 0.2
    coverage_threshold = 10
    top_k_rules = 50

    while True:
        print("\nWhat would you like to do?")
        print("1. Accuracy vs Support Threshold")
        print("2. Time Taken to extract rules vs Support Threshold")
        print("3. Accuracy vs Confidence Threshold")
        print("4. Accuracy vs GA Iteration count")
        print("5. Accuracy vs PSO Iteration count")
        print("6. Chi-Square Statistics vs Features")
        print("7. Quit")
        print("\nEnter your choice: ", end = '')
        try:
            ch = int(input())
        except ValueError:
            print("Invalid Choice")
            continue
        if ch == 1:
            accuracy_vs_support(confidence_threshold, coverage_threshold, top_k_rules)
        elif ch == 2:
            timetaken_vs_support(confidence_threshold, coverage_threshold, top_k_rules)
        elif ch == 3:
            accuracy_vs_confidence(support_threshold, coverage_threshold, top_k_rules)
        elif ch == 4:
            accuracy_vs_ga_iteration(coverage_threshold, top_k_rules)
        elif ch == 5:
            accuracy_vs_pso_iteration(coverage_threshold, top_k_rules)
        elif ch == 6:
            chi2_stats_vs_feature()
        elif ch == 7:
            break
        else:
            print("Invalid Choice")
    

if __name__ == "__main__":
    main()
