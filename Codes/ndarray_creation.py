import cv2 as cv
import pandas as pd
import numpy as np
from PIL import Image

from analysis_helper import get_path


# Metadata information
data = pd.read_csv('Tables/metadata.csv')
data.head()

df_rgb = pd.DataFrame(columns=[])

# for all images
for i in range(data.shape[0]):
    img_path = get_path(data, i) # get the i'th image from metada
    img = cv.imread(img_path, 1) # colorful image
    