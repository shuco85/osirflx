from scipy.interpolate import splprep, splev
import numpy as np


class ZRoi:
    def __init__(self, pk=None, roi_series=None, index=None, points_px=None):
        self.pk = pk
        self.index = index
        self.roi_series = roi_series
        self.points_px = points_px

    def __str__(self):
        return(f"Primary Key: {self.pk}\n" +
               f"Index: {self.index}\n" +
               f"ROI Type: {self.roi_series if self.roi_series else 'No hay'}\n" +
               f"points_px: {self.points_px}\n")

    def get_interpolated_points(self):
        # definimos la x y la y
        x = [coords[0] for coords in self.points_px]
        y = [coords[1] for coords in self.points_px]

        # Aniadimos las coordenadas iniciales
        x = np.r_[x, x[0]]
        y = np.r_[y, y[0]]

        # https://stackoverflow.com/questions/33962717/interpolating-a-closed-curve-using-scipy
        tck, u = splprep([x, y], s=0, per=True)

        # evaluate the spline fits for 1000 evenly spaced distance values
        xi, yi = splev(np.linspace(0, 1, 1000), tck)

        return xi, yi
