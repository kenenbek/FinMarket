import numpy as np
from matplotlib import pyplot as plt


def plot_income_outcome_flow(income_flow, outcome_flow):
    width = 1  # the width of the bars
    
    x = np.arange(len(income_flow))
    
    fig, ax = plt.subplots(figsize=(15, 6))
    rects1 = ax.bar(x, income_flow, width, label='Income')
    rects2 = ax.bar(x, -np.array(outcome_flow), width, label='Outcome')
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Money flow')
    ax.set_title('IRR')
    ax.set_xlim([0, len(income_flow)])
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)
    ax.legend()
    
    
    # def autolabel(rects):
    #     """Attach a text label above each bar in *rects*, displaying its height."""
    #     for rect in rects:
    #         height = rect.get_height()
    #         ax.annotate('{}'.format(height),
    #                     xy=(rect.get_x() + rect.get_width() / 2, height),
    #                     xytext=(0, 3),  # 3 points vertical offset
    #                     textcoords="offset points",
    #                     ha='center', va='bottom')
    #
    #
    # autolabel(rects1)
    # autolabel(rects2)
    
    fig.tight_layout()
    
    plt.show()
