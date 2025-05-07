-- CreateTable
CREATE TABLE `Employee` (
    `emp_id` INTEGER NOT NULL AUTO_INCREMENT,
    `emp_name` VARCHAR(75) NOT NULL,
    `emp_gender` VARCHAR(10) NOT NULL,
    `emp_phone_no` CHAR(10) NOT NULL,
    `emp_email` VARCHAR(30) NOT NULL,
    `emp_manager_id` INTEGER NOT NULL,

    PRIMARY KEY (`emp_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Employee` ADD CONSTRAINT `Employee_emp_manager_id_fkey` FOREIGN KEY (`emp_manager_id`) REFERENCES `Employee`(`emp_id`) ON DELETE RESTRICT ON UPDATE CASCADE;
