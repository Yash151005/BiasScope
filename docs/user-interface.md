# BiasScope User Interface Guide

Complete guide to using the BiasScope web interface.

## Overview

The BiasScope frontend is built with React and Tailwind CSS, providing a clean, modern interface for bias analysis.

## Pages

### Home Page (`/`)

The landing page provides:

- **Hero Section**: Overview of BiasScope capabilities
- **Features**: Key features highlighted with icons
- **How It Works**: Step-by-step process explanation
- **Start Analysis Button**: Quick access to new analysis

### Analysis Page (`/analysis`)

Start a new bias analysis:

1. **API URL Input**: Enter your model's API endpoint
2. **Validation**: URL format is validated before submission
3. **Status Messages**: Success/error feedback
4. **Loading State**: Shows progress during submission

### Results Page (`/results/:analysisId`)

View analysis results:

#### Progress Section
- Real-time progress bar (0-100%)
- Status updates during analysis
- Automatic refresh while in progress

#### Results Sections (when completed)

1. **Overall Bias Score**
   - Large display of overall bias metric
   - Scale: 0 (no bias) to 1 (maximum bias)
   - Color-coded for quick assessment

2. **Fairness Metrics**
   - Bar chart showing various fairness measurements
   - Includes demographic parity, equalized odds, etc.
   - Interactive tooltips on hover

3. **Feature Influence**
   - Horizontal bar chart
   - Shows which features most impact bias
   - Sorted by influence level

4. **Demographic Parity**
   - Pie chart breakdown
   - Shows distribution across protected attributes
   - Gender, race, and other demographic groups

#### Actions

- **Download Report**: Download PDF report with all results
- **Share**: Copy analysis ID to share results

## Navigation

- **Header**: Always visible with logo and navigation
- **Home Link**: Return to homepage
- **New Analysis Link**: Start another analysis

## Responsive Design

The interface is fully responsive:

- **Desktop**: Full-width layouts with sidebars
- **Tablet**: Adjusted layouts for medium screens
- **Mobile**: Stacked layouts, touch-friendly buttons

## Visual Elements

### Colors

- **Primary Blue**: Main actions and highlights
- **Green**: Success states
- **Red**: Errors and warnings
- **Gray**: Neutral text and backgrounds

### Icons

- Lucide React icons throughout
- Consistent iconography
- Accessible with proper labels

## Data Visualization

Charts powered by Recharts:

- **Bar Charts**: Fairness metrics, feature influence
- **Pie Charts**: Demographic parity
- **Progress Bars**: Analysis progress
- **Interactive**: Hover for details, zoom capabilities

## Best Practices

1. **Wait for Completion**: Let analysis finish before navigating away
2. **Review All Sections**: Check all metrics for comprehensive understanding
3. **Download Reports**: Save PDF reports for documentation
4. **Compare Analyses**: Run multiple analyses to track improvements

## Troubleshooting

### Analysis Not Starting
- Check API URL format
- Verify API is accessible
- Check browser console for errors

### Results Not Loading
- Refresh the page
- Check analysis status
- Verify analysis ID is correct

### Charts Not Displaying
- Check browser compatibility
- Ensure JavaScript is enabled
- Try a different browser
