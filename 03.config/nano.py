#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import os

import torch.nn as nn

from yolox.exp import Exp as MyExp


class Exp(MyExp):
    def __init__(self):
        super(Exp, self).__init__()
        self.depth = 0.33
        self.width = 0.25
        self.input_size = (416, 416)
        self.mosaic_scale = (0.5, 1.5)
        self.random_size = (10, 20)
        self.test_size = (416, 416)
        self.exp_name = os.path.split(
            os.path.realpath(__file__))[1].split(".")[0]
        self.enable_mixup = False

        # Define yourself dataset path
        self.data_dir = "/content/drive/MyDrive/YOLOXTrain/dataset/images"
        self.train_ann = "/content/drive/MyDrive/YOLOXTrain/dataset/annotations/train_annotations.json"
        self.val_ann = "/content/drive/MyDrive/YOLOXTrain/dataset/annotations/validation_annotations.json"

        #要根据02.annotation_data\pascal_label_map.pbtxt中模型的数量来修改，如id: 5，则此处也要改成5
        self.num_classes = 16

        self.max_epoch = 600
        self.data_num_workers = 4
        self.eval_interval = 1

    def get_model(self, sublinear=False):
        def init_yolo(M):
            for m in M.modules():
                if isinstance(m, nn.BatchNorm2d):
                    m.eps = 1e-3
                    m.momentum = 0.03

        if "model" not in self.__dict__:
            from yolox.models import YOLOX, YOLOPAFPN, YOLOXHead
            in_channels = [256, 512, 1024]
            # NANO model use depthwise = True, which is main difference.
            backbone = YOLOPAFPN(self.depth,
                                 self.width,
                                 in_channels=in_channels,
                                 depthwise=True)
            head = YOLOXHead(self.num_classes,
                             self.width,
                             in_channels=in_channels,
                             depthwise=True)
            self.model = YOLOX(backbone, head)

        self.model.apply(init_yolo)
        self.model.head.initialize_biases(1e-2)
        return self.model
