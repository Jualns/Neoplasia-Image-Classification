import cv2 as cv
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

from analysis_helper import get_hist

# 
dir_now = os.path.dirname(os.path.abspath("__file__"))

# dir_now/Tables/metada.csv
path_table = os.path.join(dir_now, 'Tables', 'metadata.csv')

# Metadata information
data = pd.read_csv(path_table)

num_imgs = data.shape[0]
col_names = ["id"]
col_names.extend(list(range(256)))

###########################
######## Grayscale ########
###########################

# 256(RGB scale) + 1(id)
m_gray = np.zeros((num_imgs, 256+1))

# for all images
for i in range(num_imgs):
    gray_scale = get_hist(data, i, rgb = False)
    m_gray[i,1:] = gray_scale[:]
    m_gray[i,0] = i

metada_hist_gray = pd.DataFrame(m_gray, columns=col_names, dtype=np.int64)

metada_hist_gray.to_csv("Tables/histogram_grayscale.csv", index = False)

###########################
######## RGB scale ########
###########################

# 256(RGB scale) + 1(id) + 1 (RGB name)
m_rgb = np.zeros((num_imgs,3, 256+1))

# for all images
for i in range(num_imgs):
    rgb_scale = get_hist(data, i, rgb = True) 
    m_rgb[i,0,1:] = rgb_scale[:,0] #R
    m_rgb[i,1,1:] = rgb_scale[:,1] #G
    m_rgb[i,2,1:] = rgb_scale[:,2] #B
    m_rgb[i,:,0] = i

metada_hist_r = pd.DataFrame(m_rgb[:,0,:], columns=col_names, dtype=np.int64)
metada_hist_r["Color"] = ["R"]*num_imgs

metada_hist_g = pd.DataFrame(m_rgb[:,1,:], columns=col_names, dtype=np.int64)
metada_hist_g["Color"] = ["G"]*num_imgs

metada_hist_b = pd.DataFrame(m_rgb[:,2,:], columns=col_names, dtype=np.int64)
metada_hist_b["Color"] = ["B"]*num_imgs

metada_hist_rgb = pd.concat([metada_hist_r,metada_hist_g, metada_hist_b])

metada_hist_rgb.to_csv("Tables/histogram_rgb.csv", index = False)