-- CreateTable
CREATE TABLE `Client` (
    `client_id` INTEGER NOT NULL AUTO_INCREMENT,
    `client_name` VARCHAR(100) NOT NULL,
    `client_gender` VARCHAR(10) NOT NULL,
    `client_phone_no` CHAR(10) NOT NULL,
    `client_email` VARCHAR(100) NOT NULL,
    `client_inst_id` INTEGER NOT NULL,
    `client_emergency_contact_name` VARCHAR(100) NOT NULL,
    `client_emergency_contact_no` CHAR(10) NOT NULL,
    `client_interviewed` BOOLEAN NOT NULL DEFAULT false,

    PRIMARY KEY (`client_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Client` ADD CONSTRAINT `Client_client_inst_id_fkey` FOREIGN KEY (`client_inst_id`) REFERENCES `Employee`(`emp_id`) ON DELETE RESTRICT ON UPDATE CASCADE;
