-- Test Fixtures for Spy Cats Database
-- Passwords are hashed with bcrypt (password: "SecretPaw123" for all cats)

-- Insert Cats
INSERT INTO cats (id, name, password, years_of_experience, breed, salary, is_staff, created_at, updated_at) VALUES
(1, 'Whiskers', '$2b$12$KVEPmOXqjEGpBVgi2.Sz0OlTC2QfXie2ifjy.DraHmA4CrBSQAswK', 5, 'Siamese', 75000, false, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
(2, 'Shadow', '$2b$12$KVEPmOXqjEGpBVgi2.Sz0OlTC2QfXie2ifjy.DraHmA4CrBSQAswK', 8, 'British Shorthair', 95000, true, '2023-06-20 14:45:00', '2024-03-10 09:15:00'),
(3, 'Luna', '$2b$12$KVEPmOXqjEGpBVgi2.Sz0OlTC2QfXie2ifjy.DraHmA4CrBSQAswK', 3, 'Maine Coon', 60000, false, '2024-03-05 08:00:00', '2024-03-05 08:00:00'),
(4, 'Felix', '$2b$12$KVEPmOXqjEGpBVgi2.Sz0OlTC2QfXie2ifjy.DraHmA4CrBSQAswK', 2, 'Persian', 50000, false, '2024-05-12 16:20:00', '2024-05-12 16:20:00'),
(5, 'Mittens', '$2b$12$KVEPmOXqjEGpBVgi2.Sz0OlTC2QfXie2ifjy.DraHmA4CrBSQAswK', 10, 'Ukrainian Levkoy', 120000, true, '2022-11-08 11:00:00', '2024-02-28 13:30:00');

-- Insert Missions
INSERT INTO missions (id, name, description, is_completed, created_at, updated_at) VALUES
(1, 'Operation Red Laser', 'Investigate suspicious laser pointer activity in warehouse district', false, '2024-02-01 09:00:00', '2024-02-01 09:00:00'),
(2, 'Tuna Heist Prevention', 'Prevent theft of valuable tuna shipment at the docks', true, '2024-01-10 12:30:00', '2024-01-25 18:45:00'),
(3, 'Catnip Cartel Takedown', 'Infiltrate and dismantle illegal catnip distribution network', false, '2024-03-15 07:15:00', '2024-03-15 07:15:00'),
(4, 'The Mouse Conspiracy', 'Uncover the truth behind the missing laboratory mice', false, '2024-04-20 10:00:00', '2024-04-20 10:00:00'),
(5, 'Yarn Ball Sabotage', 'Protect national yarn ball reserves from foreign agents', true, '2023-12-05 14:00:00', '2024-01-08 16:20:00');

-- Assign Cats to Missions (many-to-many relationships)
-- Mission 1: Whiskers and Shadow
-- Mission 2: Luna (completed)
-- Mission 3: Felix only
-- Mission 4: No cats assigned yet
-- Mission 5: Mittens only (completed)
INSERT INTO mission_cat (mission_id, cat_id) VALUES
(1, 1),  -- Whiskers on Operation Red Laser
(1, 2),  -- Shadow on Operation Red Laser
(2, 3),  -- Luna on Tuna Heist Prevention
(3, 4),  -- Felix on Catnip Cartel Takedown
(5, 5);  -- Mittens on Yarn Ball Sabotage

-- Insert Targets
INSERT INTO targets (id, name, country, is_completed, mission_id, created_at, updated_at) VALUES
(1, 'Dr. Evil Whiskers', 'Switzerland', false, 1, '2024-02-02 11:00:00', '2024-02-02 11:00:00'),
(2, 'The Red Dot Mastermind', 'Japan', false, 1, '2024-02-03 15:30:00', '2024-02-03 15:30:00'),
(3, 'Captain Fishbeard', 'Norway', true, 2, '2024-01-11 08:45:00', '2024-01-25 17:00:00'),
(4, 'El Gato Loco', 'Mexico', false, 3, '2024-03-16 09:20:00', '2024-03-16 09:20:00'),
(5, 'Professor Squeaks', 'United Kingdom', false, 4, '2024-04-21 13:10:00', '2024-04-21 13:10:00'),
(6, 'The Knitting Needle', 'France', true, 5, '2023-12-06 10:30:00', '2024-01-08 15:45:00'),
(7, 'Agent Meowiarty', 'Ukraine', false, 3, '2024-03-18 16:00:00', '2024-03-18 16:00:00');

-- Insert Notes
INSERT INTO notes (id, content, cat_id, target_id, created_at, updated_at) VALUES
(1, 'Target spotted near the warehouse at 3 AM. Very suspicious.', 1, 1, '2024-02-05 03:15:00', '2024-02-05 03:15:00'),
(2, 'Successfully intercepted communication between targets.', 3, 3, '2024-01-20 19:30:00', '2024-01-20 19:30:00'),
(3, 'Target has an unusual obsession with laser pointers.', 1, 2, '2024-02-08 14:22:00', '2024-02-08 14:22:00'),
(4, 'Mission accomplished! Tuna shipment secured.', 3, 3, '2024-01-25 17:50:00', '2024-01-25 17:50:00'),
(5, 'Undercover operation proceeding as planned. Target suspects nothing.', 4, 4, '2024-03-20 11:40:00', '2024-03-20 11:40:00'),
(6, 'Need backup. This catnip operation is bigger than we thought.', 4, 7, '2024-03-22 23:15:00', '2024-03-22 23:15:00'),
(7, 'Target eliminated. Yarn reserves are safe.', 5, 6, '2024-01-08 16:00:00', '2024-01-08 16:00:00');

-- Reset sequences to continue from current max IDs
SELECT setval('cats_id_seq', (SELECT MAX(id) FROM cats));
SELECT setval('missions_id_seq', (SELECT MAX(id) FROM missions));
SELECT setval('targets_id_seq', (SELECT MAX(id) FROM targets));
SELECT setval('notes_id_seq', (SELECT MAX(id) FROM notes));
