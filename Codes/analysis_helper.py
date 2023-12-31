import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def get_hist_df(df, id_img):
    if "Color" in df.columns:
        return np.array(df[df["id"] == id_img].drop(["id", "Color"], axis = 1).transpose())
    return np.array(df[df["id"] == id_img].drop(["id"], axis = 1).transpose())

def get_path(data, i):
    """
    Returns the full path to an image using DataFrame information.
    
    Args:
        data (DataFrame): DataFrame containing image information.
        i (int): Index of the image in the DataFrame.

    Returns:
        str: Full path to the image.
    """
    img_path = data['Path'][i] + data['Name'][i]
    return img_path

def get_hist(data, i, rgb = False, bins = 256):
    # get the path
    img_path = get_path(data, i)
    if rgb:
        color = ('b', 'g', 'r')
        img = cv.imread(img_path, 1)
        hist_colors = np.zeros((256,3), dtype=np.int64)
        for j, col in enumerate(color):
            histr = cv.calcHist([img], [j], None, [bins], [0, 256])
            hist_colors[:,j] = histr.transpose()
        return hist_colors
    img = cv.imread(img_path, 0)
    hist, bins = np.histogram(img.ravel(), bins=bins, range=[0, 256])
    return hist

def get_image_info(image_path):
    try:
        with Image.open(image_path) as img:
            img_bytes = os.path.getsize(image_path)
            img_size = img.size
            return img_bytes, img_size
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None

def plot_hist_rgb(data, space):
    """
    Plots the histogram of each color channel (RGB) of an image.

    Args:
        data (DataFrame): DataFrame containing image information.
        space (list): List of image indices in the DataFrame to be processed.
    """
    color = ('b', 'g', 'r')
    for i in space:
        img_path = get_path(data, i)
        img = cv.imread(img_path, 1)
        for j, col in enumerate(color):
            histr = cv.calcHist([img], [j], None, [256], [0, 256])
            plt.plot(histr, color=col)
            plt.xlim([0, 256])
        plt.show()

def plot_hist(data, space):
    """
    Plots the grayscale histogram of an image.

    Args:
        data (DataFrame): DataFrame containing image information.
        space (list): List of image indices in the DataFrame to be processed.
    """
    for i in space:
        img_path = get_path(data, i)
        img = cv.imread(img_path, 0)
        plt.hist(img.ravel(), 256, [0, 256])
        plt.show()

def show_image(title, image):
    """
    Saves an image and displays it.

    Args:
        title (str): Title to save the image.
        image (array): Image array to be saved and displayed.

    Returns:
        Image: Image loaded using the Pillow library.
    """
    cv.imwrite(title, image)
    im = Image.open(title)
    return im
