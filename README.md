# # DataHandling - Rheometer Data Analysis Project

## Overview
This project provides comprehensive data analysis and visualization tools for rheometer measurements, focusing on Z-Height vs Torque relationships across multiple trials and measurement cells.

## Scripts Description

### `curvefit.py`
- **Purpose**: Analyzes a single trial with linear regression fitting
- **Output**: Z-Height vs Torque plot with fitted equations for all 6 cells
- **Features**: Focuses on torque range 42-57%, displays R² values

### `fit_all.py`
- **Purpose**: Comprehensive analysis of all 4 trials
- **Output**: 
  - Figure 1: 2×2 subplot layout showing all trials
  - Figure 2: Summary table of linear equations
- **Features**: Cross-trial comparison, equation storage, statistical summaries

### `Uncertainity.py`
- **Purpose**: Uncertainty quantification for Cell 1 only
- **Method**: Steepest slope uncertainty propagation
- **Output**: Professional table with Z-height variations and torque uncertainties

### `Uncertainity_all.py`
- **Purpose**: Comprehensive uncertainty analysis for all 6 cells
- **Output**: 6 vertically-arranged tables (one per cell)
- **Features**: Physical uncertainty measures, performance assessment, color-coded visualization

## Key Features

### Data Analysis
- Linear regression analysis (y = mx + c) where y=Torque, x=Z-Height
- R² values typically 0.95-1.00 indicating excellent fits
- Torque filtering to 42-57% range for consistent analysis
- Z-Height conversion to positive values for intuitive interpretation

### Uncertainty Quantification
- **Steepest Slope Method**: Uses most sensitive trial for conservative estimates
- **Physical Meaning**: Translates Z-height positioning errors to actual torque measurement errors
- **Performance Categories**: EXCELLENT (<5%), GOOD (<10%), ACCEPTABLE (<20%), NEEDS ATTENTION (>20%)

### Visualization
- Professional matplotlib tables with color coding
- Subplot layouts for multi-trial comparison
- Equation display positioned at line endpoints
- Statistical summary outputs

## Usage
Run from the main DataHandling directory:
```bash
# Single trial analysis
python Row1DataSummary/curvefit.py

# All trials analysis
python Row1DataSummary/fit_all.py

# Cell 1 uncertainty
python Row1DataSummary/Uncertainity.py

# All cells uncertainty
python Row1DataSummary/Uncertainity_all.py
```

## Data Format
Excel files contain:
- `Z-Height`: Position measurements (converted to positive values)
- `Cell_1_Torque` to `Cell_6_Torque`: Torque measurements (%) for 6 measurement cells
- Analysis focuses on 42-57% torque range for consistency

## Dependencies
- numpy, pandas, matplotlib, seaborn
- scipy, scikit-learn, openpyxl
- plotly, statsmodels

## Results Summary
- **Cell Performance**: Cells 3-4 typically show best consistency (lowest uncertainty)
- **Trial Sensitivity**: Trial 1 generally has steepest slopes (highest sensitivity)
- **Measurement Quality**: Most uncertainties <10%, indicating excellent experimental control
- **Physical Insights**: Reveals real measurement limitations from positioning variations