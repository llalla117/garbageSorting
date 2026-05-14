# -*- coding: utf-8 -*-
# @Time : 2024-09-2024/9/28 22:37
# @Author : 林枫
# @File : flaskR.py

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify

from predict.model_choose import TrainingConfig, ModelChoose
from predict.prediction import Prediction


class ImagePredictorAPI:
    def __init__(self):
        """初始化 Flask 应用和模型"""
        self.app = Flask(__name__)

        # 定义路由
        self.app.add_url_rule('/predict', 'predict', self.predict, methods=['POST'])
        self.app.add_url_rule('/file_names', 'file_names', self.file_names, methods=['GET'])

    def predict(self):
        """处理预测请求"""
        # 检查请求中是否有必要的数据
        data = request.get_json()

        if not data or 'model_name' not in data or 'weights' not in data or 'image_path' not in data:
            return jsonify({'error': 'Model name, weight path, or image not provided'}), 400

        model_name = data['model_name']
        weight_path = data['weights']
        image_path = data['image_path']

        try:
            config = TrainingConfig(
                model_name=model_name,
                image_path=image_path,
                pretrained_weights='../weights/' + model_name + '/' + weight_path
            )
            model_choose = ModelChoose(config)
            model = model_choose.initialize_model()

            predictor = Prediction(config, model_choose.logger, model)
            result = predictor.run()
            return result
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_all_file_names(self, directory):
        """获取指定目录及其子目录中的所有文件名"""
        try:
            all_files = []
            # 使用 os.walk 遍历目录及其子目录
            for root, _, files in os.walk(directory):
                for file in files:
                    # 拼接完整路径并添加到列表
                    all_files.append(file)
            return all_files
        except Exception as e:
            print(f"发生错误: {e}")
            return []

    def file_names(self):
        """测试接口"""
        model_items = [name.split('.')[0] for name in self.get_all_file_names("../model")]
        weight_items = [name for name in self.get_all_file_names("../weights")]

        # 只允许展示的模型列表
        allowed_models = ['ResNet', 'MobileNetV2', 'MobileNetV3', 'EfficientNet', 'RegNet']
        
        # 过滤模型列表，只保留允许的模型，并去重
        filtered_models = list(set([model for model in model_items if model in allowed_models]))
        filtered_models.sort()  # 保持顺序一致
        
        # 过滤权重文件，只保留允许模型对应的权重，并去重
        filtered_weights = list(set([weight for weight in weight_items if any(model in weight for model in allowed_models)]))
        filtered_weights.sort()  # 保持顺序一致

        # 转换为所需格式
        formatted_model_items = [{'value': item, 'label': item} for item in filtered_models]
        formatted_weight_items = [{'value': item, 'label': item} for item in filtered_weights]

        # 创建字典
        result = {
            'model_items': formatted_model_items,
            'weight_items': formatted_weight_items
        }

        # 转换为 JSON 字符串
        json_result = json.dumps(result, ensure_ascii=False, indent=2)
        return json_result

    def run(self, port=5000):
        """运行 Flask 应用"""
        self.app.run(port=port)


if __name__ == '__main__':
    api = ImagePredictorAPI()
    api.run()
