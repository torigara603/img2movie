import os
from typing import Union, List, Tuple, Optional
from pathlib import Path

import numpy as np
import cv2

if __package__ is not None:
    import loader
else:
    from . import loader

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

class MP4Maker():
    def __init__(self):
        self.video_writer:Optional[cv2.VideoWriter] = None


    def set_video_writer(
            self,
            out_name:str,
            out_wsize:int,
            out_hsize:int,
            out_fps:float) -> None:
        
        video_fmt = cv2.VideoWriter_fourcc(*"mp4v")
        out_path = f"{FILE_DIR}/{out_name}.mp4"
        self.video_writer = cv2.VideoWriter(out_path, video_fmt, out_fps, (out_wsize, out_hsize))


    def write_frame(self, img:np.ndarray):
        self.video_writer.write(img)


    def release(self):
        if self.video_writer is not None:
            self.video_writer.release()
        self.video_writer = None


    def __del__(self):
        self.release()


    def make(self, imgdir:Union[str, Path], out_name:str="out", fps:float=30.0):
        # get img paths
        img_paths = loader.load_img_paths(imgdir)

        # compute most resolution
        out_wsize, out_hsize = self.compute_most_resolution(img_paths)

        # set video writer
        self.set_video_writer(out_name, out_wsize, out_hsize, fps)

        for p in img_paths:
            # load img
            img = cv2.imread(str(p))
            # write frame
            self.video_writer.write(img)
        self.release()


    def compute_most_resolution(self, img_paths:List[Path]) -> Tuple[int, int]:
        resolution_histgram = {}
        for p in img_paths:
            img = cv2.imread(str(p))
            hsize, wsize = img.shape[:2]
            if (wsize, hsize) not in resolution_histgram:
                resolution_histgram[(wsize, hsize)] = 0
            resolution_histgram[(wsize, hsize)] += 1
        assert len(resolution_histgram) > 0
        max_count = -1
        max_count_resolution = (0, 0)
        for resolution, count in resolution_histgram.items():
            if count > max_count:
                max_count = count
                max_count_resolution = resolution
        assert max_count_resolution != (0, 0)
        count_score = max_count / len(resolution_histgram)
        print(f"[Done] computed resolution! Max Resolution is {max_count_resolution}. Persentage is {count_score}")
        
        return max_count_resolution
