import matplotlib.pyplot as plt
import apriori
import time
import ga_optimize
import pso_optimize

def plot(xlabel, ylabel, xarray, yarray, axis):
    plt.plot(xarray, yarray)
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
    
    for sup_th in support_threshold_list:
        accuracy = apriori.test(apriori.learn(sup_th, confidence_threshold,
                                              coverage_threshold, verbose = True),
                                sup_th, confidence_threshold, top_k_rules)
        print("accuracy for support_threshold {} is {}".format(sup_th, accuracy))
        accuracy_list.append(accuracy)

    plot('support_threshold', 'accuracy(%)', support_threshold_list, accuracy_list, [0, 1, 0, 110])

def timetaken_vs_support(confidence_threshold, coverage_threshold, top_k_rules):
    print("\nPlotting time taken to extract rules vs support_threshold\n")
    print("top_k_rules is {}".format(top_k_rules))
    print("Confidence Threshold is {}".format(confidence_threshold))
    print("Coverage Threshold is {}\n".format(coverage_threshold))

    support_threshold_list = [i/10 for i in range(1,11)]
    timetaken_list = []
    
    for sup_th in support_threshold_list:
        t = time.time()
        apriori.learn(sup_th, confidence_threshold, coverage_threshold, verbose = True)
        time_taken = time.time() - t
        print("time taken for support_threshold {} is {}ms".format(sup_th, round(time_taken*1000, 3)))
        timetaken_list.append(time_taken)

    plot('support_threshold', 'learning_time(seconds)', support_threshold_list, timetaken_list, [0, 1, 0, 50])

def accuracy_vs_confidence(support_threshold, coverage_threshold, top_k_rules):
    print("\nPlotting accuracy vs confidence_threshold\n")
    print("top_k_rules is {}".format(top_k_rules))
    print("Support Threshold is {}".format(support_threshold))
    print("Coverage Threshold is {}\n".format(coverage_threshold))

    accuracy_list = []
    confidence_threshold_list = [i/10 for i in range(1,11)]

    for conf_th in confidence_threshold_list:
        accuracy = apriori.test(apriori.learn(support_threshold, conf_th,
                                              coverage_threshold, verbose = True),
                                support_threshold, conf_th, top_k_rules)
        print("accuracy for confidence_threshold {} is {}".format(conf_th, accuracy))
        accuracy_list.append(accuracy)

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

    plt.plot(gen, avg, 'g',label='average')
    plt.plot(gen, mini, 'r',label='minimum')
    plt.plot(gen, maxi, 'b',label='maximum')
    plt.ylabel('accuracy(%)')
    plt.xlabel('generation')
    plt.legend(loc='best')
    plt.axis([0 ,10 ,0 ,110])
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
        print("6. Quit")
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
            break
        else:
            print("Invalid Choice")
    #accuracy_vs_support(confidence_threshold, coverage_threshold, top_k_rules)
    #timetaken_vs_support(confidence_threshold, coverage_threshold, top_k_rules)
    #accuracy_vs_confidence(support_threshold, coverage_threshold, top_k_rules)
    #accuracy_vs_ga_iteration(coverage_threshold, top_k_rules)
    #accuracy_vs_pso_iteration(coverage_threshold, top_k_rules)
    #timetaken_vs_size_of_dataset(support_threshold, confidence_threshold,coverage_threshold)
    

if __name__ == "__main__":
    main()
