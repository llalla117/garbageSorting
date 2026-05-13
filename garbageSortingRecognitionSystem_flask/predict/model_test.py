# -*- coding: utf-8 -*-
# @Time : 2024-12-2024/12/9 16:23
# @Author : 林枫
# @File : model_test.py

import logging
from datetime import datetime
import torch
import torchvision.transforms as transforms
import torch.utils.data as Data
from torchvision.datasets import ImageFolder
from predict.model_choose import ModelChoose, TrainingConfig


class ModelTest:
    def __init__(self, config: TrainingConfig, logger, model):
        """
        初始化测试器类
        :param config: 训练配置
        :param logger: 日志记录器
        :param model: 要测试的模型
        """
        self.config = config
        self.logger = logger if logger else logging.getLogger(__name__)
        self.model = model
        self.classes = ['其他垃圾/塑料袋', '其他垃圾/烟蒂', '其他垃圾/碎瓷片', '厨余垃圾/剩菜', '厨余垃圾/水果',
                        '厨余垃圾/蔬菜', '厨余垃圾/鸡蛋壳', '可回收垃圾/塑料瓶', '可回收垃圾/易拉罐', '可回收垃圾/纸箱',
                        '有害垃圾/电池', '有害垃圾/药膏', '有害垃圾/过期药品']

    def _get_data_loaders(self):
        """数据预处理，加载测试数据集"""
        # 定义数据集处理方法变量
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.18473272612791913, 0.17158856824516447, 0.15018492073688558],
                                 [0.06782158567666746, 0.061543981543858484, 0.05524772929753039]),  # 归一化处理
            transforms.Resize((224, 224))  # 调整图像大小
        ])
        # 加载数据集
        data = ImageFolder(self.config.test_data_path, transform=transform)
        test_dataloader = Data.DataLoader(dataset=data, batch_size=self.config.batch_size, shuffle=True, num_workers=0)
        return test_dataloader

    def test(self):
        """测试模型，计算准确率并通过yield返回日志"""
        # 测试开始日志
        self.logger.info('开始模型测试')

        test_dataloader = self._get_data_loaders()
        test_corrects = 0.0
        test_num = 0
        incorrect_predictions = []

        with torch.no_grad():
            self.model.eval()  # 设置模型为评估模式
            for test_data_x, test_data_y in test_dataloader:
                test_data_x = test_data_x.to(self.config.device)  # 特征放入到测试设备中
                test_data_y = test_data_y.to(self.config.device)  # 标签放入到测试设备中

                output = self.model(test_data_x)  # 前向传播过程
                pre_lab = torch.argmax(output, dim=1)  # 预测标签
                test_corrects += torch.sum(pre_lab == test_data_y.data).item()  # 更新正确预测数量
                test_num += test_data_x.size(0)  # 更新测试样本总数

                # 收集预测失败的信息
                for i in range(test_data_x.size(0)):
                    if pre_lab[i] != test_data_y[i]:  # 仅当预测失败时记录
                        incorrect_info = {
                            'predicted': self.classes[pre_lab[i].item()],
                            'actual': self.classes[test_data_y[i].item()]
                        }
                        incorrect_predictions.append(incorrect_info)
                        message = '预测值为：' + incorrect_info['predicted'] + ' 实际值为：' + incorrect_info['actual']
                        self.logger.info(message)

        test_acc = test_corrects / test_num  # 计算测试准确率
        message = f"模型测试完成!准确率为：{test_acc:.2%}，总样本为：{test_num}，正确预测个数：{test_corrects}，错误预测个数：{len(incorrect_predictions)}"
        self.logger.info(message)

    def _log_message(self, log_type: str, message: str, **kwargs):
        """
        辅助方法，统一生成日志消息
        :param log_type: 日志类型
        :param message: 日志信息
        :param kwargs: 额外参数
        :return: 日志字典
        """
        log_data = {
            'log_type': log_type,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        log_data.update(kwargs)
        return log_data


if __name__ == '__main__':
    """
        主程序入口
    """
    config = TrainingConfig(model_name='ResNet',
                            pretrained_weights='../weights/ResNet/ResNet_model_92.40%.pth')  # 配置训练参数
    model_choose = ModelChoose(config)  # 初始化模型选择器
    model = model_choose.initialize_model()  # 初始化模型
    tester = ModelTest(config, model_choose.logger, model)  # 创建测试器并开始测试
    tester.test()