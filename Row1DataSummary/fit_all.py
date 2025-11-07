# Data Analysis and Visualization Script for All Trials
# Importing all necessary packages for data analysis and visualization
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from scipy import stats
from sklearn import preprocessing
import openpyxl
import xlsxwriter
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import requests   
import os

# Set matplotlib style for better plots
plt.style.use('default')
sns.set_palette("husl")

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define trial files
trial_files = ['Trial1.xlsx', 'Trial2.xlsx', 'Trial3.xlsx', 'Trial4.xlsx']
trial_data = {}

# Load all trial data
print("Loading all trial data...")
for i, filename in enumerate(trial_files):
    trial_num = i + 1
    try:
        # First try to find the file in the script directory
        file_path = os.path.join(script_dir, filename)
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            trial_data[trial_num] = df
            print(f"Trial {trial_num} loaded successfully! Shape: {df.shape}")
        # If not found in script directory, try current working directory
        elif os.path.exists(filename):
            df = pd.read_excel(filename)
            trial_data[trial_num] = df
            print(f"Trial {trial_num} loaded successfully! Shape: {df.shape}")
        else:
            print(f"Warning: {filename} not found, skipping...")
    except Exception as e:
        print(f"Error loading {filename}: {e}")

# Check if we have any data to plot
if not trial_data:
    print("No trial data found! Please ensure Trial1.xlsx, Trial2.xlsx, Trial3.xlsx, and Trial4.xlsx exist.")
    exit()

# Create subplots - 2x2 grid for 4 trials
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
axes = axes.flatten()  # Flatten for easier indexing

# Define colors for each cell (same across all trials for consistency)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
torque_columns = ['Cell_1_Torque', 'Cell_2_Torque', 'Cell_3_Torque', 
                 'Cell_4_Torque', 'Cell_5_Torque', 'Cell_6_Torque']

# Process each trial
all_equations = {}  # Store all equations for summary table

