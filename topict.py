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
        print(f"image size : {self.original_image_data.shape[0]}x{self.original_image_data.shape[1]}")
        self._create_pallete()
        pass
    
    def _init_image(self):
        image=cv2.imread(self.original_image_path)
        image=cv2.resize(image,None, None, self.image_ratio, self.image_ratio, cv2.INTER_NEAREST)
        self.original_image=image
        self.original_image_data=np.array(image)
    
    def _create_pallete(self):
        folder=glob.glob(self.pallete_path+"/*")
        self.pallete_paths=np.array([])
        self.pallete=[]
        for f in tqdm(folder,desc="create pallete"):
            self.pallete_paths=np.append(self.pallete_paths,f)
            img=cv2.imread(f)
            img_data=np.array(img)
            img_ave=np.average(np.average(img_data,axis=1),axis=0)
            self.pallete.append(img_ave)
            pass
        self.pallete=np.array(self.pallete)

    def _kinji(self,color):
        distance=deque()
        for i in range(self.pallete.shape[0]):
            distance.append(np.sqrt((self.pallete[i][0]-color[0])**2+(self.pallete[i][1]-color[1])**2+(self.pallete[i][2]-color[2])**2))
            pass
        idx=np.array(distance)
        return np.argmin(idx)
    
    def create_data(self):
        output_data=[]
        for i in tqdm(range(self.original_image_data.shape[0]),desc="create image data"):
            output_data.append(np.array([self._kinji(self.original_image_data[i][j]) for j in range(self.original_image_data.shape[1])]))
            pass
        self.changed_image_data=np.array(output_data)
        pass
    
    def output_bynparray(self):
        return self.changed_image_data
    
    def output_byhtml(self,path,detail:bool):
        
        if detail:
            img_detail_html=f"""
            <br>
            <span>image size {self.changed_image_data.shape[0]}x{self.changed_image_data.shape[1]}</span>
            <br>
            
            """
        
        images_str=""
        for i in tqdm(range(self.changed_image_data.shape[0]),desc="preparing output"):
            images_str+="<div>"
            for j in range(self.changed_image_data.shape[1]):
                images_str+=f'<img src="{self.pallete_paths[self.changed_image_data[i][j]]}">'
            images_str+="</div>"
        with open(path,"w") as f :
            
            f.write(f"""
                    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body style="background: #4169e1;">

    {images_str}
    {img_detail_html}
    
    </body>
        </html>
                    """)
        pass



if __name__=="__main__":
    from matplotlib import pyplot as plt
    
    chenger=topict("download2.jpeg","colors",1)
    chenger.create_data()
    chenger.output_byhtml("index5.html",True)

    fig=plt.figure()
    ax=fig.add_subplot(1,1,1,projection="3d")
    for i in chenger.pallete:
        ax.scatter(i[0],i[1],i[2])
        pass
    plt.show()
    # print(chenger.changed_image_data)