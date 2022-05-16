CREATE DATABASE  IF NOT EXISTS `curriculum_dataset` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `curriculum_dataset`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: curriculum_dataset
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `academic_result`
--

DROP TABLE IF EXISTS `academic_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academic_result` (
  `academic_result_id` char(10) NOT NULL,
  `registration_id` char(10) NOT NULL,
  `grade_result` float NOT NULL,
  PRIMARY KEY (`academic_result_id`),
  UNIQUE KEY `academic_result_id_UNIQUE` (`academic_result_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `curriculum_format`
--

DROP TABLE IF EXISTS `curriculum_format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curriculum_format` (
  `curriculum_formatID` char(3) NOT NULL,
  `program_id` varchar(3) NOT NULL,
  `subject_id` varchar(500) NOT NULL,
  `academic_year` int NOT NULL,
  `semester` int NOT NULL,
  `all_credits` int NOT NULL,
  PRIMARY KEY (`curriculum_formatID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programs` (
  `program_id` varchar(3) NOT NULL,
  `program_nameEN` varchar(200) NOT NULL,
  `program_nameTH` varchar(200) NOT NULL,
  `degree_EN` varchar(200) NOT NULL,
  `degree_TH` varchar(200) NOT NULL,
  `all_credits` int NOT NULL,
  PRIMARY KEY (`program_id`),
  UNIQUE KEY `program_id_UNIQUE` (`program_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registrations`
--

DROP TABLE IF EXISTS `registrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations` (
  `registration_id` char(10) NOT NULL,
  `student_id` char(10) NOT NULL,
  `subject_id` varchar(100) NOT NULL,
  `all_credits` int NOT NULL,
  `academic_year` int NOT NULL,
  `semester` int NOT NULL,
  `section` varchar(100) NOT NULL,
  `timestamp` date NOT NULL,
  PRIMARY KEY (`registration_id`),
  UNIQUE KEY `registration_id_UNIQUE` (`registration_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `student_id` char(10) NOT NULL,
  `program_id` varchar(3) NOT NULL,
  `student_nameEN` varchar(255) NOT NULL,
  `student_nameTH` varchar(255) NOT NULL,
  `start_year` int NOT NULL,
  `expected_grad` int NOT NULL,
  `student_email` varchar(200) NOT NULL,
  `student_phonenum` char(10) DEFAULT NULL,
  `gender` char(1) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id_UNIQUE` (`student_id`),
  UNIQUE KEY `student_email_UNIQUE` (`student_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subject_type`
--

DROP TABLE IF EXISTS `subject_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject_type` (
  `subject_type_id` int NOT NULL,
  `subject_type_name` varchar(100) NOT NULL,
  `sub_type_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`subject_type_id`),
  UNIQUE KEY `subject_type_id_UNIQUE` (`subject_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `subject_id` varchar(6) NOT NULL,
  `subject_type_id` int NOT NULL,
  `subject_name` varchar(500) NOT NULL,
  `credits` int NOT NULL,
  `havePrerequisite` tinyint(1) NOT NULL,
  `prerequisite_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`subject_id`),
  UNIQUE KEY `subject_id_UNIQUE` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` varchar(7) NOT NULL,
  `program_id` varchar(3) NOT NULL,
  `nameTH` varchar(255) NOT NULL,
  `nameEN` varchar(255) NOT NULL,
  `role` varchar(100) NOT NULL,
  `gender` char(1) NOT NULL,
  `email` varchar(200) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `program_user_idx` (`program_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-11 15:21:43
