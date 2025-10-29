BEGIN;

DROP TABLE IF EXISTS service_ticket_parts CASCADE;
DROP TABLE IF EXISTS service_mechanic CASCADE;
DROP TABLE IF EXISTS ticket_parts CASCADE;
DROP TABLE IF EXISTS ticket_mechanics CASCADE;
DROP TABLE IF EXISTS service_ticket CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS mechanic CASCADE;


CREATE TABLE mechanic (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL,
    specialty VARCHAR(100) NOT NULL
);

INSERT INTO mechanic (id, name, email, password_hash, specialty) VALUES
(1,'Admin','admin@shop.com','scrypt:32768:8:1$s4lh9pYQdGn6H77i$736617d990f124a0e38c012963226b34fcae6a7c5d1f193711c76884fd5ddaffc281d1a3a5dff2722b53c8ceb5efe8eb7e5ca16fbaf8c6c57da3d00f46ef1da0','Manager'),
(2,'Alex','alex@shop.com','scrypt:32768:8:1$SzKLhjiJlWBVciDA$035f2d2c81322e8639684d807d583407305edfca76d6d8012969af5d58dffcedb72f422d0d1ee4baa25c60457d6b136800233f1da6ce3d2f21782a0db5415b96','Brakes'),
(3,'Maria','maria@shop.com','scrypt:32768:8:1$WEhD6RwYEsgUgLm3$0f3aa4776b4341b4c1273741f25dc80cc52189ca8ab5c1575d53565f497fc4cf95cfc971bfe7898aaf1e2d39d58afec0b395cfce86234d24be9effeec6b65579','Transmission'),
(4,'Tyler','tyler@shop.com','scrypt:32768:8:1$iCGg421Wv1iwNXG8$810f192dc295743701cfcb4baa6f34ab687678a25c6b2fec4155947e719c8e49e1a8b0faea1619eece9d77773958caddeae2f642971f247857f34639d100151f','Diagnostics'),
(5,'Sasha','sasha@shop.com','scrypt:32768:8:1$l8fLRTvAO0gb9lGu$0a71be5a026fbfe98f1c762f87516d3753b41e898e66c41e09d35443cf500cba8fd346020cb08578ab7683c6ca165f6605a9325ff375448a9e19a0207251e670','Suspension'),
(6,'Jordan','jordan@shop.com','scrypt:32768:8:1$jvMbMwQ0rgyMn6C6$57523657d03794106900186cf6eea49fbdd2abf1f320f2a3dc7b83c050141606f71bad6fcfc341605feb2ec390ceb4e900f7ccfbba59ab4de930e7d96b756eb2','Electrical'),
(7,'Ravi','ravi@shop.com','scrypt:32768:8:1$SzNUsXt2GAkXwuBc$5308bce7786113c40a8048bf3fbcd9c69412caae15f60d238445fd6e000933ff29ea48961370d82f7765eef409d5ff15fd6e9f54e15c438507a781a86164ea72','Engine Repair'),
(8,'Nina','nina@shop.com','scrypt:32768:8:1$Wz3Fjnm9tTmsJGB9$aa6c3ec1eede116757aed5a04ae5f0d91cf56b723d06c5f05b07216e61e9d0cb64cd390896c4d44fdca21d72da2125cae2b98e147fae62cf4eb2ebac6d5b2efa','Body Work');

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    car VARCHAR(100) NOT NULL
);

INSERT INTO customer (id, name, email, phone, car) VALUES
(1,'John Doe','john@example.com','312-555-1111','Honda Civic'),
(2,'Jane Smith','jane@example.com','312-555-2222','Toyota Camry'),
(3,'Luis Martinez','luis@example.com','773-555-3333','Ford F-150'),
(4,'Emily Davis','emily@example.com','847-555-4444','Subaru Outback'),
(5,'Mike Johnson','mike@example.com','630-555-5555','Chevrolet Malibu'),
(6,'Olivia Brown','olivia@example.com','224-555-6666','BMW 3 Series'),
(7,'Noah Wilson','noah@example.com','708-555-7777','Hyundai Sonata'),
(8,'Ava Lee','ava@example.com','815-555-8888','Kia Sportage'),
(9,'Ethan Clark','ethan@example.com','219-555-9999','Mazda CX-5'),
(10,'Sophia Turner','sophia@example.com','309-555-0000','Nissan Altima');

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    quantity INTEGER NOT NULL
);

INSERT INTO inventory (id, name, price, quantity) VALUES
(1,'Brake Pads',49.99,30),
(2,'Oil Filter',9.99,100),
(3,'Air Filter',14.99,60),
(4,'Spark Plugs',5.49,120),
(5,'Timing Belt',89.99,20),
(6,'Alternator',199.99,10),
(7,'Battery',129.99,15),
(8,'Radiator',179.99,8),
(9,'Headlight Bulb',24.99,40),
(10,'Wiper Blades',12.99,50),
(11,'Fuel Pump',149.99,6),
(12,'Engine Oil (5qt)',29.99,75);

CREATE TABLE service_ticket (
    id SERIAL PRIMARY KEY,
    description VARCHAR(200) NOT NULL,
    date TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customer(id)
);

INSERT INTO service_ticket (id, description, date, status, customer_id) VALUES
(1,'Brake pad replacement','2025-10-29 08:35:12.398850','In Progress',1),
(2,'Oil change','2025-10-29 08:35:12.398856','Closed',2),
(3,'Engine diagnostics','2025-10-29 08:35:12.398857','Open',3),
(4,'Replace alternator','2025-10-29 08:35:12.398857','In Progress',4),
(5,'Install new timing belt','2025-10-29 08:35:12.398858','Open',5),
(6,'Battery replacement','2025-10-29 08:35:12.398858','Closed',6),
(7,'Suspension inspection','2025-10-29 08:35:12.398859','In Progress',7),
(8,'Body work estimate','2025-10-29 08:35:12.398859','Open',10);

CREATE TABLE ticket_mechanics (
    service_ticket_id INTEGER REFERENCES service_ticket(id),
    mechanic_id INTEGER REFERENCES mechanic(id)
);

INSERT INTO ticket_mechanics (service_ticket_id, mechanic_id) VALUES
(7,5),
(8,1),
(2,3),
(5,3),
(6,6),
(4,7),
(5,7),
(8,8),
(1,2),
(7,2),
(3,4);

CREATE TABLE ticket_parts (
    service_ticket_id INTEGER REFERENCES service_ticket(id),
    inventory_id INTEGER REFERENCES inventory(id)
);

COMMIT;
