-- CreateTable
CREATE TABLE `Office` (
    `office_id` INTEGER NOT NULL AUTO_INCREMENT,
    `office_street_address` VARCHAR(100) NOT NULL,
    `office_city` VARCHAR(25) NOT NULL,
    `office_county` VARCHAR(50) NOT NULL,
    `office_postal_code` VARCHAR(10) NOT NULL,
    `office_manager_id` INTEGER NOT NULL,

    PRIMARY KEY (`office_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
