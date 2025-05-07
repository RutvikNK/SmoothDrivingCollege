/*
  Warnings:

  - The primary key for the `Meeting` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to alter the column `meeting_start` on the `Meeting` table. The data in that column could be lost. The data in that column will be cast from `DateTime(0)` to `DateTime`.
  - You are about to alter the column `meeting_end` on the `Meeting` table. The data in that column could be lost. The data in that column will be cast from `DateTime(0)` to `DateTime`.

*/
-- AlterTable
ALTER TABLE `Meeting` DROP PRIMARY KEY,
    MODIFY `meeting_start` DATETIME NOT NULL,
    MODIFY `meeting_end` DATETIME NOT NULL,
    ADD PRIMARY KEY (`meeting_client_id`, `meeting_inst_id`, `meeting_start`);

-- CreateTable
CREATE TABLE `WorksAt` (
    `emp_id` INTEGER NOT NULL,
    `office_id` INTEGER NOT NULL,

    UNIQUE INDEX `WorksAt_emp_id_key`(`emp_id`),
    PRIMARY KEY (`emp_id`, `office_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `WorksAt` ADD CONSTRAINT `WorksAt_emp_id_fkey` FOREIGN KEY (`emp_id`) REFERENCES `Employee`(`emp_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `WorksAt` ADD CONSTRAINT `WorksAt_office_id_fkey` FOREIGN KEY (`office_id`) REFERENCES `Office`(`office_id`) ON DELETE RESTRICT ON UPDATE CASCADE;
