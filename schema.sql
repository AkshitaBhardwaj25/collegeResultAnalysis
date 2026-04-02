-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: college_results
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course`
--
CREATE DATABASE IF NOT EXISTS college_results;
USE college_results;

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `CourseID` int NOT NULL AUTO_INCREMENT,
  `CourseCode` varchar(20) NOT NULL,
  `CourseName` varchar(100) NOT NULL,
  `DepartmentID` int DEFAULT NULL,
  `Credits` int NOT NULL,
  `Semester` int NOT NULL,
  PRIMARY KEY (`CourseID`),
  UNIQUE KEY `CourseCode` (`CourseCode`),
  KEY `DepartmentID` (`DepartmentID`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`DepartmentID`) REFERENCES `department` (`DepartmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'CS101','Introduction to Programming',1,4,1),(2,'CS102','Data Structures',1,4,2),(3,'CS201','Database Systems',1,3,3),(4,'CS202','Operating Systems',1,3,3),(5,'ME101','Engineering Mechanics',2,4,1),(6,'ME102','Thermodynamics',2,3,2),(7,'EE101','Basic Electronics',3,3,1),(8,'EE201','Digital Circuits',3,3,2),(9,'CE101','Surveying',4,4,1),(10,'MA101','Calculus',5,4,1),(11,'MA201','Linear Algebra',5,3,2);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coursestats`
--

DROP TABLE IF EXISTS `coursestats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coursestats` (
  `CourseID` int NOT NULL,
  `AvgMarks` decimal(5,2) DEFAULT NULL,
  `LastUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CourseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coursestats`
--

LOCK TABLES `coursestats` WRITE;
/*!40000 ALTER TABLE `coursestats` DISABLE KEYS */;
INSERT INTO `coursestats` VALUES (1,77.25,'2025-11-14 19:15:43'),(2,86.00,'2025-11-14 19:15:43'),(3,NULL,'2025-11-14 19:15:43'),(4,NULL,'2025-11-14 19:15:43'),(5,77.50,'2025-11-14 19:15:43'),(6,59.00,'2025-11-14 19:15:43'),(7,83.50,'2025-11-14 19:15:43'),(8,83.00,'2025-11-14 19:15:43'),(9,66.67,'2025-11-14 19:15:43'),(10,88.00,'2025-11-14 19:15:43'),(11,92.00,'2025-11-14 19:15:43');
/*!40000 ALTER TABLE `coursestats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `DepartmentID` int NOT NULL AUTO_INCREMENT,
  `DepartmentName` varchar(100) NOT NULL,
  `HOD` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`DepartmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'Computer Science','Dr. Alice Parker'),(2,'Mechanical Engineering','Dr. John Carter'),(3,'Electronics','Dr. David Stone'),(4,'Civil Engineering','Dr. Maria Roberts'),(5,'Mathematics','Dr. Emily White');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam`
--

