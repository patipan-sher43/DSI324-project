CREATE DATABASE `curriculum_dataset`;
USE `curriculum_dataset`;

CREATE TABLE `academic_result` (
  `academic_result_id` char(10) NOT NULL,
  `registration_id` char(10) NOT NULL,
  `grade_result` float NOT NULL,
  PRIMARY KEY (`academic_result_id`),
  UNIQUE KEY `academic_result_id_UNIQUE` (`academic_result_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `curriculum_format` (
  `curriculum_formatID` char(3) NOT NULL,
  `program_id` varchar(3) NOT NULL,
  `subject_id` varchar(500) NOT NULL,
  `academic_year` int NOT NULL,
  `semester` int NOT NULL,
  `all_credits` int NOT NULL,
  PRIMARY KEY (`curriculum_formatID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `programs` (
  `program_id` varchar(3) NOT NULL,
  `program_nameEN` varchar(200) NOT NULL,
  `program_nameTH` varchar(200) NOT NULL,
  `degree_EN` varchar(200) NOT NULL,
  `degree_TH` varchar(200) NOT NULL,
  `all_credits` int NOT NULL,
  PRIMARY KEY (`program_id`),
  UNIQUE KEY `program_id_UNIQUE` (`program_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `subject_type` (
  `subject_type_id` int NOT NULL,
  `subject_type_name` varchar(100) NOT NULL,
  `sub_type_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`subject_type_id`),
  UNIQUE KEY `subject_type_id_UNIQUE` (`subject_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `subjects` (
  `subject_id` varchar(6) NOT NULL,
  `subject_type_id` int NOT NULL,
  `subject_name` varchar(500) NOT NULL,
  `credits` int NOT NULL,
  `havePrerequisite` tinyint(1) NOT NULL,
  `prerequisite_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`subject_id`),
  UNIQUE KEY `subject_id_UNIQUE` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
