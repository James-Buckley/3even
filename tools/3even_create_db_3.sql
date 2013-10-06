-- MySQL dump 10.13  Distrib 5.5.32, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: hp1_test
-- ------------------------------------------------------
-- Server version	5.5.32-0ubuntu0.12.04.1

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
-- Table structure for table `carepack_categories`
--

DROP TABLE IF EXISTS `carepack_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carepack_categories` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `RawCategory` varchar(45) NOT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carepack_categories`
--

LOCK TABLES `carepack_categories` WRITE;
/*!40000 ALTER TABLE `carepack_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `carepack_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carepacks`
--

DROP TABLE IF EXISTS `carepacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carepacks` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `SKU` varchar(45) NOT NULL DEFAULT 'MISSING SKU',
  `Title1` varchar(2048) DEFAULT NULL,
  `Title2` varchar(2048) DEFAULT NULL,
  `Price` decimal(16,3) NOT NULL,
  `Raw1` text,
  `Raw2` text,
  `Link` varchar(2048) DEFAULT NULL,
  `fkCategory` int(11) DEFAULT NULL,
  `loadTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pk`),
  KEY `fkCategory_idx` (`fkCategory`),
  KEY `carepacks_x1` (`SKU`),
  CONSTRAINT `fkCategory` FOREIGN KEY (`fkCategory`) REFERENCES `carepack_categories` (`pk`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17533 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carepacks`
--

LOCK TABLES `carepacks` WRITE;
/*!40000 ALTER TABLE `carepacks` DISABLE KEYS */;
/*!40000 ALTER TABLE `carepacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `prodID` int(11) DEFAULT NULL,
  `SubCatID` int(11) DEFAULT NULL,
  `deviceName` varchar(2048) DEFAULT NULL,
  `link` varchar(2048) DEFAULT NULL,
  `loadTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CatID` int(11) DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `devices_x1` (`prodID`,`pk`)
) ENGINE=InnoDB AUTO_INCREMENT=8701 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_carepacks`
--

DROP TABLE IF EXISTS `devices_carepacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices_carepacks` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `fkDevice` int(11) DEFAULT NULL,
  `fkCarepack` int(11) DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `fkDevice_idx` (`fkDevice`),
  KEY `fkCarepack_idx` (`fkCarepack`),
  CONSTRAINT `fkCarepack` FOREIGN KEY (`fkCarepack`) REFERENCES `carepacks` (`pk`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fkDevice` FOREIGN KEY (`fkDevice`) REFERENCES `devices` (`pk`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=54269 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_carepacks`
--

LOCK TABLES `devices_carepacks` WRITE;
/*!40000 ALTER TABLE `devices_carepacks` DISABLE KEYS */;
/*!40000 ALTER TABLE `devices_carepacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `load_carepack`
--

DROP TABLE IF EXISTS `load_carepack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `load_carepack` (
  `cpsku` varchar(256) DEFAULT NULL,
  `cppriceamt` decimal(16,3) DEFAULT NULL,
  `cpurl` varchar(2048) DEFAULT NULL,
  `cpsubcattext` varchar(2048) DEFAULT NULL,
  `cptitletext` varchar(2048) DEFAULT NULL,
  `cptitle2text` varchar(2048) DEFAULT NULL,
  `cpdescr_html` text,
  `cpspecs_html` text,
  `loadTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `loadFlag` char(1) DEFAULT 'N',
  `srcurl` varchar(2048) DEFAULT NULL,
  `cptext1` varchar(2056) DEFAULT 'NA',
  KEY `load_carepack_x1` (`cpsku`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `load_carepack`
--

LOCK TABLES `load_carepack` WRITE;
/*!40000 ALTER TABLE `load_carepack` DISABLE KEYS */;
/*!40000 ALTER TABLE `load_carepack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `load_model`
--

DROP TABLE IF EXISTS `load_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `load_model` (
  `mcpsku` varchar(45) DEFAULT NULL,
  `mdescr` varchar(2056) DEFAULT NULL,
  `murl` varchar(2056) DEFAULT NULL,
  `mprodid` int(11) DEFAULT NULL,
  `msubcatid` int(11) DEFAULT NULL,
  `mcatid` int(11) DEFAULT NULL,
  `loadTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `loadFlag` char(1) DEFAULT 'N',
  `srcurl` varchar(2056) DEFAULT NULL,
  KEY `load_model_x1` (`mcpsku`,`mprodid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `load_model`
--

LOCK TABLES `load_model` WRITE;
/*!40000 ALTER TABLE `load_model` DISABLE KEYS */;
/*!40000 ALTER TABLE `load_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xlog`
--

DROP TABLE IF EXISTS `xlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xlog` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `logType` varchar(45) NOT NULL,
  `logTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `logMessage` text,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xlog`
--

LOCK TABLES `xlog` WRITE;
/*!40000 ALTER TABLE `xlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `xlog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-10-05 18:47:37
