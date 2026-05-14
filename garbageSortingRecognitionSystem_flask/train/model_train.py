import os
import time
import sys
import signal
from datetime import datetime
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
from train.model_choose import ModelChoose, TrainingConfig


class ModelTrainer:
    def __init__(self, config: TrainingConfig, logger, model):
        """
        初始化训练器类
        :param config: 训练配置
        :param logger: 日志记录器
        :param model: 要训练的模型
        """
        self.config = config
        self.logger = logger
        self.model = model
        # 记录最佳模型权重
        self.best_model_weights = self.model.state_dict()
        self.best_val_accuracy = 0.0
        # 模型保存路径格式
        self.model_save_path = os.path.join(
            self.config.weights_dir,
            f'{self.config.model_name}_model_{{:.2f}}%.pth'
        )
        # 控制训练是否中断的标志
        self.training_interrupted = False

    def _get_data_loaders(self):
        # 保持原有代码不变
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.18473272612791913, 0.17158856824516447, 0.15018492073688558],
                                 [0.06782158567666746, 0.061543981543858484, 0.05524772929753039]),  # 归一化处理
            transforms.Resize((224, 224))  # 统一图片大小
        ])

        train_data = ImageFolder(self.config.train_data_path, transform=transform)  # 加载训练数据
        val_data = ImageFolder(self.config.val_data_path, transform=transform)  # 加载验证数据
        # 创建数据加载器
        train_loader = DataLoader(train_data, batch_size=self.config.batch_size, shuffle=True)
        val_loader = DataLoader(val_data, batch_size=1, shuffle=True)
        return train_loader, val_loader

    def _handle_interrupt(self, signum, frame):
        """
        处理中断信号
        """
        self.logger.warning("Training interrupted by user. Saving current best model...")
        self.training_interrupted = True

    def train(self):
        """
        模型训练主逻辑
        """
        # 注册中断信号处理器
        signal.signal(signal.SIGINT, self._handle_interrupt)

        start_time = time.time()  # 记录开始时间
        train_loader, val_loader = self._get_data_loaders()  # 初始化数据加载器
        criterion = nn.CrossEntropyLoss()  # 定义损失函数
        optimizer = optim.Adam(self.model.parameters(), lr=self.config.learning_rate)  # 定义优化器

        train_metrics = {  # 初始化训练和验证的指标
            'train_loss': [], 'val_loss': [],
            'train_accuracy': [], 'val_accuracy': []
        }

        if self.config.pretrained_weights:
            self.logger.info(f"已加载预训练权重： {self.config.pretrained_weights}")

        self.logger.info(f"Starting training for {self.config.num_epochs} epochs")

        try:
            for epoch in range(self.config.num_epochs):
                if self.training_interrupted:
                    break

                epoch_start_time = time.time()  # 记录当前轮次开始时间
                epoch_log = f"{'=' * 25}Epoch {epoch + 1}/{self.config.num_epochs}{'=' * 25}"
                self.logger.info(epoch_log)

                # 训练过程
                self.model.train()  # 切换为训练模式
                total_train_loss, total_train_correct, total_train_samples = 0, 0, 0

                for batch_idx, (batch_x, batch_y) in enumerate(train_loader):
                    if self.training_interrupted:
                        break

                    batch_x, batch_y = batch_x.to(self.config.device), batch_y.to(self.config.device)
                    optimizer.zero_grad()
                    outputs = self.model(batch_x)
                    if isinstance(outputs, tuple):
                        main_output = outputs[0]  # 主输出在第一个位置
                        loss = criterion(main_output, batch_y)
                    elif hasattr(outputs, 'logits'):
                        loss = criterion(outputs.logits, batch_y)
                    else:
                        loss = criterion(outputs, batch_y)

                    loss.backward()
                    optimizer.step()

                    total_train_loss += loss.item() * batch_x.size(0)
                    total_train_correct += (outputs.argmax(1) == batch_y).sum().item()
                    total_train_samples += batch_x.size(0)
                    # 实时进度条
                    progress = (batch_idx + 1) / len(train_loader) * 100
                    self._display_progress('Train', progress)

                if self.training_interrupted:
                    break

                train_loss = total_train_loss / total_train_samples if total_train_samples > 0 else 0
                train_accuracy = total_train_correct / total_train_samples if total_train_samples > 0 else 0

                # 验证过程
                self.model.eval()  # 切换为评估模式
                total_val_loss, total_val_correct, total_val_samples = 0, 0, 0

                with torch.no_grad():
                    for batch_idx, (batch_x, batch_y) in enumerate(val_loader):
                        if self.training_interrupted:
                            break

                        batch_x, batch_y = batch_x.to(self.config.device), batch_y.to(self.config.device)
                        outputs = self.model(batch_x)
                        loss = criterion(outputs, batch_y)

                        total_val_loss += loss.item() * batch_x.size(0)
                        total_val_correct += (outputs.argmax(1) == batch_y).sum().item()
                        total_val_samples += batch_x.size(0)
                        # 实时进度条
                        progress = (batch_idx + 1) / len(val_loader) * 100
                        self._display_progress('Validation', progress)

                    if self.training_interrupted:
                        break

                val_loss = total_val_loss / total_val_samples if total_val_samples > 0 else 0
                val_accuracy = total_val_correct / total_val_samples if total_val_samples > 0 else 0

                # 如果验证准确率更高，更新最佳模型
                if val_accuracy > self.best_val_accuracy:
                    self.best_val_accuracy = val_accuracy
                    self.best_model_weights = self.model.state_dict()

                # 记录指标
                train_metrics['train_loss'].append(train_loss)
                train_metrics['val_loss'].append(val_loss)
                train_metrics['train_accuracy'].append(train_accuracy)
                train_metrics['val_accuracy'].append(val_accuracy)

                epoch_duration = time.time() - epoch_start_time  # 计算本轮耗时
                log_summary = (f"Epoch Summary: "
                               f"Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, "
                               f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.4f}, "
                               f"Epoch Duration: {epoch_duration:.2f} seconds")
                self.logger.info(log_summary)

                if self.training_interrupted:
                    break

        except Exception as e:
            self.logger.error(f"Training interrupted due to an error: {e}")
            self.training_interrupted = True

        finally:
            if self.training_interrupted:
                self.logger.warning("Training was interrupted. Saving best model so far...")

            self._save_best_model()  # 在训练结束或异常时保存最佳模型

            total_time = time.time() - start_time
            final_status = "Interrupted" if self.training_interrupted else "Completed"
            self.logger.info(f"Training {final_status}. Total Time: {total_time:.2f} seconds")

            if not self.training_interrupted:
                self._plot_training_results(train_metrics)

    def _save_best_model(self):
        """
        保存最佳模型
        """
        os.makedirs(self.config.weights_dir, exist_ok=True)
        save_path = self.model_save_path.format(self.best_val_accuracy * 100)
        torch.save(self.best_model_weights, save_path)
        self.logger.info(f"Best model saved to {save_path}")

    @staticmethod
    def _plot_training_results(train_metrics):
        """
        绘制训练结果曲线
        :param train_metrics: 训练和验证指标
        """
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.title('Loss Curves')
        plt.plot(train_metrics['train_loss'], label='Train Loss')
        plt.plot(train_metrics['val_loss'], label='Val Loss')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.title('Accuracy Curves')
        plt.plot(train_metrics['train_accuracy'], label='Train Accuracy')
        plt.plot(train_metrics['val_accuracy'], label='Val Accuracy')
        plt.legend()

        plt.tight_layout()
        plt.show()

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

    def _display_progress(self, stage: str, progress: float):
        """显示训练/验证进度"""
        status_bar = f"{stage} Progress: [{'=' * int(progress / 5)}{'>' if progress < 100 else ''}{'.' * (20 - int(progress / 5))}] {progress:.2f}%"
        print(f"\r{status_bar}", end='', flush=True)
        if progress >= 100:
            print()  #


if __name__ == '__main__':
    """
    主程序入口
    """
    config = TrainingConfig(
        model_name='LeNet',
        num_epochs=10,
        weights_dir='../weights/LeNet',
        pretrained_weights='../weights/LeNet/LeNet_model_21.42%.pth')  # 配置训练参数
    model_choose = ModelChoose(config)  # 初始化模型选择器
    model = model_choose.initialize_model()  # 初始化模型
    trainer = ModelTrainer(config, model_choose.logger, model)  # 创建训练器并开始训练
    trainer.train()