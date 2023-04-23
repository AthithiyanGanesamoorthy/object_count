DROP DATABASE IF EXISTS `DB`;
CREATE DATABASE `DB`;
USE `DB`;
DROP TABLE IF EXISTS `objectcounts`;
CREATE TABLE `objectcounts` (
  `objectname` varchar(100) NOT NULL,
  `count` int
);
