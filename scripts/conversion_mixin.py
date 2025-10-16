# ConversionMixin - Mixin for unit conversion operations
# Author: [Simón Aulet]
# Date: 2025-09-10

import numpy as np
from typing import Dict, Optional

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
        
        if y_unit == 'DBM':
            # dBm is already in the correct scale
            return y_data.copy()
        elif y_unit == 'W' or y_unit == 'WATT':
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
    
        # Verify that the X-axis is in time units
        x_unit = self.header_data.get('x-Unit', '').upper()
        if x_unit != 'S':
            raise ValueError(f"X-axis must be in seconds for polar conversion, but has unit '{x_unit}'")
    
        x_data = self.data['x']
        n_points = len(x_data)
    
        # Create array of angles in radians (0 to 2π)
        # First point corresponds to 0°, last to 360° (2π radians)
        angles_radians = np.linspace(0, 2 * np.pi, n_points)
    
        return angles_radians