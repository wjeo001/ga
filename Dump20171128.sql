CREATE DATABASE  IF NOT EXISTS `gen_001` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `gen_001`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: gen_001
-- ------------------------------------------------------
-- Server version	5.5.5-10.2.8-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_number` varchar(10) DEFAULT NULL,
  `street_number` varchar(10) DEFAULT NULL,
  `street_name` varchar(100) DEFAULT NULL,
  `suburb` varchar(50) DEFAULT NULL,
  `state` varchar(20) NOT NULL,
  `postcode` varchar(4) DEFAULT NULL,
  `people_id` int(11) NOT NULL,
  `addr_type` varchar(10) NOT NULL,
  `street_address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_adrs_p_id_idx` (`people_id`),
  CONSTRAINT `fk_adrs_p_id` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='Residential and postal address';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `body` text DEFAULT NULL,
  `create_date` timestamp(6) NULL DEFAULT current_timestamp(6),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `course_unit_links`
--

DROP TABLE IF EXISTS `course_unit_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_unit_links` (
  `cul_id` int(11) NOT NULL AUTO_INCREMENT,
  `cul_parent` int(11) NOT NULL,
  `cul_child` int(11) NOT NULL,
  PRIMARY KEY (`cul_id`),
  UNIQUE KEY `cul_id_UNIQUE` (`cul_id`),
  KEY `fk_cul_parent_idx` (`cul_parent`),
  KEY `fk_cul_child_idx` (`cul_child`),
  CONSTRAINT `fk_cul_child` FOREIGN KEY (`cul_child`) REFERENCES `units` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cul_parent` FOREIGN KEY (`cul_parent`) REFERENCES `courses` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8 COMMENT='course and units link';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) NOT NULL,
  `course_desc` text DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `year` int(4) DEFAULT NULL,
  `semester` int(1) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `created_date` timestamp NULL DEFAULT current_timestamp(),
  `created_username` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COMMENT='course definition';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `people`
--

DROP TABLE IF EXISTS `people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mob` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `people_type` varchar(10) DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='students and staffs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `people_unit_quiz_link`
--

