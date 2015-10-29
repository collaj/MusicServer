-- MySQL Script generated by MySQL Workbench
-- 09/22/15 20:22:45
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema MusicServer
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `MusicServer` ;

-- -----------------------------------------------------
-- Schema MusicServer
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `MusicServer` DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ;
USE `MusicServer` ;

-- -----------------------------------------------------
-- Table `MusicServer`.`Artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `MusicServer`.`Artist` ;

CREATE TABLE IF NOT EXISTS `MusicServer`.`Artist` (
  `artist_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `artist_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`artist_id`),
  UNIQUE INDEX `artist_id_UNIQUE` (`artist_id` ASC),
  UNIQUE INDEX `artist_name_UNIQUE` (`artist_name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MusicServer`.`Album`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `MusicServer`.`Album` ;

CREATE TABLE IF NOT EXISTS `MusicServer`.`Album` (
  `album_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `album_name` VARCHAR(90) NOT NULL,
  `artist_id` INT UNSIGNED NOT NULL,
  `genre` VARCHAR(45) NULL,
  `year` INT NULL,
  PRIMARY KEY (`album_id`),
  UNIQUE INDEX `album_id_UNIQUE` (`album_id` ASC),
  INDEX `fk_Album_Artist_idx` (`artist_id` ASC),
  CONSTRAINT `fk_Album_Artist`
    FOREIGN KEY (`artist_id`)
    REFERENCES `MusicServer`.`Artist` (`artist_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MusicServer`.`Track`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `MusicServer`.`Track` ;

CREATE TABLE IF NOT EXISTS `MusicServer`.`Track` (
  `track_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `track_name` VARCHAR(90) NOT NULL,
  `track_num` INT UNSIGNED NULL,
  `album_id` INT UNSIGNED NOT NULL,
  `file_path` TEXT NOT NULL,
  `track_length` VARCHAR(6) NULL,
  PRIMARY KEY (`track_id`),
  INDEX `fk_Track_Album1_idx` (`album_id` ASC),
  CONSTRAINT `fk_Track_Album1`
    FOREIGN KEY (`album_id`)
    REFERENCES `MusicServer`.`Album` (`album_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
