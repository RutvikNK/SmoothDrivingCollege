-- CreateTable
CREATE TABLE `Positions` (
    `emp_pos_id` INTEGER NOT NULL AUTO_INCREMENT,
    `emp_post_name` ENUM('MANAGER', 'SENIOR_INSTRUCTOR', 'INSTRUCTOR', 'ADMIN') NOT NULL DEFAULT 'INSTRUCTOR',

    PRIMARY KEY (`emp_pos_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `EmployeePositions` (
    `emp_id` INTEGER NOT NULL,
    `pos_id` INTEGER NOT NULL,

    UNIQUE INDEX `EmployeePositions_emp_id_key`(`emp_id`),
    UNIQUE INDEX `EmployeePositions_pos_id_key`(`pos_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `EmployeePositions` ADD CONSTRAINT `EmployeePositions_emp_id_fkey` FOREIGN KEY (`emp_id`) REFERENCES `Employee`(`emp_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `EmployeePositions` ADD CONSTRAINT `EmployeePositions_pos_id_fkey` FOREIGN KEY (`pos_id`) REFERENCES `Positions`(`emp_pos_id`) ON DELETE RESTRICT ON UPDATE CASCADE;
