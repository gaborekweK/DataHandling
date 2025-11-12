# Uncertainty Analysis Script
# Quantifying error and variability across trials for rheometer measurements

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats                                                                                                                                                                                                  
import sys
import os

# Set matplotlib style for better plots
plt.style.use('default')
sns.set_palette("husl")

print("="*70)
print("UNCERTAINTY ANALYSIS FOR RHEOMETER MEASUREMENTS")
print("="*70)

# Import regression equations from fit_all.py analysis
# These equations were obtained from linear regression analysis (y = mx + c)
# where y = Torque, x = Z-Height (positive), for torque range 42-57%

# All cells regression equations from all trials (10K data from plotALL10K.py output)
all_cells_equations = {
    'Cell 1': {
        'Trial 1': {'slope': 87.767, 'intercept': -5759.814, 'r_squared': 0.996},
        'Trial 2': {'slope': 135.833, 'intercept': -8941.347, 'r_squared': 0.975}, 
        'Trial 3': {'slope': 89.133, 'intercept': -5838.821, 'r_squared': 0.996},
        'Trial 4': {'slope': 84.895, 'intercept': -5557.924, 'r_squared': 0.992}
    },
    'Cell 2': {
        'Trial 1': {'slope': 89.848, 'intercept': -5873.516, 'r_squared': 0.991},
        'Trial 2': {'slope': 89.767, 'intercept': -5867.689, 'r_squared': 0.993}, 
        'Trial 3': {'slope': 84.867, 'intercept': -5541.969, 'r_squared': 0.994},
        'Trial 4': {'slope': 85.600, 'intercept': -5589.990, 'r_squared': 0.995}
    },
    'Cell 3': {
        'Trial 1': {'slope': 90.657, 'intercept': -5921.408, 'r_squared': 0.991},
        'Trial 2': {'slope': 93.767, 'intercept': -6128.208, 'r_squared': 0.994}, 
        'Trial 3': {'slope': 88.867, 'intercept': -5801.210, 'r_squared': 0.991},
        'Trial 4': {'slope': 87.552, 'intercept': -5714.667, 'r_squared': 0.992}
    },
    'Cell 4': {
        'Trial 1': {'slope': 90.933, 'intercept': -5922.497, 'r_squared': 0.992},
        'Trial 2': {'slope': 92.267, 'intercept': -6010.167, 'r_squared': 0.991}, 
        'Trial 3': {'slope': 89.933, 'intercept': -5853.865, 'r_squared': 0.994},
        'Trial 4': {'slope': 91.543, 'intercept': -5960.168, 'r_squared': 0.990}
    },
    'Cell 5': {
        'Trial 1': {'slope': 94.700, 'intercept': -6176.787, 'r_squared': 0.997},
        'Trial 2': {'slope': 99.500, 'intercept': -6502.016, 'r_squared': 0.979}, 
        'Trial 3': {'slope': 93.600, 'intercept': -6102.294, 'r_squared': 0.995},
        'Trial 4': {'slope': 94.567, 'intercept': -6165.921, 'r_squared': 0.995}
    },
    'Cell 6': {
        'Trial 1': {'slope': 90.767, 'intercept': -5940.868, 'r_squared': 0.996},
        'Trial 2': {'slope': 96.767, 'intercept': -6327.421, 'r_squared': 0.991}, 
        'Trial 3': {'slope': 90.305, 'intercept': -5898.003, 'r_squared': 0.993},
        'Trial 4': {'slope': 88.900, 'intercept': -5804.552, 'r_squared': 0.994}
    }
}

# Define torque levels for analysis
torque_levels = np.array([42, 45, 48, 51, 54, 57])
print(f"\nAnalyzing all 6 cells at torque levels: {torque_levels}%")
print(f"Number of cells: {len(all_cells_equations)}")
print(f"Number of trials per cell: 4")

def calculate_z_height(torque, slope, intercept):
    """
    Calculate Z-height from torque using linear equation: y = mx + c
    Rearranged to: x = (y - c) / m
    
    Parameters:
    torque: Torque value (y)
    slope: Slope of regression line (m)
    intercept: Intercept of regression line (c)
    
    Returns:
    Z-height value (x) rounded to 3 decimal places
    """
    z_height = (torque - intercept) / slope
    return round(z_height, 3)

def analyze_cell_uncertainty(cell_name, cell_equations):
    """
    Analyze uncertainty for a single cell across all torque levels.
    """
    print(f"\nAnalyzing {cell_name}...")
    
    results_data = []
    
    for torque in torque_levels:
        row_data = [torque]  # Start with torque value
        z_heights_for_torque = []
        
        # Calculate Z-heights for this torque level across all trials
        for trial_name, eq_data in cell_equations.items():
            z_height = calculate_z_height(torque, eq_data['slope'], eq_data['intercept'])
            row_data.append(z_height)
            z_heights_for_torque.append(z_height)
        
        # Calculate statistical measures for this torque level
        z_array = np.array(z_heights_for_torque)
        min_val = np.min(z_array)
        max_val = np.max(z_array)
        range_val = max_val - min_val
        
        # Find the steepest slope (most sensitive trial) for uncertainty calculation
        steepest_slope = max([eq_data['slope'] for eq_data in cell_equations.values()])
        
        # Calculate torque uncertainty using the steepest slope
        # Torque uncertainty = |slope| × Z-height_range  
        torque_uncertainty = steepest_slope * range_val
        
        # Add statistical measures to row
        row_data.extend([min_val, max_val, range_val, torque_uncertainty])
        results_data.append(row_data)
    
    return results_data

