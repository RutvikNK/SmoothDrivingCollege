-- CreateTable
CREATE TABLE `AssignedVehicles` (
    `inst_id` INTEGER NOT NULL,
    `assigned_vehicle_no` CHAR(8) NOT NULL,

    UNIQUE INDEX `AssignedVehicles_inst_id_key`(`inst_id`),
    UNIQUE INDEX `AssignedVehicles_assigned_vehicle_no_key`(`assigned_vehicle_no`),
    PRIMARY KEY (`inst_id`, `assigned_vehicle_no`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `AssignedVehicles` ADD CONSTRAINT `AssignedVehicles_inst_id_fkey` FOREIGN KEY (`inst_id`) REFERENCES `Employee`(`emp_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `AssignedVehicles` ADD CONSTRAINT `AssignedVehicles_assigned_vehicle_no_fkey` FOREIGN KEY (`assigned_vehicle_no`) REFERENCES `Vehicle`(`vehicle_license_no`) ON DELETE RESTRICT ON UPDATE CASCADE;
