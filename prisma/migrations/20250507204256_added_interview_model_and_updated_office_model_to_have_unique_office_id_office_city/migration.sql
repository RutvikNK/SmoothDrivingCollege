/*
  Warnings:

  - A unique constraint covering the columns `[office_id,office_city]` on the table `Office` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateTable
CREATE TABLE `Interview` (
    `interv_client_id` INTEGER NOT NULL,
    `interv_inst_id` INTEGER NOT NULL,
    `interv_location_id` INTEGER NOT NULL,
    `interv_location` VARCHAR(191) NOT NULL,
    `interv_date` DATE NOT NULL,

    PRIMARY KEY (`interv_client_id`, `interv_inst_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateIndex
CREATE UNIQUE INDEX `Office_office_id_office_city_key` ON `Office`(`office_id`, `office_city`);

-- AddForeignKey
ALTER TABLE `Interview` ADD CONSTRAINT `Interview_interv_client_id_fkey` FOREIGN KEY (`interv_client_id`) REFERENCES `Client`(`client_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Interview` ADD CONSTRAINT `Interview_interv_inst_id_fkey` FOREIGN KEY (`interv_inst_id`) REFERENCES `Employee`(`emp_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Interview` ADD CONSTRAINT `Interview_interv_location_id_interv_location_fkey` FOREIGN KEY (`interv_location_id`, `interv_location`) REFERENCES `Office`(`office_id`, `office_city`) ON DELETE RESTRICT ON UPDATE CASCADE;
