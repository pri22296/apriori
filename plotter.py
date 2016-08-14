import matplotlib.pyplot as plt
plt.plot([0.03, 0.4, 0.7, 0.9], [50,60,80,20])
plt.ylabel('accuracy')
plt.xlabel('support_threshold')
plt.axis([0, 1, 0, 100])
plt.show()
