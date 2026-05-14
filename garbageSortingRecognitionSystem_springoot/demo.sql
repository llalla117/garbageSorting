/*
 Navicat Premium Data Transfer

 Source Server         : 林枫
 Source Server Type    : MySQL
 Source Server Version : 90000 (9.0.0)
 Source Host           : localhost:3306
 Source Schema         : demo

 Target Server Type    : MySQL
 Target Server Version : 90000 (9.0.0)
 File Encoding         : 65001

 Date: 11/12/2024 19:13:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for records
-- ----------------------------
DROP TABLE IF EXISTS `records`;
CREATE TABLE `records`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `confidence` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `total_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `model_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `weights` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of records
-- ----------------------------
INSERT INTO `records` VALUES (18, 'http://localhost:9999/files/80c4bfdf0a4f4c4c81f8e328331a599e', '厨余垃圾/蔬菜', '99.87%', '0.026秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-10 23:45:14');
INSERT INTO `records` VALUES (19, 'http://localhost:9999/files/e0e54c145090468a9a06ee8e9742ab47', '其他垃圾/塑料袋', '94.33%', '0.610秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:14:37');
INSERT INTO `records` VALUES (20, 'http://localhost:9999/files/2c4e326d1a454993a11e1074faa4d7eb', '其他垃圾/烟蒂', '99.97%', '0.043秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:14:56');
INSERT INTO `records` VALUES (21, 'http://localhost:9999/files/80e76ad924a441b8958bf2c052c8a7e1', '其他垃圾/碎瓷片', '86.69%', '0.048秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:15:07');
INSERT INTO `records` VALUES (22, 'http://localhost:9999/files/cf9847e59a8c4ab180baeeae35d4ded5', '厨余垃圾/剩菜', '99.23%', '0.037秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:15:37');
INSERT INTO `records` VALUES (23, 'http://localhost:9999/files/f50914e6f5ba429dba671f401ea85f03', '厨余垃圾/水果', '98.00%', '0.052秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:15:53');
INSERT INTO `records` VALUES (24, 'http://localhost:9999/files/2e7e6e3945194e7391cca2dd7f9d061c', '厨余垃圾/蔬菜', '99.87%', '0.042秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:16:03');
INSERT INTO `records` VALUES (25, 'http://localhost:9999/files/11c8ca410e01437688d82c806c6bf5c3', '厨余垃圾/鸡蛋壳', '99.29%', '0.033秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:16:15');
INSERT INTO `records` VALUES (26, 'http://localhost:9999/files/446418c141dd4c88aeeafdaad5da4328', '可回收垃圾/易拉罐', '97.44%', '0.025秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:16:29');
INSERT INTO `records` VALUES (27, 'http://localhost:9999/files/523ca7bb94ef4fdd95f8d425f7996f51', '可回收垃圾/纸箱', '99.70%', '0.046秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:16:39');
INSERT INTO `records` VALUES (28, 'http://localhost:9999/files/5caf068590414502bd6c0931055dd355', '可回收垃圾/塑料瓶', '97.37%', '0.046秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:16:54');
INSERT INTO `records` VALUES (29, 'http://localhost:9999/files/be3bdd2c84d34f999731ca13bee10499', '有害垃圾/电池', '99.19%', '0.025秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:17:11');
INSERT INTO `records` VALUES (30, 'http://localhost:9999/files/db3244a8d47c4eb2953b5d6481e88143', '有害垃圾/药膏', '98.53%', '0.034秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:17:27');
INSERT INTO `records` VALUES (31, 'http://localhost:9999/files/52ae7574386a4416a1fd9eaf3b65e3ee', '有害垃圾/过期药品', '99.56%', '0.044秒', 'ResNet', 'ResNet_model_92.40%.pth', 'admin', '2024-12-11 17:17:42');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sex` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'Table \'.\\demo\\user\' is marked as crashed and should be repaired' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', 'admin', '张三', '男', '123@qq.com', '1234567889', 'admin', 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif');
INSERT INTO `user` VALUES (2, '123', '123', '张三', '男', '123@qq.com', '1234567889', 'common', 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif');

SET FOREIGN_KEY_CHECKS = 1;
