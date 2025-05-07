/*
  Warnings:

  - You are about to alter the column `interv_location` on the `Interview` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `VarChar(25)`.

*/
-- DropForeignKey
ALTER TABLE `Interview` DROP FOREIGN KEY `Interview_interv_location_id_interv_location_fkey`;

-- DropIndex
DROP INDEX `Interview_interv_location_id_interv_location_fkey` ON `Interview`;

-- AlterTable
ALTER TABLE `Interview` MODIFY `interv_location` VARCHAR(25) NOT NULL;

-- CreateTable
CREATE TABLE `Meeting` (
    `meeting_client_id` INTEGER NOT NULL,
    `meeting_inst_id` INTEGER NOT NULL,
    `meeting_vehicle_no` CHAR(8) NOT NULL,
    `meeting_start` DATETIME NOT NULL,
    `meeting_end` DATETIME NOT NULL,
    `meeting_type` ENUM('LESSON', 'WRITTEN_EXAM', 'DRIVING_EXAM') NOT NULL,
    `meeting_notes` VARCHAR(250) NOT NULL,
    `meeting_mileage` INTEGER NOT NULL,

    PRIMARY KEY (`meeting_client_id`, `meeting_inst_id`, `meeting_start`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Interview` ADD CONSTRAINT `Interview_interv_location_id_interv_location_fkey` FOREIGN KEY (`interv_location_id`, `interv_location`) REFERENCES `Office`(`office_id`, `office_city`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Meeting` ADD CONSTRAINT `Meeting_meeting_client_id_fkey` FOREIGN KEY (`meeting_client_id`) REFERENCES `Client`(`client_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Meeting` ADD CONSTRAINT `Meeting_meeting_inst_id_fkey` FOREIGN KEY (`meeting_inst_id`) REFERENCES `Employee`(`emp_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Meeting` ADD CONSTRAINT `Meeting_meeting_vehicle_no_fkey` FOREIGN KEY (`meeting_vehicle_no`) REFERENCES `Vehicle`(`vehicle_license_no`) ON DELETE RESTRICT ON UPDATE CASCADE;