# Analyze all cells
print("="*70)
print("CALCULATING UNCERTAINTY FOR ALL CELLS")
print("="*70)

all_results = {}
for cell_name, cell_equations in all_cells_equations.items():
    all_results[cell_name] = analyze_cell_uncertainty(cell_name, cell_equations)

# Create visualization with 6 tables (one per row)
fig, axes = plt.subplots(6, 1, figsize=(22, 36))

print(f"\n" + "="*70)
print("CREATING UNCERTAINTY ANALYSIS TABLES FOR ALL CELLS")
print("="*70)

for idx, (cell_name, results_data) in enumerate(all_results.items()):
    ax = axes[idx]
    ax.axis('off')  # Hide axes for table-only display
    
    # Create column names with shorter, more compact headers
    column_names = ['Torque(%)', 'Trial 1(mm)', 'Trial 2(mm)', 'Trial 3(mm)', 'Trial 4(mm)', 
                   'Min(mm)', 'Max(mm)', 'Range(mm)', 'Uncertainty(%)']
    
    # Prepare table data for display
    table_data = []
    for row in results_data:
        formatted_row = []
        for i, val in enumerate(row):
            if i == 0:  # Torque column
                formatted_row.append(f"{val:.0f}")
            elif i <= 4:  # Trial columns  
                formatted_row.append(f"{val:.3f}")
            elif i in [5, 6, 7]:  # Min, Max, Range
                formatted_row.append(f"{val:.3f}")
            else:  # Uncertainty(%)
                formatted_row.append(f"±{val:.1f}")
        table_data.append(formatted_row)
    
    # Create the table with adjusted column widths for better space utilization
    table = ax.table(cellText=table_data,
                    colLabels=column_names,
                    cellLoc='center',
                    loc='center',
                    colWidths=[0.08, 0.10, 0.10, 0.10, 0.10, 0.08, 0.08, 0.08, 0.12])
    
    # Style the table with larger scaling and better font sizes
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 2.8)
    
    # Style header row with better font size
    for i in range(len(column_names)):
        table[(0, i)].set_facecolor('#2E86AB')
        table[(0, i)].set_text_props(weight='bold', color='white')
        table[(0, i)].set_fontsize(11)
    
    # Style torque column
    for i in range(1, len(torque_levels) + 1):
        table[(i, 0)].set_facecolor('#A23B72')
        table[(i, 0)].set_text_props(weight='bold', color='white')
    
    # Style trial columns (orange)
    for i in range(1, len(torque_levels) + 1):
        for j in range(1, 5):  # Trial columns
            table[(i, j)].set_facecolor('#F18F01')
            table[(i, j)].set_text_props(color='white', weight='bold')
    
    # Style statistics columns
    for i in range(1, len(torque_levels) + 1):
        for j in range(5, len(column_names)):  # Statistics columns
            if j == len(column_names) - 1:  # Uncertainty(%) column - always red
                table[(i, j)].set_facecolor('#E74C3C')  # Red color for uncertainty
                table[(i, j)].set_text_props(color='white', weight='bold')
            else:
                table[(i, j)].set_facecolor('#ECF0F1')
    
    # Set subplot title with better positioning
   # ax.set_title(f'{cell_name} - Uncertainty Analysis', 
               # fontsize=16, fontweight='bold', pad=25)

plt.suptitle('', 
             fontsize=20, fontweight='bold', y=0.99)
plt.tight_layout(rect=[0, 0.02, 1, 0.98])
plt.show()

# Print comprehensive summary
print(f"\n" + "="*70)
print("COMPREHENSIVE UNCERTAINTY ANALYSIS SUMMARY")
print("="*70)

for cell_name, results_data in all_results.items():
    cell_equations = all_cells_equations[cell_name]
    
    # Calculate summary statistics
    all_uncertainties = [row[-1] for row in results_data]
    max_uncertainty = max(all_uncertainties)
    min_uncertainty = min(all_uncertainties)
    avg_uncertainty = np.mean(all_uncertainties)
    
    # Find steepest slope for this cell
    steepest_slope = max([eq_data['slope'] for eq_data in cell_equations.values()])
    steepest_trial = [name for name, eq_data in cell_equations.items() 
                     if eq_data['slope'] == steepest_slope][0]
    
    print(f"\n{cell_name} Summary:")
    print(f"  Maximum uncertainty: ±{max_uncertainty:.1f}%")
    print(f"  Minimum uncertainty: ±{min_uncertainty:.1f}%") 
    print(f"  Average uncertainty: ±{avg_uncertainty:.1f}%")
    print(f"  Most sensitive trial: {steepest_trial} (slope = {steepest_slope:.1f})")
    
    # Performance assessment
    if max_uncertainty < 5:
        status = "EXCELLENT"
    elif max_uncertainty < 10:
        status = "GOOD"
    elif max_uncertainty < 20:
        status = "ACCEPTABLE"
    else:
        status = "NEEDS ATTENTION"
    
    print(f"  Performance: {status}")

print(f"\nOverall Analysis:")
print(f"  Total data points analyzed: {len(torque_levels) * 4 * len(all_cells_equations)}")
print(f"  Torque levels: {torque_levels}")
print(f"  Analysis method: Steepest slope uncertainty propagation")

print(f"\nAnalysis complete!")


