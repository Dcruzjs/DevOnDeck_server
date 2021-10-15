-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema dev_on_deck
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dev_on_deck
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dev_on_deck` ;
USE `dev_on_deck` ;

-- -----------------------------------------------------
-- Table `dev_on_deck`.`developers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dev_on_deck`.`developers` (
  `developer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `position` VARCHAR(255) NOT NULL,
  `genre` VARCHAR(255) NOT NULL,
  `description` LONGTEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`developer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dev_on_deck`.`companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dev_on_deck`.`companies` (
  `company_id` INT NOT NULL AUTO_INCREMENT,
  `company_name` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`company_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dev_on_deck`.`positions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dev_on_deck`.`positions` (
  `company_id` INT NOT NULL,
  `position_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` LONGTEXT NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  INDEX `fk_positions_companies_idx` (`company_id` ASC) VISIBLE,
  PRIMARY KEY (`position_id`),
  CONSTRAINT `fk_positions_companies`
    FOREIGN KEY (`company_id`)
    REFERENCES `dev_on_deck`.`companies` (`company_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dev_on_deck`.`skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dev_on_deck`.`skills` (
  `skill_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`skill_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dev_on_deck`.`developers_skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dev_on_deck`.`developers_skills` (
  `developer_id` INT NOT NULL,
  `skill_id` INT NOT NULL,
  PRIMARY KEY (`developer_id`, `skill_id`),
  INDEX `fk_developers_has_skills_skills1_idx` (`skill_id` ASC) VISIBLE,
  INDEX `fk_developers_has_skills_developers1_idx` (`developer_id` ASC) VISIBLE,
  CONSTRAINT `fk_developers_has_skills_developers1`
    FOREIGN KEY (`developer_id`)
    REFERENCES `dev_on_deck`.`developers` (`developer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_developers_has_skills_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `dev_on_deck`.`skills` (`skill_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dev_on_deck`.`positions_skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dev_on_deck`.`positions_skills` (
  `position_id` INT NOT NULL,
  `skill_id` INT NOT NULL,
  PRIMARY KEY (`position_id`, `skill_id`),
  INDEX `fk_positions_has_skills_skills1_idx` (`skill_id` ASC) VISIBLE,
  INDEX `fk_positions_has_skills_positions1_idx` (`position_id` ASC) VISIBLE,
  CONSTRAINT `fk_positions_has_skills_positions1`
    FOREIGN KEY (`position_id`)
    REFERENCES `dev_on_deck`.`positions` (`position_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_positions_has_skills_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `dev_on_deck`.`skills` (`skill_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

DELETE FROM skills;

INSERT INTO skills(name)
VALUES('javascript'),('python'),('java'),('html5'),('css3'),('mysql'),('ruby'),('csharp'),('go'),('nodejs'),('flask'),('spring');