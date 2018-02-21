try:
    import cPickle as pickle
except ImportError:
    import pickle
import cv2
import os
import numpy as np

from ..logger import logger
from .imdb import IMDB
from .pascal_voc_eval import voc_eval
from .ds_utils import unique_boxes, filter_small_boxes


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

if __name__ == "__main__":
    cat = Cat("Cat", "rcnn/dataset/cat/", "rcnn/dataset/cat/")
    print cat