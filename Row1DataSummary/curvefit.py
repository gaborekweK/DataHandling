# Data Analysis and Visualization Script
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

# Set matplotlib style for better plots
plt.style.use('default')
sns.set_palette("husl")

# Load Trial1.xlsx data
print("Loading Trial1.xlsx data...")
try:
    # Read the Excel file
    df = pd.read_excel('Trial1.xlsx')
    print("Data loaded successfully!")
    print(f"Data shape: {df.shape}")
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())
    
except FileNotFoundError:
    print("Error: Trial1.xlsx file not found in the current directory")
except Exception as e:
    print(f"Error loading data: {e}")

# Check if the required columns exist before plotting
if 'df' in locals():
    print("\nData info:")
    print(df.info())
    
    # Create the plot of Z-Height vs Torque for all 6 cells (filtered for torque 45-55)
    plt.figure(figsize=(14, 8))
    
    # Define colors for each cell
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Plot each cell's torque vs Z-Height, filtering for torque values between 45 and 55
    torque_columns = ['Cell_1_Torque', 'Cell_2_Torque', 'Cell_3_Torque', 
                     'Cell_4_Torque', 'Cell_5_Torque', 'Cell_6_Torque']
    
    # Track if any data is plotted and store data for fitting
    has_data = False
    cell_data = {}  # Store data for linear fitting
    
    for i, column in enumerate(torque_columns):
        # Filter for non-null values AND torque between 42 and 57
        mask = (df[column].notna()) & (df[column] >= 42) & (df[column] <= 57)
        
        if mask.any():  # Only plot if there are data points in the range
            # Multiply Z-Height by -1 to make it positive
            z_height_positive = df.loc[mask, 'Z-Height'] * -1
            torque_values = df.loc[mask, column]
            
            # Plot the data points
            plt.plot(z_height_positive, torque_values, 
                    marker='o', markersize=4, linewidth=2, 
                    color=colors[i], label=f'Cell {i+1}', alpha=0.8)
            
            # Store data for linear fitting
            cell_data[i] = {
                'z_height': z_height_positive.values,
                'torque': torque_values.values,
                'column': column
            }
            
            has_data = True
            print(f"Cell {i+1}: {mask.sum()} data points in range 42-57")
        else:
            print(f"Cell {i+1}: No data points in range 42-57")
    
    # Add linear fit lines for each cell with data
    if has_data:
        print("\nLinear fit equations:")
        for i, data in cell_data.items():
            # Perform linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(data['z_height'], data['torque'])
            
            # Generate points for the fitted line
            x_fit = np.linspace(data['z_height'].min(), data['z_height'].max(), 100)
            y_fit = slope * x_fit + intercept
            
            # Plot the fitted line
            plt.plot(x_fit, y_fit, 'k--', alpha=0.7, linewidth=1.5)
            
            # Create equation label
            equation = f'Cell {i+1}: y = {slope:.3f}x + {intercept:.3f} (R² = {r_value**2:.3f})'
            print(equation)
            
            # Position equation text at the end (top) of the fitted line
            # Use the maximum Z-Height point for x position
            text_x = data['z_height'].max()
            text_y = slope * text_x + intercept  # Y position at the end of the line
            
            # Add small offset to position label slightly above the line end
            text_y += 0.3
            
            plt.text(text_x, text_y, f'y = {slope:.3f}x + {intercept:.3f}', 
                    fontsize=8, ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    if has_data:
        plt.xlabel('Z-Height/mm (Positive)', fontsize=12)
        plt.ylabel('Torque/%', fontsize=12)
        plt.title('Z-Height vs Torque for All 6 Cells', fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Set y-axis limits to 42-57
        plt.ylim(42, 57)
        
        # Format x-axis to show 3 decimal places
        ax = plt.gca()
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.3f}'))
        
        plt.tight_layout()
        
        # Add some styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    else:
        plt.text(0.5, 0.5, 'No data points found in torque range 42-57', 
                horizontalalignment='center', verticalalignment='center',
                transform=plt.gca().transAxes, fontsize=14)
        plt.title('Z-Height vs Torque (No data in range 42-57)', fontsize=14)
    
    # Show the plot
    plt.show()
    
    print("Plot created successfully!")
    
    # Print some basic statistics
    print("\nBasic Statistics:")
    print(f"Original Z-Height range: {df['Z-Height'].min():.2f} to {df['Z-Height'].max():.2f}")
    print(f"Positive Z-Height range: {df['Z-Height'].max() * -1:.2f} to {df['Z-Height'].min() * -1:.2f}")
    print("\nTorque statistics by cell:")
    for column in torque_columns:
        non_null_count = df[column].count()
        if non_null_count > 0:
            mean_torque = df[column].mean()
            max_torque = df[column].max()
            print(f"{column}: {non_null_count} data points, Mean: {mean_torque:.2f}, Max: {max_torque:.2f}")
        else:
            print(f"{column}: No data")