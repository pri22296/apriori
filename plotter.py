import matplotlib.pyplot as plt
import apriori

support_threshold_list = [i/100 for i in range(1,40)]
accuracy_list = []

confidence_threshold = 0.2
coverage_threshold = 5
top_k_rules = 20

print("top_k_rules is " + str(top_k_rules))
print("Confidence Threshold is " + str(confidence_threshold))
print("Coverage Threshold is " + str(coverage_threshold))

for sup_th in support_threshold_list:
    accuracy = apriori.test(*apriori.learn(sup_th, confidence_threshold, coverage_threshold), top_k_rules)
    print("accuracy for support_threshold {} is {}".format(sup_th, accuracy))
    accuracy_list.append(accuracy)
    
plt.plot(support_threshold_list, accuracy_list)
plt.ylabel('accuracy')
plt.xlabel('support_threshold')
plt.axis([0, 0.4, 0, 100])
plt.show()
