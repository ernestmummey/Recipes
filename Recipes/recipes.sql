-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema recipes_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema recipes_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `recipes_schema` DEFAULT CHARACTER SET utf8 ;
USE `recipes_schema` ;

-- -----------------------------------------------------
-- Table `recipes_schema`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `recipes_schema`.`users` ;

CREATE TABLE IF NOT EXISTS `recipes_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(100) NULL,
  `password` VARCHAR(100) NULL,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recipes_schema`.`recipes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `recipes_schema`.`recipes` ;

CREATE TABLE IF NOT EXISTS `recipes_schema`.`recipes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `description` VARCHAR(250) NULL,
  `minutes` VARCHAR(45) NULL,
  `instructions` TEXT(500) NULL,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_recipies_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_recipies_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `recipes_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
