-- DROP TABLE oj_user;
-- DROP TABLE oj_session;
-- DROP TABLE oj_user_role;

--
-- User
--
CREATE TABLE IF NOT EXISTS `oj_user`
(
	`id`				INT			NOT NULL AUTO_INCREMENT,
	
	`email`				VARCHAR(50)	NOT NULL,
	`password`			VARCHAR(32)	NOT NULL,
	`password_salt`		VARCHAR(5)	NOT NULL,
	`display_name`		VARCHAR(20)	NOT NULL,
	`gender`			TINYINT		NOT NULL,
	
	`created_time`		DATETIME	NOT NULL,
	`updated_time`		DATETIME	NOT NULL,
	
	`activated`			TINYINT(1)	NOT NULL,
	`activation_code`	INT			NOT NULL,
	`activation_time`	DATETIME	NOT NULL,
	
	`banned`			TINYINT(1)	NOT NULL,
	`ban_expired`		DATETIME	NOT NULL,
	
	`deleted`			TINYINT(1)	NOT NULL,
	
	PRIMARY KEY							(`id`),
	UNIQUE KEY	`email_unique`			(`email`),
	INDEX		`display_name_index`	(`display_name`),
	INDEX		`created_time_index`	(`created_time`),
	INDEX		`activated_index`		(`activated`),
	INDEX		`banned_index`			(`banned`),
	INDEX		`deleted_index`			(`deleted`)
)
ENGINE=InnoDB;


--
-- Session
--
CREATE TABLE IF NOT EXISTS `oj_session`
(
	`id`			CHAR(32)		NOT NULL,
	`user_id`		INT				NOT NULL,
	`created_time`	DATETIME		NOT NULL,
	`updated_time`	DATETIME		NOT NULL,
	`expired_time`	DATETIME		NOT NULL,
	`user_agent`	VARCHAR(200)	NOT NULL,
	`persistent`	TINYINT(1)		NOT NULL,
	
	PRIMARY KEY							(`id`),
	INDEX		`user_id_index`			(`user_id`),
	INDEX		`expired_time_index`	(`expired_time`)
)
ENGINE=InnoDB;


--
-- User roles
--
CREATE TABLE IF NOT EXISTS `oj_user_role`
(
	`user_id`	INT	NOT NULL,
	`role_id`	INT	NOT NULL,
	
	PRIMARY KEY (`user_id`, `role_id`),
	INDEX `user_id_index` (`user_id`),
	INDEX `role_id_index` (`role_id`)
)
ENGINE=InnoDB;

--
-- Sample data
--

REPLACE INTO `oj_user`
VALUES (1, "vit@launchar.com", "doviethoa", "", "VIT", 1,
        "2014-07-25 22:58:00", "2014-07-25 22:58:00",
        1, 0, "2014-07-25 22:58:00",
        0, "2014-07-25 22:58:00",
        0);

