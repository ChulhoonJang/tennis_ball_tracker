import cv2
import numpy as np

class ImgQueue:
    def __init__(self, maxsize = 5):
        self.items = []
        self.maxsize = maxsize

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        if self.size() == self.maxsize:
            self.dequeue()
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    def calculate_average(self):
        imgs = np.array(self.items).astype(np.float)
        return np.mean(imgs, axis = 0)
    
def clustering(img, num_pixels, aspect_ratio):
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img)
    rects = []
    if num_pixels != None and aspect_ratio != None:
        for stat in stats:
            ratio = float(stat[2])/stat[3]
            n = stat[4]

            if n >= num_pixels[0]  and n <= num_pixels[1] and ratio >= aspect_ratio[0] and ratio <= aspect_ratio[1]:
                rects.append(stat)
    else:
        rects = stats[1:,:]
            
    return rects