import cv2 
import numpy as np
import glob
from collections import deque
from tqdm import tqdm

class topict:
    def __init__(self,original_path,pallete_path,ratio) -> None:
        self.original_image_path=original_path
        self.pallete_path=pallete_path
        self.original_image=None
        self.pallete_paths=None
        self.pallete=None
        self.original_image_data=None
        self.changed_image_data=None
        self.image_ratio=ratio
        self._init_image()
        # print(f"image size : {self.original_image_data.shape[0]}x{self.original_image_data.shape[1]}")
        # self._create_pallete()
        pass
    
    def _init_image(self):
        img=cv2.imread(self.original_image_path)
        img=cv2.resize(img,None,None,self.image_ratio,self.image_ratio,cv2.INTER_NEAREST)
        self.original_image=img
        print(img)
        print(list(img))
        print(deque(img))
        # self.original_image_data


chenger=topict("download2.jpeg","colors",1)