DROP TABLE IF EXISTS `exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam` (
  `ExamID` int NOT NULL AUTO_INCREMENT,
  `ExamName` varchar(100) NOT NULL,
  `ExamType` enum('Midterm','EndSem','Internal','Practical') NOT NULL,
  `AcademicYear` year NOT NULL,
  `Semester` int NOT NULL,
  `ExamDate` date NOT NULL,
  PRIMARY KEY (`ExamID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam`
--

LOCK TABLES `exam` WRITE;
/*!40000 ALTER TABLE `exam` DISABLE KEYS */;
INSERT INTO `exam` VALUES (1,'Midterm SEM1','Midterm',2025,1,'2025-03-05'),(2,'EndSem SEM1','EndSem',2025,1,'2025-05-20'),(3,'Midterm SEM2','Midterm',2025,2,'2025-09-10'),(4,'EndSem SEM2','EndSem',2025,2,'2025-11-25');
/*!40000 ALTER TABLE `exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `FacultyID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `DepartmentID` int DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`FacultyID`),
  KEY `DepartmentID` (`DepartmentID`),
  CONSTRAINT `faculty_ibfk_1` FOREIGN KEY (`DepartmentID`) REFERENCES `department` (`DepartmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'Dr. Alan Smith',1,'alan.smith@college.edu','9876543210'),(2,'Dr. Lisa Brown',1,'lisa.brown@college.edu','9876501234'),(3,'Dr. George Hill',2,'george.hill@college.edu','9812345678'),(4,'Dr. Olivia Green',2,'olivia.green@college.edu','9823456789'),(5,'Dr. Henry Adams',3,'henry.adams@college.edu','9834567890'),(6,'Dr. Sarah Clark',3,'sarah.clark@college.edu','9845678901'),(7,'Dr. James Walker',4,'james.walker@college.edu','9856789012'),(8,'Dr. Sophia Lewis',4,'sophia.lewis@college.edu','9867890123'),(9,'Dr. Daniel Young',5,'daniel.young@college.edu','9878901234'),(10,'Dr. Emma Scott',5,'emma.scott@college.edu','9889012345');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result` (
  `ResultID` int NOT NULL AUTO_INCREMENT,
  `StudentID` int DEFAULT NULL,
  `CourseID` int DEFAULT NULL,
  `ExamID` int DEFAULT NULL,
  `MarksObtained` decimal(5,2) NOT NULL,
  `MaxMarks` decimal(5,2) NOT NULL,
  `Grade` varchar(2) DEFAULT NULL,
  `Status` enum('Pass','Fail') DEFAULT NULL,
  PRIMARY KEY (`ResultID`),
  KEY `CourseID` (`CourseID`),
  KEY `ExamID` (`ExamID`),
  KEY `fk_result_student` (`StudentID`),
  CONSTRAINT `fk_result_student` FOREIGN KEY (`StudentID`) REFERENCES `student` (`StudentID`) ON DELETE CASCADE,
  CONSTRAINT `result_ibfk_2` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`),
  CONSTRAINT `result_ibfk_3` FOREIGN KEY (`ExamID`) REFERENCES `exam` (`ExamID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result`
--

LOCK TABLES `result` WRITE;
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
INSERT INTO `result` VALUES (1,1,1,1,85.00,100.00,'A','Pass'),(2,1,2,2,90.00,100.00,'A+','Pass'),(3,2,1,1,78.00,100.00,'B+','Pass'),(4,2,2,2,82.00,100.00,'A','Pass'),(5,3,1,1,67.00,100.00,'B','Pass'),(6,4,5,1,74.00,100.00,'B+','Pass'),(7,5,6,2,59.00,100.00,'C','Pass'),(8,6,7,1,91.00,100.00,'A+','Pass'),(9,7,8,2,83.00,100.00,'A','Pass'),(10,8,9,1,68.00,100.00,'B','Pass'),(11,9,9,2,70.00,100.00,'B+','Pass'),(12,10,10,1,88.00,100.00,'A','Pass'),(13,11,11,2,92.00,100.00,'A+','Pass'),(14,12,1,1,79.00,100.00,'B+','Pass'),(15,13,5,2,81.00,100.00,'A','Pass'),(16,14,7,1,76.00,100.00,'B+','Pass'),(17,15,9,2,62.00,100.00,'B','Pass');
/*!40000 ALTER TABLE `result` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 TRIGGER `trg_auto_grade` BEFORE INSERT ON `result` FOR EACH ROW BEGIN
    SET NEW.Grade = CASE
        WHEN NEW.MarksObtained >= 90 THEN 'A'
        WHEN NEW.MarksObtained >= 80 THEN 'B'
        WHEN NEW.MarksObtained >= 70 THEN 'C'
        WHEN NEW.MarksObtained >= 60 THEN 'D'
        ELSE 'F'
    END;

    SET NEW.Status = CASE
        WHEN NEW.MarksObtained >= 40 THEN 'Pass'
        ELSE 'Fail'
    END;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `StudentID` int NOT NULL AUTO_INCREMENT,
  `RollNo` varchar(20) DEFAULT NULL,
  `Name` varchar(100) NOT NULL,
  `Gender` enum('Male','Female','Other') NOT NULL,
  `DOB` date DEFAULT NULL,
  `DepartmentID` int DEFAULT NULL,
  `BatchYear` year DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`StudentID`),
  KEY `DepartmentID` (`DepartmentID`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`DepartmentID`) REFERENCES `department` (`DepartmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'R1001','John Williams','Male','2003-05-14',1,2023,'john.w@college.edu','9123456789'),(2,'R1002','Emily Johnson','Female','2004-03-21',1,2023,'emily.j@college.edu','9123456790'),(3,'R1003','Michael Brown','Male','2003-07-09',1,2023,'michael.b@college.edu','9123456791'),(4,'R1004','Sophia Davis','Female','2003-02-28',2,2023,'sophia.d@college.edu','9123456792'),(5,'R1005','Daniel Miller','Male','2003-11-10',2,2023,'daniel.m@college.edu','9123456793'),(6,'R1006','Olivia Wilson','Female','2004-08-05',3,2023,'olivia.w@college.edu','9123456794'),(7,'R1007','William Taylor','Male','2003-09-18',3,2023,'william.t@college.edu','9123456795'),(8,'R1008','Ava Moore','Female','2004-06-22',4,2023,'ava.m@college.edu','9123456796'),(9,'R1009','James Anderson','Male','2003-04-13',4,2023,'james.a@college.edu','9123456797'),(10,'R1010','Isabella Thomas','Female','2004-01-30',5,2023,'isabella.t@college.edu','9123456798'),(11,'R1011','Lucas Martin','Male','2003-10-02',5,2023,'lucas.m@college.edu','9123456799'),(12,'R1012','Mia Harris','Female','2004-02-11',1,2023,'mia.h@college.edu','9123456700'),(13,'R1013','Elijah Lewis','Male','2003-12-20',2,2023,'elijah.l@college.edu','9123456701'),(14,'R1014','Amelia Walker','Female','2004-04-05',3,2023,'amelia.w@college.edu','9123456702'),(15,'R1015','Logan Hall','Male','2003-06-16',4,2023,'logan.h@college.edu','9123456703');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-31  0:01:53
