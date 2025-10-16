# PlotMixin - Mixin class for plotting spectrum analyzer data
# Author: [Simón Aulet]
# Date: 2025-09-10

import matplotlib.pyplot as plt
import numpy as np
from typing import Literal, Optional, Tuple, Dict, Any

class PlotMixin:
    """
    Mixin for adding plotting functionality to the SAData class.

    Provides methods for visualizing data in different representations:
    - Time domain
    - Frequency domain
    - Polar representation
    """

    def plot_time(self, mag: Literal['dB', 'dBm'] = 'dB', y_limits: Optional[Tuple[float, float]] = None, savefig: str = '', legend: bool = False, **kwargs):
        """
        Plot data in the time domain.

        Parameters:
        -----------
        mag : str, optional
            Magnitude unit ('dB' or 'dBm'), default 'dB'
            'dB' uses normalized data (P - max(P))
            'dBm' uses absolute power in dBm
        y_limits : Tuple[float, float], optional
            Vertical limits for y-axis (min, max). If None, auto-adjusts.
        savefig : str, optional
            Filename to save the figure. If empty string, figure is not saved.
        legend : bool, optional
            If True, shows a box with statistics (min, max, and mean)

        """
        # Get x-axis data (time)
        x_data = self.get_x_data()

        # Get y-axis data and convert to specified unit
        if mag == 'dB':
            y_data = self.convert_to_db()
        elif mag == 'dBm':
            y_data = self.convert_to_dBm()
        else:
            raise ValueError(f"Invalid magnitude unit: {mag}. Use 'dB' or 'dBm'")

        # Create figure and axes
        fig_kwargs = {'figsize': (10, 6)}
        # Separate parameters for plt.subplots and ax.plot
        subplot_params = {}
        plot_params = {'linewidth': 1.5}
        ax_params = {}

        # Filter parameters for specific functions
        for key, value in kwargs.items():
            if key in ['figsize', 'dpi', 'facecolor', 'edgecolor', 'frameon', 'tight_layout', 'constrained_layout']:
                fig_kwargs[key] = value
            elif key in ['color', 'linestyle', 'marker', 'markersize', 'label']:
                plot_params[key] = value
            elif key in ['title', 'xlabel', 'ylabel', 'xlim', 'ylim']:
                ax_params[key] = value
            else:
                # Unrecognized parameters are ignored
                pass

        fig, ax = plt.subplots(**fig_kwargs)

        # Plot the data
        ax.plot(x_data, y_data, **plot_params)

        # Apply axis configuration parameters
        if 'title' in ax_params:
            ax.set_title(ax_params['title'])
        else:
            ax.set_title(f'Time Domain Data - {mag}', fontsize=14)

        if 'xlabel' in ax_params:
            ax.set_xlabel(ax_params['xlabel'])
        else:
            ax.set_xlabel('Time', fontsize=12)

        if 'ylabel' in ax_params:
            ax.set_ylabel(ax_params['ylabel'])
        else:
            ax.set_ylabel(mag, fontsize=12)

        if 'xlim' in ax_params:
            ax.set_xlim(ax_params['xlim'])
        if 'ylim' in ax_params:
            ax.set_ylim(ax_params['ylim'])

        # Configure logarithmic grid
        ax.grid(True, which='both', linestyle='--', alpha=0.7)

        # Configure vertical limits if specified (only if not passed via kwargs)
        if y_limits is not None and 'ylim' not in ax_params:
            ax.set_ylim(y_limits)

        # Add statistics box if requested
        if legend:
            min_val = np.min(y_data)
            max_val = np.max(y_data)
            mean_val = np.mean(y_data)

            # Create text with statistics
            stats_text = f'Min: {min_val:.2f} {mag}\nMax: {max_val:.2f} {mag}\nMean: {mean_val:.2f} {mag}'

            # Add box with statistics
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=15,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightsteelblue', alpha=0.9))

        # Improve layout
        plt.tight_layout()

        # Save figure if filename is specified
        if savefig:
            fig.savefig(savefig, bbox_inches='tight', dpi=300)

    def plot_frec(self, mag: Literal['dB', 'dBm'] = 'dB', savefig: str = ''):
        """
        Plot data in the frequency domain.

        Parameters:
        -----------
        mag : str, optional
            Magnitude unit ('dB' or 'dBm'), default 'dB'
        savefig : str, optional
            Filename to save the figure. If empty string, figure is not saved.

        Returns:
        --------
        matplotlib.figure.Figure
            Figure with the generated plot
        """
        # TODO: Implement frequency domain plot
        pass

        # Save figure if filename is specified
        if savefig:
            # Figure would be saved here when plot_frec is implemented
            pass

    def plot_polar(self, mag: Literal['dB', 'dBm'] = 'dB', mag_limits: Optional[Tuple[float, float]] = None, savefig: str = '', legend: bool = False, **kwargs):
        """
        Plot data in polar representation.

        Parameters:
        -----------
        mag : str, optional
            Magnitude unit ('dB' or 'dBm'), default 'dB'
            'dB' uses normalized data (P - max(P))
            'dBm' uses absolute power in dBm
        mag_limits : Tuple[float, float], optional
            Magnitude limits for radial axis (min, max). If None, auto-adjusts.
        savefig : str, optional
            Filename to save the figure. If empty string, figure is not saved.
        legend : bool, optional
            If True, shows a box with statistics (min, max, and mean)

        Returns:
        --------
        matplotlib.figure.Figure
            Figure with the generated plot
        """
        # Get magnitude data and convert to specified unit
        if mag == 'dB':
            magnitude_data = self.convert_to_db()
        elif mag == 'dBm':
            magnitude_data = self.convert_to_dBm()
        else:
            raise ValueError(f"Invalid magnitude unit: {mag}. Use 'dB' or 'dBm'")

        # Get angular data in radians
        angle_data = self.convert_to_polar()

        # Create figure and polar axes
        fig_kwargs = {'figsize': (8, 8), 'subplot_kw': {'projection': 'polar'}}
        # Separate parameters for plt.subplots and ax.plot
        subplot_params = {}
        plot_params = {'linewidth': 1.5}
        ax_params = {}

        # Filter parameters for specific functions
        for key, value in kwargs.items():
            if key in ['figsize', 'dpi', 'facecolor', 'edgecolor', 'frameon', 'tight_layout', 'constrained_layout']:
                fig_kwargs[key] = value
            elif key in ['color', 'linestyle', 'marker', 'markersize', 'label']:
                plot_params[key] = value
            elif key in ['title', 'xlabel', 'ylabel', 'xlim', 'ylim']:
                ax_params[key] = value
            else:
                # Unrecognized parameters are ignored
                pass

        fig, ax = plt.subplots(**fig_kwargs)

        # Plot data in polar coordinates
        ax.plot(angle_data, magnitude_data, **plot_params)

        # Apply axis configuration parameters
        if 'title' in ax_params:
            ax.set_title(ax_params['title'])
        else:
            ax.set_title(f'Polar Representation - {mag}', fontsize=14, pad=20)

        if 'ylabel' in ax_params:
            ax.set_ylabel(ax_params['ylabel'])
        else:
            ax.set_ylabel(mag, fontsize=12, labelpad=20)

        if 'ylim' in ax_params:
            ax.set_ylim(ax_params['ylim'])
        # Configure grid with better label visibility
        ax.grid(True, linestyle='--', alpha=0.7)

        # Force display of radial labels
        ax.set_rlabel_position(22.5)  # Position radial labels at 22.5 degrees

        # Ensure all radial grid labels are displayed
        ax.tick_params(axis='y', labelsize=8)

        # Configure magnitude limits if specified (only if not passed via kwargs)
        if mag_limits is not None and 'ylim' not in ax_params:
            ax.set_ylim(mag_limits)

        # Configure angles in degrees instead of radians
        ax.set_thetagrids(range(0, 360, 45),
                         ['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'])

        # Add statistics box if requested
        if legend:
            min_val = np.min(magnitude_data)
            max_val = np.max(magnitude_data)
            mean_val = np.mean(magnitude_data)

            # Create text with statistics
            stats_text = f'Min: {min_val:.2f} {mag}\nMax: {max_val:.2f} {mag}\nMean: {mean_val:.2f} {mag}'

            # Add box with statistics
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightsteelblue', alpha=0.9))

        # Improve layout
        plt.tight_layout()

        # Save figure if filename is specified
        if savefig:
            fig.savefig(savefig, bbox_inches='tight', dpi=300)

        return fig, ax

    def plot_superposition(self, mag: Literal['dB', 'dBm'] = 'dB', 
                          left_shift_deg: float = 0.0, right_shift_deg: float = 0.0) -> Dict[str, int]:
        """
        Plot data with mirrored superposition for visualization.

        Creates two mirrored plots with extremes meeting at the center.

        Parameters:
        -----------
        mag : str, optional
            Magnitude unit ('dB' or 'dBm'), default 'dB'

        Returns:
        --------
        Dict[str, int]
            Dictionary with calculated crop indices {'start_index': int, 'end_index': int}
        """
        # Get original data
        x_data = self.get_x_data()
        if mag == 'dB':
            y_data = self.convert_to_db()
        elif mag == 'dBm':
            y_data = self.convert_to_dBm()
        else:
            raise ValueError(f"Invalid magnitude unit: {mag}. Use 'dB' or 'dBm'")

        n_points = len(x_data)
        mid_point = n_points // 2

        # Split data into two halves (invertir nombres para coincidir con visualización)
        right_y = y_data[mid_point:]   # Segunda mitad como derecha visual (espejada)
        left_y = y_data[:mid_point]    # Primera mitad como izquierda visual
        
        # Calculate crop indices based on angular shifts
        # left_shift_deg applies to visual left (original right data)
        # right_shift_deg applies to visual right (original left data)
        total_points = n_points
        
        # Calculate number of points to crop from each side
        left_crop_points = int((left_shift_deg / 360.0) * len(right_y))
        right_crop_points = int((right_shift_deg / 360.0) * len(left_y))
        
        # Calculate crop indices for the original data
        # start_index: crop from beginning (visual right side)
        start_index = right_crop_points
        # end_index: crop from end (visual left side)  
        end_index = total_points - left_crop_points

        # Calculate shift factors from degrees (invertir para coincidir con visualización)
        # Positive shift means the side is "too far", so we need to move it inward
        right_shift_factor = left_shift_deg / 360.0 if left_shift_deg != 0 else 0
        left_shift_factor = right_shift_deg / 360.0 if right_shift_deg != 0 else 0

        # Create artificial x-axis for superposition with shifts
        # Right half (visual left): goes from center outward to left
        right_x = []
        for i in range(len(right_y)):
            distance_from_center = len(right_y) - i - 1
            # Apply right shift: positive shift moves visual left side inward (less negative)
            shifted_distance = distance_from_center - right_shift_factor * len(right_y)
            right_x.append(-shifted_distance)

        # Left half (visual right): goes from center outward to right
        left_x = []
        for i in range(len(left_y)):
            distance_from_center = i
            
            # Apply 1 unit shift for even number of points to avoid overlap
            if n_points % 2 == 0:
                distance_from_center += 1

            # Apply left shift: positive shift moves visual right side inward (less positive)
            shifted_distance = distance_from_center - left_shift_factor * len(left_y)
            left_x.append(shifted_distance)

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot both halves using artificial x-axis (invertir leyendas)
        ax.plot(right_x, right_y, 'b-', linewidth=2, label='Right half (original)')
        ax.plot(left_x, left_y, 'r-', linewidth=2, label='Left half (mirrored)')

        # Configure axes
        # Create title with shift information
        title = f'Superposition Visualization - {mag}'
        if left_shift_deg != 0 or right_shift_deg != 0:
            title += f'\nRight shift: {left_shift_deg}°, Left shift: {right_shift_deg}°'
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Position from Center', fontsize=12)
        ax.set_ylabel(mag, fontsize=12)
        
        # Fix x-axis limits to maintain visual center regardless of cropping
        max_distance = max(len(right_y), len(left_y))
        ax.set_xlim(-max_distance - 1, max_distance + 1)
        
        ax.grid(True, which='both', linestyle='--', alpha=0.7)
        ax.legend()

        plt.tight_layout()
        
        # Return crop indices for use with crop_data
        crop_info = {
            'start_index': start_index,
            'end_index': end_index
        }
        
        return crop_info
