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
-- Dumping data for table `ref_categories`
--

LOCK TABLES `ref_categories` WRITE;
/*!40000 ALTER TABLE `ref_categories` DISABLE KEYS */;
INSERT INTO `ref_categories` VALUES (1,'Problem Solving','GA',20),(2,'Verbal Reasoning','GA',20),(3,'Space and Geometry','GA',20),(4,'Nonverbal Reasoning','GA',20),(5,'Deductive Reasoning','GA',20),(6,'Interpret Meaning from text','Reading-English',22),(7,'Point of view','Reading-English',22),(8,'Inference','Reading-English',22),(9,'Main purpose','Reading-English',22),(10,'Figurative Language','Reading-English',22),(11,'Interpret word definition from text','Reading-English',22),(12,'Main idea','Reading-English',22),(13,'Ideas, text Structure','Writing-English',23),(14,'Cohesion, Control of language','Writing-English',23),(15,'Grammar, Puntuation','Writing-English',23),(16,'Vocabulary, Spelling','Writing-English',23),(17,'Problem Solving','Maths',21),(18,'Space and Geometry','Maths',21),(19,'Patterns and Algebra','Maths',21),(20,'Chance and Data','Maths',21),(21,'Numeracy and Measurement','Maths',21);
/*!40000 ALTER TABLE `ref_categories` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `ref_description`
--

LOCK TABLES `ref_description` WRITE;
/*!40000 ALTER TABLE `ref_description` DISABLE KEYS */;
INSERT INTO `ref_description` VALUES (1,'Calculation',21),(2,'Series and Sequence',21),(3,'Algebra',21),(4,'Mixed Pattern',21),(5,'Weight',21),(6,'Date',21),(7,'Time',21),(8,'Height',21),(9,'Money',21),(10,'Ratio',21),(11,'Volume',21),(12,'Patterns',21),(13,'Space',21),(14,'Identify',21),(15,'Statement',21),(16,'Analysis',21),(17,'Symmetry',21),(18,'Cube',21),(19,'Angle',21),(20,'Extraolate information from Graph',21),(21,'Average',21),(22,'Multy Step',21),(23,'Probability',21),(24,'Average',21),(25,'Distance',20),(26,'Weight',20),(27,'Height',20),(28,'Dicrection',20),(29,'Sequence Patterns',20),(30,'Date',20),(31,'Fraction',20),(32,'Volume',20),(33,'Setence Connection',20),(34,'Word',20),(35,'Proverb',20),(36,'Spelling',20),(37,'Grammar',20),(38,'Synonym',20),(39,'Antonym',20),(40,'Odd One Out',20),(41,'Quantity',20),(42,'Statement',20),(43,'Age',20),(44,'Chance',20),(45,'Analogies',20),(46,'Code Translation',20);
/*!40000 ALTER TABLE `ref_description` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `ref_subjects`
--

LOCK TABLES `ref_subjects` WRITE;
/*!40000 ALTER TABLE `ref_subjects` DISABLE KEYS */;
INSERT INTO `ref_subjects` VALUES (1,'English',NULL),(2,'Mathematics',NULL),(3,'Science',NULL),(4,'Biology',NULL),(5,'Chemistry',NULL),(6,'Earth and Environmental Science',NULL),(7,'Physics',NULL),(8,'Senior Science',NULL),(9,'Mathematics General',NULL),(10,'Mathematics Extension 1',NULL),(11,'Mathematics Extension 2',NULL),(12,'English (Standard)',NULL),(13,'English (Advanced)',NULL),(14,'Preliminary English Extension',NULL),(15,'HSC English Extension 1',NULL),(16,'HSC English Extension 2',NULL),(17,'English as a Second Language',NULL),(18,'Fundamentals of English',NULL),(19,'OC',NULL),(20,'GA',NULL),(21,'Maths',NULL),(22,'Reading-English',NULL),(23,'Writing-English',NULL);
/*!40000 ALTER TABLE `ref_subjects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-28  5:29:14