for trial_num, df in trial_data.items():
    ax = axes[trial_num - 1]  # Get the appropriate subplot
    
    print(f"\n=== Processing Trial {trial_num} ===")
    
    # Track if any data is plotted and store data for fitting
    has_data = False
    cell_data = {}  # Store data for linear fitting
    trial_equations = {}  # Store equations for this trial
    
    for i, column in enumerate(torque_columns):
        # Filter for non-null values AND torque between 42 and 57
        mask = (df[column].notna()) & (df[column] >= 42) & (df[column] <= 57)
        
        if mask.any():  # Only plot if there are data points in the range
            # Multiply Z-Height by -1 to make it positive
            z_height_positive = df.loc[mask, 'Z-Height'] * -1
            torque_values = df.loc[mask, column]
            
            # Plot the data points
            ax.plot(z_height_positive, torque_values, 
                   marker='o', markersize=4, linewidth=2, 
                   color=colors[i], label=f'Cell {i+1}', alpha=0.8)
            
            # Store data for linear fitting
            cell_data[i] = {
                'z_height': z_height_positive.values,
                'torque': torque_values.values,
                'column': column
            }
            
            has_data = True
            print(f"  Cell {i+1}: {mask.sum()} data points in range 42-57")
        else:
            print(f"  Cell {i+1}: No data points in range 42-57")
    
    # Add linear fit lines for each cell with data
    if has_data:
        print(f"\n  Linear fit equations for Trial {trial_num}:")
        for i, data in cell_data.items():
            # Perform linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(data['z_height'], data['torque'])
            
            # Generate points for the fitted line
            x_fit = np.linspace(data['z_height'].min(), data['z_height'].max(), 100)
            y_fit = slope * x_fit + intercept
            
            # Plot the fitted line
            ax.plot(x_fit, y_fit, 'k--', alpha=0.7, linewidth=1.5)
            
            # Create equation label
            equation = f'  Cell {i+1}: y = {slope:.3f}x + {intercept:.3f} (R² = {r_value**2:.3f})'
            print(equation)
            
            # Store equation for summary table
            trial_equations[f'Cell {i+1}'] = {
                'equation': f'y = {slope:.3f}x + {intercept:.3f}',
                'r_squared': f'{r_value**2:.3f}',
                'slope': slope,
                'intercept': intercept
            }
            
            # Position equation text at the end (top) of the fitted line
            # Use the maximum Z-Height point for x position
            text_x = data['z_height'].max()
            text_y = slope * text_x + intercept  # Y position at the end of the line
            
            # Add small offset to position label slightly above the line end
            text_y += 0.3
            
            ax.text(text_x, text_y, f'y = {slope:.3f}x + {intercept:.3f}', 
                   fontsize=7, ha='right', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    # Configure subplot
    if has_data:
        ax.set_xlabel('Z-Height/mm (Positive)', fontsize=11)
        ax.set_ylabel('Torque/%', fontsize=11)
        ax.set_title(f'Trial {trial_num}: Z vs T ', fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Set y-axis limits to 42-57
        ax.set_ylim(42, 57)
        
        # Format x-axis to show 3 decimal places
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.3f}'))
        
        # Add some styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    else:
        ax.text(0.5, 0.5, f'Trial {trial_num}\nNo data points found in torque range 42-57', 
               horizontalalignment='center', verticalalignment='center',
               transform=ax.transAxes, fontsize=12)
        ax.set_title(f'Trial {trial_num}: No data in range 42-57', fontsize=12)
    
    # Store equations for this trial
    all_equations[trial_num] = trial_equations

# Adjust layout for Figure 1
plt.tight_layout(pad=3.0)
plt.suptitle('Z-Height vs Torque Analysis for All Trials (42-57% Torque Range)', 
             fontsize=16, fontweight='bold', y=0.98)

# Create Figure 2: Summary Table of Linear Equations
fig2, ax2 = plt.subplots(figsize=(16, 10))
ax2.axis('off')  # Hide axes for table-only display

# Prepare data for the table
cells = ['Cell 1', 'Cell 2', 'Cell 3', 'Cell 4', 'Cell 5', 'Cell 6']
trial_cols = [f'Trial {i}' for i in range(1, len(trial_data) + 1)]

# Create table data
table_data = []
headers = ['Cell'] + trial_cols

for cell in cells:
    row = [cell]
    for trial_num in sorted(all_equations.keys()):
        if cell in all_equations[trial_num]:
            eq_data = all_equations[trial_num][cell]
            cell_text = f"{eq_data['equation']}\n(R² = {eq_data['r_squared']})"
        else:
            cell_text = "No data\nin range"
        row.append(cell_text)
    table_data.append(row)

# Create the table
table = ax2.table(cellText=table_data,
                 colLabels=headers,
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.15] + [0.2] * len(trial_cols))

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 3)

# Style header row
for i in range(len(headers)):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')
    table[(0, i)].set_fontsize(12)

# Style cell column
for i in range(1, len(cells) + 1):
    table[(i, 0)].set_facecolor('#E8F5E8')
    table[(i, 0)].set_text_props(weight='bold')

# Alternate row colors
for i in range(1, len(cells) + 1):
    for j in range(1, len(headers)):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#F5F5F5')
        else:
            table[(i, j)].set_facecolor('#FFFFFF')

plt.title('Summary of Linear Equations: y = mx + c', 
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("SUMMARY STATISTICS FOR ALL TRIALS")
print("="*60)

# Print summary statistics for all trials
for trial_num, df in trial_data.items():
    print(f"\nTrial {trial_num} Statistics:")
    print(f"  Data shape: {df.shape}")
    print(f"  Original Z-Height range: {df['Z-Height'].min():.2f} to {df['Z-Height'].max():.2f}")
    print(f"  Positive Z-Height range: {df['Z-Height'].max() * -1:.2f} to {df['Z-Height'].min() * -1:.2f}")
    print("  Torque statistics by cell:")
    
    for column in torque_columns:
        non_null_count = df[column].count()
        if non_null_count > 0:
            mean_torque = df[column].mean()
            max_torque = df[column].max()
            # Count data points in 42-57 range
            range_count = ((df[column] >= 42) & (df[column] <= 57)).sum()
            print(f"    {column}: {non_null_count} total points, {range_count} in range 42-57, Mean: {mean_torque:.2f}, Max: {max_torque:.2f}")
        else:
            print(f"    {column}: No data")

print(f"\nPlot created successfully with {len(trial_data)} trials!")