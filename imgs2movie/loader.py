import os
import sys
from typing import Union, List, Optional
from pathlib import Path
import glob

def load_img_paths(dir:Union[str, Path], fmts:Optional[List[str]]=None) -> List[Path]:
    dirpath = Path(dir)
    assert dirpath.exists()

    if fmts is None:
        fmts = [".jpg", ".png"]
    
    paths = [Path(p) for p in glob.glob(f"{dir}/*")]
    
    img_paths = []
    for path in paths:
        if path.suffix.lower() in fmts:
            img_paths.append(path)

    return img_paths
