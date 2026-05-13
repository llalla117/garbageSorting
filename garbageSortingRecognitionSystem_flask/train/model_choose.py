# -*- coding: utf-8 -*-
# @Time : 2024-12-2024/12/7 22:08
# @Author : 林枫
# @File : model_choose.py

import os
import logging
import torch
from typing import Optional, Dict, Callable

# 导入各种模型
from model.DenseNet import densenet201
from model.EfficientNet import efficientnet_b7
from model.GoogLeNet import GoogLeNet
from model.LeNet import LeNet
from model.MobileNetV2 import mobilenet_v2
from model.MobileNetV3 import mobilenet_v3_large
from model.ResNet import resnet50
from model.AlexNet import AlexNet
from model.ShuffleNetV2 import shufflenet_v2_x2_0
from model.VGGNet import vgg
from model.RegNet import regnet_x_32gf
from model.YOLOv8 import yolov8n, yolov8s, yolov8m, yolov8l, yolov8x


class TrainingConfig:
    """训练配置类，用于管理模型训练的基本参数"""

    def __init__(
            self,
            model_name: str = 'ResNet',
            num_epochs: int = 5,
            learning_rate: float = 0.001,
            batch_size: int = 64,
            num_classes: int = 13,
            train_data_path: str = '../data/train',
            val_data_path: str = '../data/val',
            weights_dir: str = '../weights/ResNet',
            pretrained_weights: Optional[str] = None
    ):
        # 初始化训练配置参数
        self.model_name = model_name
        self.num_epochs = num_epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.train_data_path = train_data_path
        self.val_data_path = val_data_path
        self.weights_dir = weights_dir
        self.pretrained_weights = pretrained_weights
        # 自动检测并选择可用的设备（GPU/CPU）
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ModelChoose:
    """模型选择和初始化类，支持多种深度学习模型的加载和预训练权重处理"""

    def __init__(self, config: TrainingConfig):
        """
        初始化模型选择器

        :param config: 训练配置对象
        """
        self.config = config
        self.logger = self._setup_logger()
        # 定义支持的模型映射
        self.supported_models: Dict[str, Callable] = {
            "LeNet": self._create_lenet,
            "AlexNet": self._create_alexnet,
            "GoogLeNet": self._create_googlenet,
            "VGG": self._create_vgg19,
            "ResNet": self._create_resnet50,
            "RegNet": self._create_regnetx,
            "MobileNetV2": self._create_mobilenetv2,
            "MobileNetV3": self._create_mobilenetv3,
            "DenseNet": self._create_densenet201,
            "EfficientNet": self._create_efficientnet,
            "ShuffleNetV2": self._create_shufflenetv2,
            "YOLOv8": self._create_yolov8,
        }

    def _create_model_factory(self, model_func: Callable) -> torch.nn.Module:
        """
        通用模型创建工厂方法

        :param model_func: 模型创建函数
        :return: 初始化的模型实例
        """
        return model_func(num_classes=self.config.num_classes).to(self.config.device)

    def _create_lenet(self) -> torch.nn.Module:
        return LeNet(num_classes=self.config.num_classes).to(self.config.device)

    def _create_alexnet(self) -> torch.nn.Module:
        return AlexNet(num_classes=self.config.num_classes, init_weights=True).to(self.config.device)

    def _create_googlenet(self) -> torch.nn.Module:
        return GoogLeNet(num_classes=self.config.num_classes).to(self.config.device)

    def _create_vgg19(self) -> torch.nn.Module:
        return vgg(model_name="vgg19", num_classes=self.config.num_classes, init_weights=True).to(self.config.device)

    def _create_resnet50(self) -> torch.nn.Module:
        return resnet50(num_classes=self.config.num_classes).to(self.config.device)

    def _create_regnetx(self) -> torch.nn.Module:
        return regnet_x_32gf(num_classes=self.config.num_classes).to(self.config.device)

    def _create_mobilenetv2(self) -> torch.nn.Module:
        return mobilenet_v2(num_classes=self.config.num_classes).to(self.config.device)

    def _create_mobilenetv3(self) -> torch.nn.Module:
        return mobilenet_v3_large(num_classes=self.config.num_classes).to(self.config.device)

    def _create_densenet201(self) -> torch.nn.Module:
        return densenet201(num_classes=self.config.num_classes).to(self.config.device)

    def _create_efficientnet(self) -> torch.nn.Module:
        return efficientnet_b7(num_classes=self.config.num_classes).to(self.config.device)

    def _create_shufflenetv2(self) -> torch.nn.Module:
        return shufflenet_v2_x2_0(num_classes=self.config.num_classes).to(self.config.device)

    def _create_yolov8(self) -> torch.nn.Module:
        """创建YOLOv8目标检测模型"""
        return yolov8n(nc=self.config.num_classes).to(self.config.device)

    def initialize_model(self) -> torch.nn.Module:
        """
        初始化模型并加载预训练权重
        """
        # 使用映射字典获取模型创建函数
        model_creator = self.supported_models.get(
            self.config.model_name,
            self._create_resnet50  # 默认使用ResNet50
        )
        model = model_creator()

        # 如果提供预训练权重，则加载
        if self.config.pretrained_weights and os.path.exists(self.config.pretrained_weights):
            try:
                # 加载权重并选择性更新模型参数
                state_dict = torch.load(self.config.pretrained_weights, map_location=self.config.device, weights_only=True)
                model_dict = model.state_dict()
                pretrained_dict = {
                    k: v for k, v in state_dict.items()
                    if k in model_dict and v.size() == model_dict[k].size()
                }
                model_dict.update(pretrained_dict)
                model.load_state_dict(model_dict)

                # 根据不同模型选择性冻结和解冻层
                self._selective_layer_freezing(model)

                self.logger.info(f"成功加载权重从 {self.config.pretrained_weights}")
            except Exception as e:
                self.logger.warning(f"加载权重失败: {e}")

        return model

    def _selective_layer_freezing(self, model: torch.nn.Module):
        """
        选择性冻结和解冻模型层

        :param model: 要处理的模型实例
        """
        # 定义需要特殊处理的模型及其冻结策略
        special_models = {
            'AlexNet': ('classifier', 'classifier'),
            'VGG': ('classifier', 'classifier'),
            'MobileNetV2': ('classifier', 'classifier'),
            'MobileNetV3': ('classifier', 'classifier'),
            'EfficientNet': ('classifier', 'classifier'),
            'DenseNet': ('classifier', 'classifier'),
        }

        # 获取当前模型的特殊冻结策略
        target_layer, trainable_layer = special_models.get(
            self.config.model_name,
            ('fc', 'fc')
        )

        # 冻结所有参数
        for param in model.parameters():
            param.requires_grad = False

        # 解冻特定层
        try:
            trainable_params = getattr(model, trainable_layer).parameters()
            for param in trainable_params:
                param.requires_grad = True
        except AttributeError:
            self.logger.warning(f"无法找到 {trainable_layer} 层")

    def _setup_logger(self):
        """
        设置日志记录器

        :return: 配置好的日志记录器
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger(__name__)