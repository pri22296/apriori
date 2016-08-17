import matplotlib.pyplot as plt
import apriori
import time

support_threshold_list = [i/100 for i in range(1,40)]
confidence_threshold_list = [i/20 for i in range(1,20)]
accuracy_list = []

confidence_threshold = 0.2
coverage_threshold = 5
top_k_rules = 20
support_threshold = 0.07

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

accuracy_list = []

for sup_th in support_threshold_list:
    t = time.time()
    apriori.learn(sup_th, confidence_threshold, coverage_threshold)
    time_taken = time.time() - t
    print("time taken for support_threshold {} is {}ms".format(sup_th, round(time_taken*1000, 3)))
    accuracy_list.append(time_taken)
    
plt.plot(support_threshold_list, accuracy_list)
plt.ylabel('time taken to learn(seconds)')
plt.xlabel('support_threshold')
plt.axis([0, 0.4, 0, 20])
plt.show()

print("top_k_rules is " + str(top_k_rules))
print("Support Threshold is " + str(support_threshold))
print("Coverage Threshold is " + str(coverage_threshold))

accuracy_list = []

for conf_th in confidence_threshold_list:
    accuracy = apriori.test(*apriori.learn(support_threshold, conf_th, coverage_threshold), top_k_rules)
    print("accuracy for confidence_threshold {} is {}".format(conf_th, accuracy))
    accuracy_list.append(accuracy)

plt.plot(confidence_threshold_list, accuracy_list)
plt.ylabel('accuracy')
plt.xlabel('confidence_threshold')
plt.axis([0, 1, 0, 100])
plt.show()
