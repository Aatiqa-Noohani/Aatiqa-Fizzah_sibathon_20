"""
Chart Generator Module
Creates visualizations for energy consumption data
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime
import config


class ChartGenerator:
    """Generates charts and visualizations for energy data"""
    
    def __init__(self):
        """Initialize the chart generator"""
        # Set the style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def create_daily_chart(self, data, title="Daily Energy Consumption"):
        """
        Create a line chart for daily energy consumption
        
        Args:
            data: DataFrame with datetime and energy columns
            title: Chart title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot the data
        ax.plot(data.index, data.values, 
                color=config.CHART_COLORS['primary'], 
                linewidth=2, 
                marker='o', 
                markersize=4)
        
        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Hour of Day', fontsize=11)
        ax.set_ylabel('Energy (MW)', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        
        # Tight layout
        plt.tight_layout()
        
        return fig
    
    def create_weekly_chart(self, daily_data, title="Weekly Energy Consumption"):
        """
        Create a bar chart for weekly energy consumption
        
        Args:
            daily_data: Series with dates as index and total energy as values
            title: Chart title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Create bar chart
        dates = [str(d) for d in daily_data.index]
        values = daily_data.values
        
        bars = ax.bar(dates, values, 
                      color=config.CHART_COLORS['success'], 
                      alpha=0.7,
                      edgecolor='black',
                      linewidth=1.2)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.0f}',
                   ha='center', va='bottom', fontsize=9)
        
        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Total Energy (MW)', fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        
        # Tight layout
        plt.tight_layout()
        
        return fig
    
    def create_hourly_pattern_chart(self, hourly_avg, title="Average Hourly Energy Pattern"):
        """
        Create a line chart showing average energy consumption by hour
        
        Args:
            hourly_avg: Series with hour as index and average energy as values
            title: Chart title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot the pattern
        ax.plot(hourly_avg.index, hourly_avg.values,
                color=config.CHART_COLORS['warning'],
                linewidth=3,
                marker='o',
                markersize=6,
                markerfacecolor=config.CHART_COLORS['secondary'],
                markeredgecolor='black',
                markeredgewidth=1)
        
        # Fill area under the curve
        ax.fill_between(hourly_avg.index, hourly_avg.values, 
                        alpha=0.3, 
                        color=config.CHART_COLORS['warning'])
        
        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Hour of Day', fontsize=11)
        ax.set_ylabel('Average Energy (MW)', fontsize=11)
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, alpha=0.3)
        
        # Tight layout
        plt.tight_layout()
        
        return fig
    
    def create_prediction_chart(self, predictions, title="Energy Consumption Predictions"):
        """
        Create a chart showing predictions
        
        Args:
            predictions: List of dictionaries with 'hour'/'day_number' and 'prediction'
            title: Chart title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Extract data
        if 'hour' in predictions[0]:
            x_values = [p['hour'] for p in predictions]
            xlabel = 'Hour of Day'
        else:
            x_values = [p['day_number'] for p in predictions]
            xlabel = 'Day'
        
        y_values = [p['prediction'] for p in predictions]
        
        # Create line plot with markers
        ax.plot(x_values, y_values,
                color=config.CHART_COLORS['info'],
                linewidth=2.5,
                marker='s',
                markersize=7,
                markerfacecolor=config.CHART_COLORS['secondary'],
                markeredgecolor='black',
                markeredgewidth=1,
                label='Predicted')
        
        # Fill area
        ax.fill_between(x_values, y_values,
                        alpha=0.2,
                        color=config.CHART_COLORS['info'])
        
        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel('Predicted Energy (MW)', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        
        # Tight layout
        plt.tight_layout()
        
        return fig
    
    def create_device_comparison_chart(self, devices_data, title="Device Energy Comparison"):
        """
        Create a bar chart comparing energy consumption of different devices
        
        Args:
            devices_data: List of device simulation results
            title: Chart title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Extract data
        devices = [d['device'] for d in devices_data]
        energy = [d['energy_kwh'] for d in devices_data]
        costs = [d['cost'] for d in devices_data]
        
        # Create bar chart
        x_pos = range(len(devices))
        bars = ax.bar(x_pos, energy,
                      color=config.CHART_COLORS['primary'],
                      alpha=0.7,
                      edgecolor='black',
                      linewidth=1.2)
        
        # Color bars by energy level
        colors = []
        max_energy = max(energy)
        for e in energy:
            if e < max_energy * 0.3:
                colors.append(config.CHART_COLORS['success'])
            elif e < max_energy * 0.6:
                colors.append(config.CHART_COLORS['warning'])
            else:
                colors.append(config.CHART_COLORS['secondary'])
        
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        # Add value labels
        for i, (bar, cost) in enumerate(zip(bars, costs)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f} kWh\n${cost:.2f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Device', fontsize=11)
        ax.set_ylabel('Energy Consumption (kWh)', fontsize=11)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(devices, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
        
       
 # Tight layout
        plt.tight_layout()
        
        return fig
    
    def embed_chart_in_tkinter(self, figure, parent_widget):
        """
        Embed a matplotlib figure in a Tkinter widget
        
        Args:
            figure: matplotlib Figure object
            parent_widget: Tkinter parent widget
            
        Returns:
            FigureCanvasTkAgg object
        """
        canvas = FigureCanvasTkAgg(figure, parent_widget)
        canvas.draw()
        return canvas
    
    def close_all_figures(self):
        """Close all matplotlib figures to free memory"""
        plt.close('all')
