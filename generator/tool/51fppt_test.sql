/*
Navicat MySQL Data Transfer

Source Server         : 22.37
Source Server Version : 50716
Source Host           : 172.16.22.37:3306
Source Database       : 51fppt_test

Target Server Type    : MYSQL
Target Server Version : 50716
File Encoding         : 65001

Date: 2019-09-11 17:46:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for excu_time
-- ----------------------------
DROP TABLE IF EXISTS `excu_time`;
CREATE TABLE `excu_time` (
  `history_id` varchar(50) NOT NULL,
  `case_id` int(11) NOT NULL,
  `e_time` int(11) NOT NULL,
  PRIMARY KEY (`case_id`,`history_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for often_step_data
-- ----------------------------
DROP TABLE IF EXISTS `often_step_data`;
CREATE TABLE `often_step_data` (
  `step_id` int(11) NOT NULL,
  `step_name` varchar(100) NOT NULL,
  `http_method` varchar(10) NOT NULL,
  `headers` varchar(3000) DEFAULT NULL,
  `url_sql` varchar(3000) NOT NULL,
  `request_sql_param` text NOT NULL,
  `out_put` longtext,
  `expected_modify` longtext,
  `expected_result` longtext,
  `expected_result_b` longblob,
  UNIQUE KEY `step_id` (`step_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for step_data
-- ----------------------------
DROP TABLE IF EXISTS `step_data`;
CREATE TABLE `step_data` (
  `case_id` int(11) NOT NULL,
  `step` int(11) NOT NULL,
  `test_desc` varchar(2000) NOT NULL,
  `step_reference` varchar(100) DEFAULT NULL,
  `http_method` varchar(10) DEFAULT NULL,
  `headers` varchar(3000) DEFAULT NULL,
  `url_sql` varchar(3000) DEFAULT NULL,
  `request_sql_param` text,
  `out_put` longtext,
  `request_name` varchar(100) DEFAULT NULL,
  `aoto_replace` int(11) DEFAULT NULL,
  `expected_modify` longtext,
  `expected_result` longtext,
  `expected_result_b` longblob,
  PRIMARY KEY (`case_id`,`step`),
  UNIQUE KEY `unicasestep` (`case_id`,`step`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for step_result
-- ----------------------------
DROP TABLE IF EXISTS `step_result`;
CREATE TABLE `step_result` (
  `history_id` varchar(50) NOT NULL,
  `case_id` int(11) NOT NULL,
  `step` int(11) NOT NULL,
  `request_name` varchar(100) DEFAULT NULL,
  `step_reference` varchar(100) NOT NULL,
  `http_method` varchar(10) NOT NULL,
  `headers` varchar(3000) DEFAULT NULL,
  `url_sql` varchar(3000) NOT NULL,
  `request_sql_param` longtext NOT NULL,
  `out_put` longtext,
  `test_desc` varchar(2000) NOT NULL,
  `expected_result` longtext,
  `actual_result` longtext,
  `result` varchar(20) NOT NULL,
  `reason` longtext,
  `runtime` datetime DEFAULT NULL,
  PRIMARY KEY (`case_id`,`history_id`,`step`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for test_data
-- ----------------------------
DROP TABLE IF EXISTS `test_data`;
CREATE TABLE `test_data` (
  `case_id` int(11) NOT NULL,
  `http_method` varchar(10) NOT NULL,
  `headers` varchar(3000) DEFAULT NULL,
  `request_name` varchar(100) DEFAULT NULL,
  `request_url` varchar(200) NOT NULL,
  `request_param` longtext NOT NULL,
  `test_method` varchar(50) NOT NULL,
  `test_desc` varchar(2000) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `expected_modify` longtext,
  `expected_result` longtext,
  `expected_result_b` longblob,
  UNIQUE KEY `case_id` (`case_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for test_result
-- ----------------------------
DROP TABLE IF EXISTS `test_result`;
CREATE TABLE `test_result` (
  `history_id` varchar(50) NOT NULL,
  `case_id` int(11) NOT NULL,
  `http_method` varchar(10) NOT NULL,
  `headers` varchar(3000) DEFAULT NULL,
  `request_name` varchar(100) DEFAULT NULL,
  `request_url` varchar(200) NOT NULL,
  `request_param` longtext NOT NULL,
  `test_method` varchar(50) NOT NULL,
  `test_desc` varchar(2000) NOT NULL,
  `expected_result` longtext,
  `actual_result` longtext,
  `result` varchar(20) NOT NULL,
  `reason` longtext,
  `runtime` datetime DEFAULT NULL,
  PRIMARY KEY (`history_id`,`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `51fppt_test`.`step_data` (`case_id`, `step`, `test_desc`, `step_reference`, `http_method`, `headers`, `url_sql`, `request_sql_param`, `out_put`, `request_name`, `aoto_replace`, `expected_modify`, `expected_result`, `expected_result_b`) VALUES ('24230041', '1', '发票采集', '', 'post', '', '/services/tyjs/saveInvoice', '{\r\n    \"FPXX\": {\r\n        \"FP_KJ\": {\r\n            \"FPQQLSH\": \"10780194078\",\r\n            \"XSF_NSRMC\": \"==测试rest==\",\r\n            \"XSF_NSRSBH\": \"110101N1KRX0F08\",\r\n            \"FPDM\": \"114011015609\",\r\n            \"FPHM\": \"19081601\",\r\n            \"KPRQ\": \"2019-08-11 14:17:39\",\r\n            \"KPLX\": \"2\",\r\n            \"KPHJJE\": \"1199.00\",\r\n            \"HJBHSJE\": \"1024.79\",\r\n            \"KPHJSE\": \"174.21\",\r\n            \"KPXM\": \"华为手机\",\r\n            \"GMF_NSRSBH\": \"110101009791112\",\r\n            \"GMF_NSRMC\": \"梭罗公司\",\r\n            \"GMF_YH\": \"12310\",\r\n            \"GMF_YHZH\": \"123\",\r\n            \"GMF_DZ\": \"美国加州152******\",\r\n            \"GMF_DH\": \"13333333334\",\r\n            \"GMF_SF\": \"1239\",\r\n            \"GMF_EMAIL\": \"926299670@qq.com\",\r\n            \"GMF_SJ\": \"13333333334\",\r\n            \"YFPHM\": \"1237\",\r\n            \"YFPDM\": \"1238\",\r\n            \"JQBH\": \"661505060904\",\r\n            \"KPY\": \"开票员\",\r\n            \"SKY\": \"收款员\",\r\n            \"FHR\": \"复核人\",\r\n            \"SWJG_DM\": \"111019201\",\r\n            \"SPHSL\": \"1\",\r\n            \"FP_ZLDM\": \"2\",\r\n            \"VERSION\": \"1\",\r\n            \"XSF_DZ\": \"北京市海淀区春晖园2号楼\",\r\n            \"XSF_DH\": \"123123123\",\r\n            \"XSF_YH\": \"1236\",\r\n            \"XSF_YHZH\": \"招商银行\",\r\n            \"FJH\": \"9\",\r\n            \"DSPTBM\": \"11110101\",\r\n            \"DKBZ\": \"0\",\r\n            \"PDFPATH\": \"123\",\r\n            \"TSCHBZ\": \"1\",\r\n            \"CHYY\": \"冲红原因\",\r\n            \"XHQD\": \"销货清单\",\r\n            \"XHQDBZ\": \"0\",\r\n            \"BMB_BBH\": \"1233\",\r\n            \"QD_BZ\": \"0\",\r\n            \"DDH\": \"11111111117\",\r\n            \"DSF_PTBM\": \"11111111\",\r\n            \"SGBZ\": \"1\",\r\n            \"QDXMMC\": \"1232\",\r\n            \"SKM\": \"12323354657677\",\r\n            \"EWM\": \"Qk1+BgAAAAAAAD4AAAAoAAAAZAAAAGQAAAABAAEAAAAAAEAGAAAAAAAAAAAAAAAAAAACAAAAAAAA///////////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAAADPAAAzPPzwD////AAAAAAAzwAAMzz88A////wAAAAP/P8P8/DM//A////8AAAAD/z/D/PwzP/wP////AAAAAwM8D/DzPMM/D////wAAAAMDPA/w8zzDPw////8AAAADAzw888P8Dz/P////AAAAAwM8PPPD/A8/z////wAAAAMDM8/PDzAwAw////8AAAADAzPPzw8wMAMP////AAAAA/8/DMAPAwPwD////wAAAAP/PwzADwMD8A////8AAAAAADDzAPPD8zAP////AAAAAAAw8wDzw/MwD////wAAAA//8DDP8APD88////8AAAAP//Awz/ADw/PP////AAAAD8MAD/Aw/zAAD////wAAAA/DAA/wMP8wAA////8AAAAAw8PwAAAP8MwD////AAAAAMPD8AAAD/DMA////wAAAAAAAzPMDMMA/A////8AAAAAAAMzzAzDAPwP////AAAADPPwPz8MM8zDD////wAAAAzz8D8/DDPMww////8AAAAM8AwP8/P/MzwD////AAAADPAMD/Pz/zM8A////wAAAAPz8MPDwM8M/D////8AAAAD8/DDw8DPDPw/////AAAAD/AMMA88D8zPD////wAAAA/wDDAPPA/Mzw////8AAAAPz8PwzPPADMPP////AAAAD8/D8MzzwAzDz////wAAAA//M8PADM8zPDP///8AAAAP/zPDwAzPMzwz////AAAADPDMMDw8MwzMD////wAAAAzwzDA8PDMMzA////8AAAAPDA/88PM/wMwP////AAAADwwP/PDzP8DMD////wAAAA8w8wwzw/zMw8////8AAAAPMPMMM8P8zMPP////AAAADPMM8P8/MzM8A////wAAAAzzDPD/PzMzPAP///8AAAAD888PwD8P/PwD////AAAAA/PPD8A/D/z8A////wAAAAwwMADM/88PwA////8AAAAMMDAAzP/PD8AP////AAAAAz/Azw/wAMzAD////wAAAAM/wM8P8ADMwA////8AAAAMwA8DPDD/Mzwz////AAAADMAPAzww/zM8M////wAAAAwD8PDAwA8z8D////8AAAAMA/DwwMAPM/A/////AAAADA8Dz8zMAwD/D////wAAAAwPA8/MzAMA/w////8AAAAPwMPM/w8wzMP/////AAAAD8DDzP8PMMzD/////wAAAAPzAADD8/8wAPP///8AAAAD8wAAw/P/MADz////AAAAD//w8//wz8P//////wAAAA//8PP/8M/D//////8AAAAAADMzMzMzMwAD////AAAAAAAzMzMzMzMAA////wAAAAP/MD88w/A/P/P///8AAAAD/zA/PMPwPz/z////AAAAAwMz//zzAM8wM////wAAAAMDM//88wDPMDP///8AAAADAzAAD/MwzzAz////AAAAAwMwAA/zMM8wM////wAAAAMDPDDA/DM/MDP///8AAAADAzwwwPwzPzAz////AAAAA/888/APwDM/8////wAAAAP/PPPwD8AzP/P///8AAAAAADPDM8P8zwAD////AAAAAAAzwzPD/M8AA////wAAAA\",\r\n            \"BZ\": \"1\",\r\n            \"FP_MW\": \"6134*3>950+75<8/1208-85*</*14>-65-142/+7390*24855672678136749+92184+/8*553-9-8-+5*</*1/670433467<<3<0*24<4*6\",\r\n            \"DDSJ\": \"2019-08-01 14:15:11\",\r\n            \"JYM\": \"65560891271390877510\"\r\n        },\r\n        \"FP_KJ_MX\": [\r\n            {\r\n                \"SPHXH\": \"01\",\r\n                \"SPMC\": \"华为手机\",\r\n                \"SPSL\": \"1.00000000\",\r\n                \"SPJE\": \"1024.79\",\r\n                \"SPDJ\": \"1024.78632479\",\r\n                \"DW\": \"1231\",\r\n                \"GGXH\": \"12\",\r\n                \"HSJBZ\": \"0\",\r\n                \"FJH\": \"1\",\r\n                \"KCE\": \"2\",\r\n                \"SE\": \"174.21\",\r\n                \"SL\": \"17%\",\r\n                \"SPBM\": \"123\",\r\n                \"ZXBM\": \"1234\",\r\n                \"YHZCBS\": \"1\",\r\n                \"LSLBS\": \"0\",\r\n                \"ZZSTSGL\": \"1235\",\r\n                \"FPHXZ\": \"1\"\r\n            }\r\n        ],\r\n        \"FP_WLXX\": [\r\n            {\r\n                \"CYGS\": \"承运公司\",\r\n                \"WLDH\": \"123123123\",\r\n                \"SHDZ\": \"测试送货地址\",\r\n                \"SHSJ\": \"2019-08-01 14:17:11\"\r\n            }\r\n        ],\r\n        \"FP_ZFXX\": {\r\n            \"ZFFS\": \"测试支付方式\",\r\n            \"ZFPT\": \"测试支付平台\",\r\n            \"ZFLSH\": \"12312312367\"\r\n        }\r\n    }\r\n}', '', '发票采集', NULL, '{\r\n    \"[data][content][returncode]\": \"0000\", \r\n    \"[data][content][returnmessage]\": \"发票上传成功\", \r\n}', '{\n    \"[data][content][returncode]\": \"0000\", \n    \"[data][content][returnmessage]\": \"发票上传成功\", \n    \"[data][dataDescription]\": null, \n    \"[globalInfo][appId]\": \"1.1\", \n    \"[globalInfo][dataExchangeId]\": \"123\", \n    \"[globalInfo][interfaceCode]\": \"EI_INVUPLOAD_U_EC_IP\", \n    \"[globalInfo][passWord]\": \"1621916134FxuQr1nzD4/wsIkcQg73mQ==\", \n    \"[globalInfo][requestCode]\": \"1123\", \n    \"[globalInfo][requestTime]\": \"123\", \n    \"[globalInfo][responseCode]\": \"123\", \n    \"[globalInfo][userName]\": \"123\", \n    \"[returnStateInfo][returnCode]\": \"0000\", \n    \"[returnStateInfo][returnMessage]\": \"发票上传成功\"\n}', NULL);

