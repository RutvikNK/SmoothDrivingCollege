-- CreateTable
CREATE TABLE `Vehicle` (
    `vehicle_license_no` CHAR(8) NOT NULL,
    `vehicle_make` VARCHAR(25) NOT NULL,
    `vehicle_model` VARCHAR(25) NOT NULL,
    `vehicle_year` CHAR(4) NOT NULL,
    `vehicle_color` VARCHAR(15) NOT NULL,
    `vehicle_last_inspection` DATE NOT NULL,

    PRIMARY KEY (`vehicle_license_no`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