DROP TABLE IF EXISTS `people_unit_quiz_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_unit_quiz_link` (
  `puql_id` int(11) NOT NULL AUTO_INCREMENT,
  `pu_id` int(11) DEFAULT NULL,
  `qs_id` int(11) DEFAULT NULL,
  `qr_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`puql_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `people_units`
--

DROP TABLE IF EXISTS `people_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_units` (
  `pu_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `people_id` int(11) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`pu_id`),
  UNIQUE KEY `id_UNIQUE` (`pu_id`),
  KEY `fk_pu_course_idx` (`course_id`),
  KEY `fk_pu_unit_idx` (`unit_id`),
  KEY `fk_pu_people_idx` (`people_id`),
  CONSTRAINT `fk_pu_course` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pu_people` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pu_unit` FOREIGN KEY (`unit_id`) REFERENCES `units` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8 COMMENT='course and unit enrolments for students';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_answer`
--

DROP TABLE IF EXISTS `quiz_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_answer` (
  `qa_id` int(11) NOT NULL AUTO_INCREMENT,
  `qa_answer` varchar(45) NOT NULL,
  `qa_isRightAnswer` binary(1) NOT NULL DEFAULT '0',
  `qq_id` int(11) NOT NULL,
  PRIMARY KEY (`qa_id`),
  UNIQUE KEY `qa_id_UNIQUE` (`qa_id`),
  KEY `fk_qa_qq_idx` (`qq_id`),
  CONSTRAINT `fk_qa_qq` FOREIGN KEY (`qq_id`) REFERENCES `quiz_questions` (`qq_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_answers_commit`
--

DROP TABLE IF EXISTS `quiz_answers_commit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_answers_commit` (
  `qa_id` int(11) NOT NULL AUTO_INCREMENT,
  `qa_answer` text DEFAULT NULL,
  `qq_number` int(11) DEFAULT NULL,
  `qa_answer_number` varchar(2) DEFAULT NULL,
  `qs_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`qa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=165 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_questions`
--

DROP TABLE IF EXISTS `quiz_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_questions` (
  `qq_id` int(11) NOT NULL AUTO_INCREMENT,
  `qq_question` text DEFAULT NULL,
  `qq_type` varchar(45) DEFAULT NULL,
  `qq_number_of_answers` int(11) DEFAULT NULL,
  `qs_id` int(11) DEFAULT NULL,
  `qq_body` text DEFAULT NULL,
  `qq_number` int(11) DEFAULT NULL,
  PRIMARY KEY (`qq_id`),
  UNIQUE KEY `qq_id_UNIQUE` (`qq_id`),
  KEY `fk_qq_qs_idx` (`qs_id`),
  CONSTRAINT `fk_qq_qs` FOREIGN KEY (`qs_id`) REFERENCES `quiz_sets` (`qs_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_questions_commit`
--

DROP TABLE IF EXISTS `quiz_questions_commit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_questions_commit` (
  `qq_id` int(11) NOT NULL AUTO_INCREMENT,
  `qq_body` mediumtext DEFAULT NULL,
  `qq_number` int(11) DEFAULT NULL,
  `qq_correct_answer` varchar(999) DEFAULT NULL,
  `qs_id` int(11) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `description_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`qq_id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_record`
--

DROP TABLE IF EXISTS `quiz_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_record` (
  `qr_id` int(11) NOT NULL AUTO_INCREMENT,
  `qs_id` int(11) DEFAULT NULL,
  `qr_correct` int(11) DEFAULT NULL,
  `qr_total` int(11) DEFAULT NULL,
  `qr_attempt` int(11) DEFAULT NULL,
  `qr_answered` varchar(100) DEFAULT NULL,
  `people_id` int(11) DEFAULT NULL,
  `pu_id` int(11) DEFAULT NULL,
  `percent` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`qr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_sets`
--

DROP TABLE IF EXISTS `quiz_sets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_sets` (
  `qs_id` int(11) NOT NULL AUTO_INCREMENT,
  `qs_name` varchar(100) NOT NULL,
  `qs_type` varchar(20) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `number_of_questions` int(3) DEFAULT NULL,
  `quizfile` varchar(999) DEFAULT NULL,
  PRIMARY KEY (`qs_id`),
  UNIQUE KEY `qs_id_UNIQUE` (`qs_id`),
  KEY `fk_unit_id_idx` (`unit_id`),
  CONSTRAINT `fk_qs_units` FOREIGN KEY (`unit_id`) REFERENCES `units` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='quiz definition';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_staging_answers`
--

DROP TABLE IF EXISTS `quiz_staging_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_staging_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qa_answer` text DEFAULT NULL,
  `qq_number` int(11) DEFAULT NULL,
  `qa_answer_number` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_staging_questions`
--

DROP TABLE IF EXISTS `quiz_staging_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_staging_questions` (
  `qq_body` mediumtext DEFAULT NULL,
  `qq_number` int(11) DEFAULT NULL,
  `qq_correct_answer` varchar(999) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `description_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz_user_answers`
--

DROP TABLE IF EXISTS `quiz_user_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_user_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qr_id` int(11) DEFAULT NULL,
  `question_number` int(11) DEFAULT NULL,
  `user_answer` mediumtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ref_categories`
--

DROP TABLE IF EXISTS `ref_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ref_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ref_description`
--

DROP TABLE IF EXISTS `ref_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ref_description` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ref_subjects`
--

DROP TABLE IF EXISTS `ref_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ref_subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(99) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `units`
--

DROP TABLE IF EXISTS `units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `units` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_name` varchar(100) NOT NULL,
  `unit_desc` varchar(999) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `year` int(4) DEFAULT NULL,
  `semester` int(1) DEFAULT NULL,
  `subject` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='unit definitions';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `users_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(100) DEFAULT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `register_date` timestamp NULL DEFAULT current_timestamp(),
  `username` varchar(30) DEFAULT NULL,
  `power_level` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`users_id`),
  UNIQUE KEY `users_id_UNIQUE` (`users_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-28  4:09:48
