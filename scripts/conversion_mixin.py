# ConversionMixin - Mixin for unit conversion operations
# Author: [Simón Aulet]
# Date: 2025-09-10

import numpy as np
from typing import Dict, Optional, Tuple

class ConversionMixin:
    """
    Mixin for unit conversion operations of spectrum analyzer data
    """

    def convert_to_db(self) -> np.ndarray:
        """
        Convert y1 data to normalized dB scale (P - max(P))

        Returns:
        --------
        np.ndarray
            Array with values normalized to dB scale relative to maximum
            Each value is calculated as: value - max(values)

        Raises:
        -------
        ValueError
            If no data is available
        """
        if self.data is None:
            raise ValueError("No data available for conversion")

        y_data = self.data['y1']

        # Normalize data: P - max(P)
        return y_data - np.max(y_data)

    def convert_to_dBm(self) -> np.ndarray:
        """
        Convert y1 data to dBm according to units specified in the header

        Returns:
        --------
        np.ndarray
            Array with values converted to dBm

        Raises:
        -------
        ValueError
            If no data is available or the unit is not recognized
        """
        if self.data is None:
            raise ValueError("No data available for conversion")

        y_unit = self.header_data.get('y-Unit', '').upper()
        y_data = self.data['y1']

        if y_unit in ['DBM', 'dBm', 'DBM;']:
            # dBm is already in the correct scale
            return y_data.copy()
        elif y_unit in ['W', 'WATT', 'W;', 'WATT;']:
            # Convert from watts to dBm (10*log10(W/0.001))
            return 10 * np.log10(np.abs(y_data / 0.001))
        else:
            raise ValueError(f"Unit '{y_unit}' not recognized for conversion to dBm")

    def convert_to_polar(self) -> np.ndarray:
        """
        Convert X-axis data to polar coordinates (radians)

        Assumes the first X-axis data point corresponds to 0° (0 radians)
        and the last data point corresponds to 360° (2π radians), with
        linear interpolation in between.

        Returns:
        --------
        np.ndarray
            Array with X-axis values converted to radians (0 to 2π)
            for use in matplotlib polar plots

        Raises:
        -------
        ValueError
            If no data is available or the X-axis is not in time units
        """
        if self.data is None:
            raise ValueError("No data available for conversion")

        # Check current X-axis unit and handle accordingly
        x_unit = self.header_data.get('x-Unit', '').upper()
        
        if x_unit in ['S', 'S;']:
            # Time units: convert from time to polar coordinates
            x_data = self.data['x']
            n_points = len(x_data)
            # Create array of angles in radians (0 to 2π)
            # First point corresponds to 0°, last to 360° (2π radians)
            angles_radians = np.linspace(0, 2 * np.pi, n_points)
        elif x_unit in ['DEG', 'DEG;']:
            # Already in degrees: convert degrees to radians
            x_data = self.data['x']
            angles_radians = np.deg2rad(x_data)
        else:
            raise ValueError(f"X-axis must be in seconds or degrees for polar conversion, but has unit '{x_unit}'")

        return angles_radians

    def convert_to_degree(self, min_deg: float = 0.0, max_deg: float = 360.0) -> np.ndarray:
        """
        Convert X-axis data to degree scale with specified range
        
        Converts the time-based X-axis to degrees, useful for antenna pattern measurements
        where time corresponds to angular position.
        
        Parameters:
        -----------
        min_deg : float, optional
            Minimum degree value (default: 0.0)
        max_deg : float, optional
            Maximum degree value (default: 360.0)

            
        Returns:
        --------
        np.ndarray
            Array with X-axis values converted to degrees
            
        Raises:
        -------
        ValueError
            If no data is available or the X-axis is not in time units
        """
        if self.data is None:
            raise ValueError("No data available for conversion")
    
        # Verify that the X-axis is in time units
        x_unit = self.header_data.get('x-Unit', '').upper()
        if x_unit not in ['S', 'S;']:
            raise ValueError(f"X-axis must be in seconds for degree conversion, but has unit '{x_unit}'")
    
        x_data = self.data['x']
        n_points = len(x_data)
    
        # Create array of angles in degrees with specified range
        # First point corresponds to min_deg, last to max_deg
        angles_degrees = np.linspace(min_deg, max_deg, n_points)
        

    
        return angles_degrees
