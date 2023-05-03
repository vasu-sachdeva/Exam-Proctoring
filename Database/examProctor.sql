-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3308
-- Generation Time: Aug 19, 2021 at 03:26 PM
-- Server version: 5.5.22
-- PHP Version: 8.0.2
create database quizapp;
use quizapp;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `quizapp`

-- Table structure for table `proctoring_log`
--
-- ********kaam ka*********
CREATE TABLE `proctoring_log` (
  `pid` bigint(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `test_id` varchar(100) NOT NULL,
  `voice_db` int DEFAULT '0',
  `img_log` longtext NOT NULL,
  `user_movements_updown` tinyint NOT NULL,
  `user_movements_lr` tinyint NOT NULL,
  `user_movements_eyes` tinyint NOT NULL,
  `phone_detection` tinyint NOT NULL,
  `person_status` tinyint NOT NULL,
  `log_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `uid` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `questions_uid` bigint NOT NULL,
  `test_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `qid` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `q` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `a` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `b` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `c` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `d` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ans` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `marks` int NOT NULL,
  `uid` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `sid` bigint NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `test_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `qid` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ans` longtext COLLATE utf8mb4_unicode_ci,
  `uid` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `studenttestinfo`
--

CREATE TABLE `studenttestinfo` (
  `stiid` bigint NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `test_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time_left` time NOT NULL,
  `completed` tinyint DEFAULT '0',
  `uid` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `tid` bigint NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `test_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `test_type` varchar(75) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `end` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `duration` int NOT NULL,
  `show_ans` int NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `topic` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `neg_marks` int NOT NULL,
  `calc` tinyint NOT NULL,
  `proctoring_type` tinyint NOT NULL DEFAULT '0',
  `uid` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uid` bigint NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `register_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_type` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_image` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_login` tinyint NOT NULL,
  `examcredits` int NOT NULL DEFAULT '7'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `quizapp`.`users`
(`uid`,
`name`,
`email`,
`password`,
`user_type`,
`user_image`,
`user_login`)
VALUES
(123456,'Manav','abc@abc.com','lnm','professor','adasdkjdhadkhksdhkjadhkjadhk',2);

SELECT `questions`.`questions_uid`,
    `questions`.`test_id`,
    `questions`.`qid`,
    `questions`.`q`,
    `questions`.`a`,
    `questions`.`b`,
    `questions`.`c`,
    `questions`.`d`,
    `questions`.`ans`,
    `questions`.`marks`,
    `questions`.`uid`
FROM `quizapp`.`questions`;



-- --------------------------------------------------------

--
-- Table structure for table `window_estimation_log`
--

CREATE TABLE `window_estimation_log` (
  `wid` bigint NOT NULL,
  `email` varchar(100) NOT NULL,
  `test_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `window_event` tinyint NOT NULL,
  `transaction_log` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `uid` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

select * from teachers;

--
-- Indexes for dumped tables
--
-- Indexes for table `proctoring_log`
--
ALTER TABLE `proctoring_log`
  ADD PRIMARY KEY (`pid`),
  ADD KEY `proctor_email_index` (`email`),
  ADD KEY `proctor_email_test_id_index` (`email`,`test_id`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`questions_uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`sid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `studenttestinfo`
--
ALTER TABLE `studenttestinfo`
  ADD PRIMARY KEY (`stiid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`tid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `window_estimation_log`
--
ALTER TABLE `window_estimation_log`
  ADD PRIMARY KEY (`wid`),
  ADD KEY `uid` (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `proctoring_log`
--
ALTER TABLE `proctoring_log`
  MODIFY `pid` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `questions_uid` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `sid` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `studenttestinfo`
--
ALTER TABLE `studenttestinfo`
  MODIFY `stiid` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `tid` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `window_estimation_log`
--
ALTER TABLE `window_estimation_log`
  MODIFY `wid` bigint NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--
--
-- Constraints for table `proctoring_log`
--
ALTER TABLE `proctoring_log`
  ADD CONSTRAINT `proctoring_log_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`);

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`);

--
-- Constraints for table `studenttestinfo`
--
ALTER TABLE `studenttestinfo`
  ADD CONSTRAINT `studenttestinfo_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`);

--
-- Constraints for table `teachers`
--
ALTER TABLE `teachers`
  ADD CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`);

--
-- Constraints for table `window_estimation_log`
--
ALTER TABLE `window_estimation_log`
  ADD CONSTRAINT `window_estimation_log_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

select @@password_history