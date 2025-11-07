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

# All cells regression equations from all trials (from fit_all.py output)
all_cells_equations = {
    'Cell 1': {
        'Trial 1': {'slope': 117.200, 'intercept': -7722.002, 'r_squared': 0.998},
        'Trial 2': {'slope': 91.571, 'intercept': -6008.560, 'r_squared': 0.992}, 
        'Trial 3': {'slope': 92.900, 'intercept': -6105.849, 'r_squared': 0.991},
        'Trial 4': {'slope': 89.057, 'intercept': -5849.702, 'r_squared': 0.986}
    },
    'Cell 2': {
        'Trial 1': {'slope': 79.705, 'intercept': -5217.116, 'r_squared': 0.980},
        'Trial 2': {'slope': 89.276, 'intercept': -5840.457, 'r_squared': 0.992}, 
        'Trial 3': {'slope': 88.438, 'intercept': -5784.236, 'r_squared': 0.994},
        'Trial 4': {'slope': 85.000, 'intercept': -5556.020, 'r_squared': 0.993}
    },
    'Cell 3': {
        'Trial 1': {'slope': 61.893, 'intercept': -4031.049, 'r_squared': 0.963},
        'Trial 2': {'slope': 89.500, 'intercept': -5849.869, 'r_squared': 0.993}, 
        'Trial 3': {'slope': 87.933, 'intercept': -5745.053, 'r_squared': 0.996},
        'Trial 4': {'slope': 106.133, 'intercept': -6950.891, 'r_squared': 0.999}
    },
    'Cell 4': {
        'Trial 1': {'slope': 104.633, 'intercept': -6864.468, 'r_squared': 0.975},
        'Trial 2': {'slope': 90.267, 'intercept': -5913.411, 'r_squared': 0.992}, 
        'Trial 3': {'slope': 79.895, 'intercept': -5227.275, 'r_squared': 0.980},
        'Trial 4': {'slope': 81.833, 'intercept': -5353.966, 'r_squared': 0.993}
    },
    'Cell 5': {
        'Trial 1': {'slope': 202.667, 'intercept': -13305.203, 'r_squared': 1.000},
        'Trial 2': {'slope': 186.167, 'intercept': -12207.618, 'r_squared': 0.967}, 
        'Trial 3': {'slope': 125.367, 'intercept': -8187.536, 'r_squared': 0.983},
        'Trial 4': {'slope': 85.981, 'intercept': -5605.991, 'r_squared': 0.956}
    },
    'Cell 6': {
        'Trial 1': {'slope': 94.700, 'intercept': -6221.678, 'r_squared': 0.993},
        'Trial 2': {'slope': 90.067, 'intercept': -5904.849, 'r_squared': 0.993}, 
        'Trial 3': {'slope': 90.590, 'intercept': -5947.949, 'r_squared': 0.992},
        'Trial 4': {'slope': 87.433, 'intercept': -5738.806, 'r_squared': 0.991}
    }
}

# Extract Cell 1 equations for this analysis
cell_1_equations = all_cells_equations['Cell 1']

# Define torque levels for analysis
torque_levels = np.array([45, 47, 49, 51, 53])
print(f"\nAnalyzing Cell 1 at torque levels: {torque_levels}%")
print(f"Number of trials: {len(cell_1_equations)}")

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

# Calculate Z-height values for each trial and torque level
results_data = []
z_height_matrix = []

print(f"\nCalculating Z-height values for Cell 1:")
print("-" * 50)

for torque in torque_levels:
    row_data = [torque]  # Start with torque value
    z_heights_for_torque = []
    
    print(f"\nTorque = {torque}%:")
    for trial_name, eq_data in cell_1_equations.items():
        z_height = calculate_z_height(torque, eq_data['slope'], eq_data['intercept'])
        row_data.append(z_height)
        z_heights_for_torque.append(z_height)
        print(f"  {trial_name}: Z-height = {z_height:.3f} mm")
    
    # Calculate statistical measures for this torque level
    z_array = np.array(z_heights_for_torque)
    min_val = np.min(z_array)
    max_val = np.max(z_array)
    range_val = max_val - min_val
    
    # Find the steepest slope (most sensitive trial) for uncertainty calculation
    steepest_slope = max([eq_data['slope'] for eq_data in cell_1_equations.values()])
    steepest_trial = [name for name, eq_data in cell_1_equations.items() 
                     if eq_data['slope'] == steepest_slope][0]
    
    # Calculate torque uncertainty using the steepest slope
    # Torque uncertainty = slope × Z-height_range
    torque_uncertainty = steepest_slope * range_val
    
    # Add statistical measures to row (removed steepest_slope from display)
    row_data.extend([min_val, max_val, range_val, torque_uncertainty])
    results_data.append(row_data)
    z_height_matrix.append(z_heights_for_torque)
    
    print(f"  Statistics: Min={min_val:.3f}, Max={max_val:.3f}, Range={range_val:.3f}")
    print(f"              Steepest slope={steepest_slope:.3f} ({steepest_trial})")
    print(f"              Torque uncertainty=±{torque_uncertainty:.3f}%")

