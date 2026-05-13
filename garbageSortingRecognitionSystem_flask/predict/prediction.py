# -*- coding: utf-8 -*-
# @Time : 2024-12-09 17:08
# @Author : 林枫
# @File : prediction.py

import logging
import json
import time
from io import BytesIO

import requests
import torch
import torchvision.transforms as transforms
from PIL import Image
from predict.model_choose import ModelChoose, TrainingConfig


class Prediction:
    def __init__(self, config: TrainingConfig, logger=None, model=None):
        """
        初始化预测类
        :param config: 训练配置
        :param logger: 日志记录器
        :param model: 要测试的模型
        """
        self.config = config
        self.logger = logger
        self.model = model
        self.classes = [
            '其他垃圾/塑料袋', '其他垃圾/烟蒂', '其他垃圾/碎瓷片',
            '厨余垃圾/剩菜', '厨余垃圾/水果', '厨余垃圾/蔬菜', '厨余垃圾/鸡蛋壳',
            '可回收垃圾/塑料瓶', '可回收垃圾/易拉罐', '可回收垃圾/纸箱',
            '有害垃圾/电池', '有害垃圾/药膏', '有害垃圾/过期药品'
        ]
        if self.model is None:
            raise ValueError("模型未初始化，请提供有效的模型实例。")

    def preprocess_image(self):
        """
        图像预处理，适配模型输入
        :return: 预处理后的图像张量
        """
        try:
            # 从URL获取图像
            response = requests.get(self.config.image_path)
            response.raise_for_status()  # 检查请求是否成功
            image = Image.open(BytesIO(response.content)).convert('RGB')  # 转为RGB图像
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.1847, 0.1716, 0.1502],
                    std=[0.0678, 0.0615, 0.0552]
                )
            ])
            return transform(image).unsqueeze(0)  # 增加批次维度
        except Exception as e:
            self.logger.error(f"图像处理失败: {e}")
            raise ValueError(f"图像处理失败: {e}")

    def predict(self, image_tensor):
        """
        使用模型对图像进行预测
        :param image_tensor: 图像张量
        :return: 预测类别及置信度
        """
        try:
            self.model.eval()
            with torch.no_grad():
                image_tensor = image_tensor.to(self.config.device)
                output = self.model(image_tensor)
                _, predicted_idx = torch.max(output, dim=1)
                confidence = torch.softmax(output, dim=1)[0, predicted_idx].item()
                return self.classes[predicted_idx.item()], confidence
        except Exception as e:
            self.logger.error(f"预测失败: {e}")
            raise ValueError(f"预测失败: {e}")

    def run(self):
        """
        执行预测并返回结果
        :return: JSON格式结果
        """
        try:
            start_time = time.time()
            image_tensor = self.preprocess_image()
            prediction, confidence = self.predict(image_tensor)
            total_time = time.time() - start_time

            result = {
                "status": 200,
                "message": "预测成功",
                "prediction": prediction,
                "confidence": f"{confidence*100:.2f}%",
                "total_time": f"{total_time:.3f}秒"
            }
            self.logger.info(f"预测完成: {result}")
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            error_response = {
                "status": 400,
                "message": f"出错: {str(e)}"
            }
            self.logger.error(f"预测失败: {error_response}")
            return json.dumps(error_response, ensure_ascii=False)


def main():
    """
    主程序入口
    """

    try:
        config = TrainingConfig(
            model_name='ResNet50',
            num_classes=13,
            image_path='../test.jpg',
            pretrained_weights='../weights/ResNet/ResNet50_model_89.46%.pth'
        )
        model_choose = ModelChoose(config)
        model = model_choose.initialize_model()

        predictor = Prediction(config, model_choose.logger, model)
        result = predictor.run()
        print(result)
    except Exception as e:
        print(f"主程序运行失败: {e}")


if __name__ == '__main__':
    main()
