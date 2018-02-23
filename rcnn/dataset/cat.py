try:
    import cPickle as pickle
except ImportError:
    import pickle
import cv2
import os
import numpy as np

from ..logger import logger
from .imdb import IMDB
from .ds_utils import unique_boxes, filter_small_boxes
import json

class Cat(IMDB):
    def __init__(self, image_set, root_path, data_path):
        """
        fill basic information to initialize imdb
        :param image_set: 2007_trainval, 2007_test, etc
        :param root_path: 'selective_search_data' and 'cache'
        :param devkit_path: data and results
        :return: imdb object
        """
        super(Cat, self).__init__("cat", image_set, root_path, data_path)  # set self.name
        self.root_path = root_path
        self.data_path = data_path

        self.classes = ['__background__',  "cat"]
        self.num_classes = len(self.classes)
        self.image_set_index = self.load_image_set_index()
        self.num_images = len(self.image_set_index)
        logger.info('%s num_images %d' % (self.name, self.num_images))

        self.config = {'comp_id': 'comp4',
                       'use_diff': False,
                       'min_size': 2}


    def load_image_set_index(self):
        """
        find out which indexes correspond to given image set (train or val)
        :return:
        """
        image_set_index_file = os.path.join(self.data_path, 'index.txt')
        assert os.path.exists(image_set_index_file), 'Path does not exist: {}'.format(image_set_index_file)
        with open(image_set_index_file) as f:
            image_set_index = [x.strip() for x in f.readlines()]
        
        return image_set_index

    def image_path_from_index(self, index):
        """
        given image index, find out full path
        :param index: index of a specific image
        :return: full path of this image
        """
        image_file = os.path.join(self.data_path, index + '.jpg')
        assert os.path.exists(image_file), 'Path does not exist: {}'.format(image_file)
        return image_file

    def gt_roidb(self):
        """
        return ground truth image regions database
        :return: imdb[image_index]['boxes', 'gt_classes', 'gt_overlaps', 'flipped']
        """
        def load_roi(key, gt_f):
            objs = gt_f[key]
            roi_rec = dict()
            roi_rec['image'] = self.image_path_from_index(index)
            size = cv2.imread(roi_rec['image']).shape
            roi_rec['height'] = size[0]
            roi_rec['width'] = size[1]
            num_objs = len(objs)
            boxes = np.zeros((num_objs, 4), dtype=np.uint16)
            gt_classes = np.zeros((num_objs), dtype=np.int32)
            overlaps = np.zeros((num_objs, self.num_classes), dtype=np.float32)
            for ix, bbox in enumerate(objs):
                cx, cy, w, h = bbox
                [x1, y1] = (cx-w/2+1,cy-h/2+1)
                [x2, y2] = (cx+w/2+1,cy+h/2+1)
                cls = 1 # cuz there is only cat
                boxes[ix, :] = [x1, y1, x2, y2]
                gt_classes[ix] = cls
                overlaps[ix, cls] = 1.0
            roi_rec.update({'boxes': boxes,
                            'gt_classes': gt_classes,
                            'gt_overlaps': overlaps,
                            'max_classes': overlaps.argmax(axis=1),
                            'max_overlaps': overlaps.max(axis=1),
                            'flipped': False})
            return roi_rec

        cache_file = os.path.join(self.data_path, "annotation.json")
        assert os.path.exists(cache_file), "wrong GT path"
        with open(cache_file, "r") as f:
            gt = json.load(f)
        gt_roidb = [load_roi(index, gt) for index in self.image_set_index]
        return gt_roidb



if __name__ == "__main__":
    cat = Cat("Cat", "rcnn/dataset/cat/", "rcnn/dataset/cat/")
    catlist = cat.load_image_set_index()
    for idx in catlist:
        cat.image_path_from_index(idx)
        # print idx
    print "Done with image reading"
    roidb = cat.gt_roidb()
    print "Done with roidb"