# Create summary table
column_names = ['Torque'] + list(cell_1_equations.keys()) + ['Min', 'Max', 'Range', 'Uncertainty(%)']
df_results = pd.DataFrame(results_data, columns=column_names)

print(f"\n" + "="*70)
print("SUMMARY TABLE - CELL 1 Z-HEIGHT ANALYSIS")
print("="*70)
print(df_results.to_string(index=False, float_format='%.3f'))

# Create visualization
fig, ax = plt.subplots(figsize=(16, 10))
ax.axis('off')  # Hide axes for table-only display

# Prepare table data for matplotlib table
table_data = []
headers = column_names

# Format data for display
for _, row in df_results.iterrows():
    formatted_row = []
    for i, val in enumerate(row):
        if i == 0:  # Torque column
            formatted_row.append(f"{val:.0f}")
        elif i <= 4:  # Trial columns  
            formatted_row.append(f"{val:.3f}")
        elif i in [5, 6, 7]:  # Min, Max, Range
            formatted_row.append(f"{val:.3f}")
        else:  # Uncertainty(%)
            formatted_row.append(f"±{val:.1f}%")
    table_data.append(formatted_row)

# Create the table
table = ax.table(cellText=table_data,
                colLabels=headers,
                cellLoc='center',
                loc='center',
                colWidths=[0.1, 0.12, 0.12, 0.12, 0.12, 0.1, 0.1, 0.1, 0.16])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)

# Style header row
for i in range(len(headers)):
    table[(0, i)].set_facecolor('#2E86AB')
    table[(0, i)].set_text_props(weight='bold', color='white')
    table[(0, i)].set_fontsize(10)

# Style torque column
for i in range(1, len(torque_levels) + 1):
    table[(i, 0)].set_facecolor('#A23B72')
    table[(i, 0)].set_text_props(weight='bold', color='white')

# Style trial columns (light blue)
for i in range(1, len(torque_levels) + 1):
    for j in range(1, 5):  # Trial columns
        table[(i, j)].set_facecolor('#F18F01')
        table[(i, j)].set_text_props(color='white', weight='bold')

# Style statistics columns
for i in range(1, len(torque_levels) + 1):
    for j in range(5, len(headers)):  # Statistics columns
        if j == len(headers) - 1:  # Uncertainty(%) column - always red
            table[(i, j)].set_facecolor('#E74C3C')  # Red color for uncertainty
            table[(i, j)].set_text_props(color='white', weight='bold')
        else:
            table[(i, j)].set_facecolor('#ECF0F1')

plt.title('Cell 1: Z-Height to Torque Uncertainty Analysis', 
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

# Additional analysis
print(f"\n" + "="*70)
print("TORQUE UNCERTAINTY ANALYSIS SUMMARY")
print("="*70)

# Find overall statistics
all_uncertainties = [row[-1] for row in results_data]
max_uncertainty = max(all_uncertainties)
min_uncertainty = min(all_uncertainties)
avg_uncertainty = np.mean(all_uncertainties)

print(f"Torque Uncertainty Statistics for Cell 1:")
print(f"  Maximum torque uncertainty: ±{max_uncertainty:.3f}%")
print(f"  Minimum torque uncertainty: ±{min_uncertainty:.3f}%") 
print(f"  Average torque uncertainty: ±{avg_uncertainty:.3f}%")

# Find steepest slope info
steepest_slope = max([eq_data['slope'] for eq_data in cell_1_equations.values()])
steepest_trial = [name for name, eq_data in cell_1_equations.items() 
                 if eq_data['slope'] == steepest_slope][0]
print(f"  Most sensitive trial: {steepest_trial} (slope = {steepest_slope:.1f})")

print(f"\nPer-Torque Uncertainty Analysis:")
for i, torque in enumerate(torque_levels):
    uncertainty = results_data[i][-1]
    range_val = results_data[i][-3]
    status = "LOW" if uncertainty < 0.2 else "MEDIUM" if uncertainty < 0.5 else "HIGH"
    print(f"  {torque}%: ±{uncertainty:.3f}% torque (Z-range: {range_val:.3f}mm) - {status}")

print(f"\nPhysical Interpretation:")
print(f"  • This uncertainty represents actual torque measurement error")
print(f"  • Caused by Z-height positioning variations between trials") 
print(f"  • Uses {steepest_trial} slope (most sensitive) for worst-case analysis")
print(f"  • Steeper slopes = higher sensitivity to positioning errors")

print(f"\nRecommendations:")
if max_uncertainty < 0.2:
    print("  ✓ EXCELLENT: Torque uncertainty <0.2% across all levels")
elif max_uncertainty < 0.5:
    print("  ✓ GOOD: Torque uncertainty <0.5% - acceptable for most applications")
else:
    print("  ⚠ ATTENTION: Some torque levels show >0.5% uncertainty")
    print("    Consider improving Z-height positioning consistency")

print(f"\nMethodology Validation:")
print("  ✓ This approach provides REAL, PHYSICAL uncertainty measures")
print("  ✓ Directly translates positioning errors to measurement errors") 
print("  ✓ Uses worst-case scenario (steepest slope) for conservative estimates")
print("  ✓ More meaningful than statistical relative errors")

print(f"\nAnalysis complete! Total data points analyzed: {len(torque_levels) * len(cell_1_equations)}")
