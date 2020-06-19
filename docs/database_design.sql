CREATE TABLE `gp_practices` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name_ice` varchar(255),
  `created_at` timestamp,
  `address` int,
  `phone_num` varchar(255),
  `emis_cdb_practice_code` varchar(255),
  `go_live_date` timestamp,
  `closed` boolean,
  `main_partner` int
);

CREATE TABLE `gp_practices_system_types` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `gp_practice_id` int,
  `system_type` int
);

CREATE TABLE `system_types` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `gp_addresses` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `line_1` varchar(255),
  `line_2` varchar(255),
  `town` varchar(255),
  `county` varchar(255),
  `postcode` varchar(255),
  `dts_email` varchar(255)
);

CREATE TABLE `practice_managers` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `gp_practice_id` int,
  `gp_employee_id` int
);

CREATE TABLE `ip_ranges` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `cidr` varchar(255),
  `gp_practice` int
);

CREATE TABLE `gp_employees` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `email` varchar(255),
  `job_title` int,
  `gmc_id` varchar(255),
  `nmc_id` varchar(255),
  `desktop_id` varchar(255),
  `it_portal_id` varchar(255)
);

CREATE TABLE `gp_practice_employees` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `gp_practice_id` int,
  `gp_employee_id` int,
  `active` boolean
);

CREATE TABLE `job_titles` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(255)
);

CREATE TABLE `system_users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `email` varchar(255),
  `role` int,
  `password_hash` varchar(255),
  `password_salt` varchar(255)
);

CREATE TABLE `system_roles` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

ALTER TABLE `gp_practices` ADD FOREIGN KEY (`address`) REFERENCES `gp_addresses` (`id`);

ALTER TABLE `practice_managers` ADD FOREIGN KEY (`gp_practice_id`) REFERENCES `gp_practices` (`id`);

ALTER TABLE `practice_managers` ADD FOREIGN KEY (`gp_employee_id`) REFERENCES `gp_employees` (`id`);

ALTER TABLE `system_users` ADD FOREIGN KEY (`role`) REFERENCES `system_roles` (`id`);

ALTER TABLE `gp_practice_employees` ADD FOREIGN KEY (`gp_employee_id`) REFERENCES `gp_employees` (`id`);

ALTER TABLE `gp_practice_employees` ADD FOREIGN KEY (`gp_practice_id`) REFERENCES `gp_practices` (`id`);

ALTER TABLE `gp_practices` ADD FOREIGN KEY (`main_partner`) REFERENCES `gp_employees` (`id`);

ALTER TABLE `ip_ranges` ADD FOREIGN KEY (`gp_practice`) REFERENCES `gp_practices` (`id`);

ALTER TABLE `gp_employees` ADD FOREIGN KEY (`job_title`) REFERENCES `job_titles` (`id`);

ALTER TABLE `gp_practices_system_types` ADD FOREIGN KEY (`gp_practice_id`) REFERENCES `gp_practices` (`id`);

ALTER TABLE `gp_practices_system_types` ADD FOREIGN KEY (`system_type`) REFERENCES `system_types` (`name`);
