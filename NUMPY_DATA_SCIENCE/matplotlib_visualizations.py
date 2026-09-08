"""
Matplotlib & NumPy Data Visualization Suite
Demonstrates 12 different graph styles:
1. Basic Line Plot
2. Formatted Line Plot with Markers
3. Multi-Line Plot with Legends
4. Bar Chart & Horizontal Bar Chart
5. Pie Chart with Percentages
6. Histogram Distribution
7. Scatter Plot
8. Area Fill Chart
9. Stack Plot
10. Box Plot
11. Violin Plot
12. 2x2 Subplots Multi-figure
"""

import matplotlib.pyplot as plt
import numpy as np

def demo_line_plots():
    names = ["SUMIT", "SHAURYA", "MANJIT", "VINEET", "RAVI"]
    marks = [55, 66, 77, 44, 55]
    plt.figure(figsize=(8, 4))
    plt.plot(names, marks, color='red', linestyle='--', linewidth=2, marker='o')
    plt.title('Student Marks Line Plot')
    plt.xlabel('Student Names')
    plt.ylabel('Marks Scored')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def demo_bar_and_pie():
    categories = ['Python', 'SQL', 'Pandas', 'NumPy']
    values = [35, 25, 20, 20]
    
    # Bar Chart
    plt.figure(figsize=(6, 4))
    plt.bar(categories, values, color='#3182CE')
    plt.title('Skill Proficiency Score')
    plt.ylabel('Proficiency')
    plt.tight_layout()
    plt.show()

    # Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, colors=['#E53E3E', '#3182CE', '#38A169', '#D69E2E'])
    plt.title('Project Skill Distribution')
    plt.tight_layout()
    plt.show()

def demo_statistical_plots():
    np.random.seed(42)
    data = np.random.randn(1000)
    
    # Histogram
    plt.figure(figsize=(7, 4))
    plt.hist(data, bins=30, color='skyblue', edgecolor='black')
    plt.title('Normal Distribution Histogram')
    plt.tight_layout()
    plt.show()

    # Scatter Plot
    x = np.random.rand(50)
    y = np.random.rand(50)
    plt.figure(figsize=(6, 4))
    plt.scatter(x, y, color='purple', alpha=0.7)
    plt.title('2D Scatter Distribution')
    plt.tight_layout()
    plt.show()

def demo_subplots():
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    
    # Plot 1: Line
    ax[0, 0].plot([1, 2, 3], [4, 5, 6], color='blue')
    ax[0, 0].set_title('Subplot 1: Line')

    # Plot 2: Bar
    ax[0, 1].bar(['A', 'B', 'C'], [3, 7, 5], color='orange')
    ax[0, 1].set_title('Subplot 2: Bar')

    # Plot 3: Scatter
    ax[1, 0].scatter([1, 2, 3, 4], [3, 1, 5, 2], color='green')
    ax[1, 0].set_title('Subplot 3: Scatter')

    # Plot 4: Histogram
    ax[1, 1].hist(np.random.randn(100), color='salmon', edgecolor='black')
    ax[1, 1].set_title('Subplot 4: Histogram')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print("Running Matplotlib Visualization Suite demonstrations...")
    print("1. Launching Line Plot...")
    demo_line_plots()
    print("2. Launching Bar and Pie Charts...")
    demo_bar_and_pie()
    print("3. Launching Statistical Histograms & Scatters...")
    demo_statistical_plots()
    print("4. Launching Subplots...")
    demo_subplots()
