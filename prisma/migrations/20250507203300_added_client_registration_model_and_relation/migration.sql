-- CreateTable
CREATE TABLE `ClientRegistrations` (
    `client_id` INTEGER NOT NULL,
    `client_reg_office_id` INTEGER NOT NULL,

    UNIQUE INDEX `ClientRegistrations_client_id_key`(`client_id`),
    PRIMARY KEY (`client_id`, `client_reg_office_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `ClientRegistrations` ADD CONSTRAINT `ClientRegistrations_client_id_fkey` FOREIGN KEY (`client_id`) REFERENCES `Client`(`client_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ClientRegistrations` ADD CONSTRAINT `ClientRegistrations_client_reg_office_id_fkey` FOREIGN KEY (`client_reg_office_id`) REFERENCES `Office`(`office_id`) ON DELETE RESTRICT ON UPDATE CASCADE;
