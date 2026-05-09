import matplotlib.pyplot as plt
import numpy as np

class GraphManager:
    @staticmethod
    def plot_project_status(projects):
        if not projects:
            print("No projects to plot.")
            return
            
        # Count the occurrences of each project status
        status_counts = {}
        for p in projects:
            status = p.status
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
            
        labels = list(status_counts.keys())
        sizes = list(status_counts.values())
        
        # Generate the pie chart using matplotlib
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Project Status Distribution')
        plt.show()

    @staticmethod
    def plot_financial_breakdown(projects):
        if not projects:
            print("No projects to plot.")
            return

        # Prepare the data
        titles = [p.get_title() for p in projects]
        gross_earnings = [p.calculate_gross_earnings() for p in projects]
        expenses = [p.expenses for p in projects]
        net_incomes = [p.calculate_net_income() for p in projects]

        # Set up the bar locations on the X-axis
        x = np.arange(len(titles))  # [0, 1, 2, ...] based on number of projects
        width = 0.25  # The width of each individual bar

        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plotting the three groups of bars. We shift the X coordinates slightly 
        # so they sit side-by-side instead of overlapping.
        ax.bar(x - width, gross_earnings, width, label='Gross Earnings', color='skyblue')
        ax.bar(x, expenses, width, label='Expenses', color='salmon')
        ax.bar(x + width, net_incomes, width, label='Net Income', color='lightgreen')

        # Add labels, title, and adjust X-axis ticks to show project names
        ax.set_ylabel('Amount ($)')
        ax.set_title('Project Financial Breakdown')
        ax.set_xticks(x)
        # Rotate long project titles by 45 degrees so they don't overlap
        ax.set_xticklabels(titles, rotation=45, ha="right")  
        ax.legend()

        # tight_layout prevents the rotated labels from bg cut off at the bottom of the window
        fig.tight_layout()
        plt.show()
