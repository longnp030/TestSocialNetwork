CREATE DATABASE  IF NOT EXISTS `tomo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tomo`;
-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: tomo
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('558sjvakg2deddq4jxqygpveltqpju0b','.eJxVjDsOwjAQBe_iGlny36ak5wzWeneFA8iW4qSKuDuJlALamXlvExnWpeZ18JwnEldhxOWXFcAXt0PQE9qjS-xtmacij0Sedsh7J37fzvbvoMKo-zqVEilwUc4z2cjWxOACGe3AI6KP3jjFFlVUSWt0O1DeADuyGiwm8fkC3jc3WA:1l2rfu:GU9sqA0iGsxhjylg5OrFnscO_WeMer55oVw_Ii9lMb8','2021-02-05 08:20:10.545616'),('c5nxzb7dc08m20616ikgej4sgt15haud','.eJxVjDsOwjAQBe_iGlny36ak5wzWeneFA8iW4qSKuDuJlALamXlvExnWpeZ18JwnEldhxOWXFcAXt0PQE9qjS-xtmacij0Sedsh7J37fzvbvoMKo-zqVEilwUc4z2cjWxOACGe3AI6KP3jjFFlVUSWt0O1DeADuyGiwm8fkC3jc3WA:1l2yMS:JovKUSibC-JG9ox01jVS__9SN5GZm86hefdPJjvFf9A','2021-02-05 15:28:32.165786'),('iye63afe2063qlq8siss194orth5454o','.eJxVjDsOwjAQBe_iGlny36ak5wzWeneFA8iW4qSKuDuJlALamXlvExnWpeZ18JwnEldhxOWXFcAXt0PQE9qjS-xtmacij0Sedsh7J37fzvbvoMKo-zqVEilwUc4z2cjWxOACGe3AI6KP3jjFFlVUSWt0O1DeADuyGiwm8fkC3jc3WA:1l2Uq0:9-yzyeLQQl5TodhOx1vhVYvjwwSB60wqpXSyUSUv0tg','2021-02-04 07:57:04.646493'),('k4imsz6r0d2gl7f0jd2rnr4jw4upan4n','.eJxVjDsOwjAQBe_iGlny36ak5wzWeneFA8iW4qSKuDuJlALamXlvExnWpeZ18JwnEldhxOWXFcAXt0PQE9qjS-xtmacij0Sedsh7J37fzvbvoMKo-zqVEilwUc4z2cjWxOACGe3AI6KP3jjFFlVUSWt0O1DeADuyGiwm8fkC3jc3WA:1l2lfu:MRryp3q5k4Ot8CRPIKUtvTWMoTAdpEgZjc5SX1Z3Tkk','2021-02-05 01:55:46.201491'),('w38udw5nb6le4ob5lb933v08sjvm9hx8','.eJxVjDsOwjAQBe_iGlny36ak5wzWeneFA8iW4qSKuDuJlALamXlvExnWpeZ18JwnEldhxOWXFcAXt0PQE9qjS-xtmacij0Sedsh7J37fzvbvoMKo-zqVEilwUc4z2cjWxOACGe3AI6KP3jjFFlVUSWt0O1DeADuyGiwm8fkC3jc3WA:1l2RWm:d8wg5k5v5I3DgLJNBKKFn2r6zWsGm1LW8tHLI6blksA','2021-02-04 04:25:00.983980'),('y0ix0769s4nhe16z6c8aokhqmbcdbjjr','.eJxVjEEOwiAQRe_C2hDEAaYu3XuGZhgGqRpISrsy3l2bdKHb_977LzXSupRx7TKPU1JnBerwu0Xih9QNpDvVW9Pc6jJPUW-K3mnX15bkedndv4NCvXxrL964SJ4wGXQJogzkQIDFoiUILIGDDcmELIB8yjgwZo8cw9E7AfX-APdQOFU:1l2STn:8Wx2XFHQeGyiu04LO8QSZMFN9-NCe_kv-6Vg44XebWY','2021-02-04 05:25:59.470663');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-23  9:04:57
