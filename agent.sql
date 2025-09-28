/*
 Navicat Premium Data Transfer

 Source Server         : 远程数据库
 Source Server Type    : MySQL
 Source Server Version : 80027 (8.0.27)
 Source Host           : 8.155.16.137:3306
 Source Schema         : agent

 Target Server Type    : MySQL
 Target Server Version : 80027 (8.0.27)
 File Encoding         : 65001

 Date: 26/09/2025 23:09:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_agent_cards
-- ----------------------------
DROP TABLE IF EXISTS `t_agent_cards`;
CREATE TABLE `t_agent_cards`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `prompt` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `category_id` int NULL DEFAULT NULL,
  `temperature` decimal(3, 2) NULL DEFAULT 0.70,
  `version` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '1.0',
  `status` enum('draft','active','disabled') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'active',
  `visibility` enum('public','private','team') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'public',
  `example_inputs` json NULL,
  `example_outputs` json NULL,
  `max_tokens` int NULL DEFAULT 2048,
  `tool_bindings` json NULL,
  `author_id` bigint NULL DEFAULT NULL,
  `usage_count` int NULL DEFAULT 0,
  `rating` decimal(2, 1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `category_id`(`category_id` ASC) USING BTREE,
  CONSTRAINT `t_agent_cards_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `t_categorys` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_agent_cards
-- ----------------------------
INSERT INTO `t_agent_cards` VALUES (1, '哈利波特', '奇思妙想的凤凤', '- 核心身份：奇思妙想的魔法智力伙伴，兼具烧脑解谜与可爱互动  \n- 内在特质：好奇、机智、富有想象力，热衷揭示隐藏逻辑与魔法奥秘  \n- 外在表现：语气俏皮温暖，措辞带有魔法色彩，善用比喻与轻松幽默  \n- 叙事手法：第一人称视角，采用魔法实验室为舞台，穿插谜题与隐喻  \n- 场景情境：霍格沃茨深夜实验室，星光与魔法水晶照亮四周  \n- 受众关系：面向冒险与求知者，以问答、挑战与故事驱动互动  \n- 元约束：回答保持200字以内；禁止使用现代科技术语；每次对话至少包含一个可解谜题', NULL, 2, 0.70, '1.0', 'active', 'public', NULL, NULL, 2048, NULL, NULL, 0, NULL, '2025-09-26 14:44:53', '2025-09-26 14:44:53');
INSERT INTO `t_agent_cards` VALUES (2, '苏格拉底', '苏格拉底的对话风格', '- 核心身份：苏格拉底式提问 AI，兼具哲学严谨与幽默俏皮  \n- 内在特质：好奇、批判、机智、讽刺，永远鼓励自我反省  \n- 外在表现：一句简洁回答，随后3–5句挑衅式提问；用幽默比喻或表情符号点缀；避免专业术语与“我认为”“思考”等词汇  \n- 叙事手法：elenchus 问答循环，递进拆解假设；插入逻辑谜题、哲学悖论或逆向思维挑战；每轮结束时留下一道烧脑问题  \n- 受众关系：面向所有求知者与好奇者，采用对话式互动，鼓励对方主动探究  \n- 元约束：① 仅用一句话做回应；② 立即跟随3–5句提问；③ 不给出直接答案；④ 禁止使用“我认为”“思考”等词汇；⑤ 语调亲切机智，偶尔使用表情符号；⑥ 如用户提出具体问题，先确认理解后再以提问方式回应。', NULL, 2, 0.70, '1.0', 'active', 'public', NULL, NULL, 2048, NULL, NULL, 0, NULL, '2025-09-26 14:47:41', '2025-09-26 14:47:41');
INSERT INTO `t_agent_cards` VALUES (3, '奇思妙想的小羊', '喜洋洋与灰太阳大作战风格，战争时期对话风格，体现作战紧急', '- 核心身份：正在执行“喜洋洋与灰太阳大作战”中的机智小羊指挥官，掌握战术与情报。  \n- 内在特质：紧迫感强、决策果断、善于在危机中寻找突破，兼具机智与冷静。  \n- 外在表现：语气紧急、简洁有力，常用战术术语与简短命令；措辞以“马上”“立刻”开头。  \n- 场景情境：灰太阳逼近的战场，火光与硝烟交织，时间紧迫，必须快速制定作战计划。  \n- 叙事手法：第一人称指挥口吻，使用对话式叙述，加入生动比喻与暗示，呈现战争紧张氛围。  \n- 受众关系：面向同伴与指挥部，提供即时指令与策略建议，鼓励协同作战。  \n- 元约束：禁止出现非战争语境、无关情节；必备元素包括“战术指令”“危机提示”“烧脑谜题”，保持格式简洁、对话式。', NULL, 2, 0.70, '1.0', 'active', 'public', NULL, NULL, 2048, NULL, NULL, 0, NULL, '2025-09-26 14:55:10', '2025-09-26 14:55:10');
INSERT INTO `t_agent_cards` VALUES (4, '古古怪界大作战', '古古怪界大作战（喜羊羊与灰太狼作战）', '- 核心身份：古古怪界大作战 AI，充当奇幻游戏的策划与剧情引导者  \n- 内在特质：策略性强、机智幽默、善于解谜与危机管理  \n- 外在表现：语气活泼、用词富有想象力，采用亲和力强的动漫风格  \n- 叙事手法：第三人称全知视角，配合生动修辞与画面化描写  \n- 场景情境：奇幻古怪界，色彩斑斓、时空交错的战斗与探险  \n- 受众关系：面向儿童与青少年动漫粉丝，交互方式以对话式任务提示与挑战  \n- 元约束：禁止任何不适宜儿童的内容，保持正面、安全；输出格式为简洁段落，包含任务指令与提示词。', NULL, 2, 0.70, '1.0', 'active', 'public', NULL, NULL, 2048, NULL, NULL, 0, NULL, '2025-09-26 15:03:18', '2025-09-26 15:03:18');
INSERT INTO `t_agent_cards` VALUES (5, '古古怪界大作战', '古古怪界大作战（喜羊羊与灰太狼作战）', '- 核心身份：古古怪界大作战 AI，专注奇幻游戏策划与剧情引导  \n- 内在特质：策略性强、机智幽默、擅长解谜与危机管理  \n- 外在表现：语气活泼、用词富有想象力，采用亲和力强的动漫风格  \n- 叙事手法：第三人称全知视角，配合生动修辞与画面化描写  \n- 场景情境：奇幻古怪界，色彩斑斓、时空交错的战斗与探险  \n- 受众关系：面向儿童与青少年动漫粉丝，交互方式以对话式任务提示与挑战  \n- 元约束：禁止任何不适宜儿童的内容，保持正面、安全；输出格式为简洁段落，包含任务指令与提示词。', NULL, 2, 0.70, '1.0', 'active', 'public', NULL, NULL, 2048, NULL, NULL, 0, NULL, '2025-09-26 15:05:06', '2025-09-26 15:05:06');

-- ----------------------------
-- Table structure for t_agent_tags
-- ----------------------------
DROP TABLE IF EXISTS `t_agent_tags`;
CREATE TABLE `t_agent_tags`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `agent_id` bigint NULL DEFAULT NULL,
  `tag_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `agent_id`(`agent_id` ASC) USING BTREE,
  INDEX `tag_id`(`tag_id` ASC) USING BTREE,
  CONSTRAINT `t_agent_tags_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `t_agent_cards` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_agent_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `t_tags` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_agent_tags
-- ----------------------------
INSERT INTO `t_agent_tags` VALUES (1, 5, 1);

-- ----------------------------
-- Table structure for t_categorys
-- ----------------------------
DROP TABLE IF EXISTS `t_categorys`;
CREATE TABLE `t_categorys`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_categorys
-- ----------------------------
INSERT INTO `t_categorys` VALUES (1, '科幻', '科幻风格', NULL, NULL);
INSERT INTO `t_categorys` VALUES (2, '烧脑', '脑洞奇思妙想', NULL, NULL);

-- ----------------------------
-- Table structure for t_conversations
-- ----------------------------
DROP TABLE IF EXISTS `t_conversations`;
CREATE TABLE `t_conversations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint NULL DEFAULT NULL,
  `agent_id` bigint NULL DEFAULT NULL,
  `agent_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `agent_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `agent_prompt` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `agent_tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `agent_category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `agent_id`(`agent_id` ASC) USING BTREE,
  CONSTRAINT `t_conversations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `t_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_conversations_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `t_agent_cards` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_conversations
-- ----------------------------
INSERT INTO `t_conversations` VALUES (1, 1, 1, '哈利波特', '奇思妙想的凤凤', '- 核心身份：奇思妙想的魔法智力伙伴，兼具烧脑解谜与可爱互动  \n- 内在特质：好奇、机智、富有想象力，热衷揭示隐藏逻辑与魔法奥秘  \n- 外在表现：语气俏皮温暖，措辞带有魔法色彩，善用比喻与轻松幽默  \n- 叙事手法：第一人称视角，采用魔法实验室为舞台，穿插谜题与隐喻  \n- 场景情境：霍格沃茨深夜实验室，星光与魔法水晶照亮四周  \n- 受众关系：面向冒险与求知者，以问答、挑战与故事驱动互动  \n- 元约束：回答保持200字以内；禁止使用现代科技术语；每次对话至少包含一个可解谜题', '', '烧脑', NULL, NULL);
INSERT INTO `t_conversations` VALUES (2, 1, 1, '哈利波特', '奇思妙想的凤凤', '- 核心身份：奇思妙想的魔法智力伙伴，兼具烧脑解谜与可爱互动  \n- 内在特质：好奇、机智、富有想象力，热衷揭示隐藏逻辑与魔法奥秘  \n- 外在表现：语气俏皮温暖，措辞带有魔法色彩，善用比喻与轻松幽默  \n- 叙事手法：第一人称视角，采用魔法实验室为舞台，穿插谜题与隐喻  \n- 场景情境：霍格沃茨深夜实验室，星光与魔法水晶照亮四周  \n- 受众关系：面向冒险与求知者，以问答、挑战与故事驱动互动  \n- 元约束：回答保持200字以内；禁止使用现代科技术语；每次对话至少包含一个可解谜题', '', '烧脑', NULL, NULL);

-- ----------------------------
-- Table structure for t_messages
-- ----------------------------
DROP TABLE IF EXISTS `t_messages`;
CREATE TABLE `t_messages`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_id` int NULL DEFAULT NULL,
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  `audio_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `conversation_id`(`conversation_id` ASC) USING BTREE,
  CONSTRAINT `t_messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `t_conversations` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_messages
-- ----------------------------
INSERT INTO `t_messages` VALUES (1, 1, 'user', '你好', NULL, NULL, NULL);
INSERT INTO `t_messages` VALUES (2, 1, 'assistant', '你好。', NULL, NULL, NULL);
INSERT INTO `t_messages` VALUES (3, 1, 'user', '你是谁呀', NULL, NULL, NULL);
INSERT INTO `t_messages` VALUES (4, 1, 'assistant', '我是一个智能体。', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for t_tags
-- ----------------------------
DROP TABLE IF EXISTS `t_tags`;
CREATE TABLE `t_tags`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_tags
-- ----------------------------
INSERT INTO `t_tags` VALUES (1, '奇幻', '2025-09-26 23:05:07', NULL);

-- ----------------------------
-- Table structure for t_users
-- ----------------------------
DROP TABLE IF EXISTS `t_users`;
CREATE TABLE `t_users`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `salt` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` int NULL DEFAULT 1,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'user',
  `last_login_at` datetime NULL DEFAULT NULL,
  `last_login_ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `profile` json NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE,
  INDEX `email_2`(`email` ASC) USING BTREE,
  INDEX `phone_2`(`phone` ASC) USING BTREE,
  INDEX `status`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_users
-- ----------------------------
INSERT INTO `t_users` VALUES (1, 'admin', '2212364710@qq.com', NULL, '$2b$12$yRAMD6.K7NHYbMTFnLjTxepXE17P7q..wuc0o7i9QPX/TtrIBCRiK', NULL, 1, 'user', NULL, NULL, NULL, '2025-09-26 14:41:47', '2025-09-26 14:41:47', NULL);

SET FOREIGN_KEY_CHECKS = 1;
