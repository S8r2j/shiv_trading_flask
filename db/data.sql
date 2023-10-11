INSERT INTO products(p_id, product_name)
VALUES
    (1, 'Wall Tiles'),
    (2, 'Floor Tiles'),
    (3, 'Sanitary and CP Fittings'),
    (4, 'Granite and Marbles');

INSERT INTO sizes(s_id,sizes)
VALUES
    (1,'12×18inch'),
    (2,'24×12inch'),
    (3,'24×24inch'),
    (4,'24×48inch'),
    (5,'32×32inch'),
    (6,'12×12inch'),
    (7,'16×16inch');

INSERT INTO rooms(room_id,room_name)
VALUES
    (1,'Bedroom'),
    (2,'Livingroom'),
    (3,'Outdoor'),
    (4,'Kitchen'),
    (5,'Bathroom'),
    (6,'Parking');

INSERT INTO cpfittings(fitting_id,fitting_name)
VALUES
    (1,'Single Piece Basin'),
    (2,'Two Piece Basin'),
    (3,'Counter Basin'),
    (4,'Wall Hung Commote'),
    (5,'Double Vacuum Commote'),
    (6,'Single Vacuum Commote');


INSERT INTO product_room_size(prs_id,p_id,room_id,s_id)
VALUES
    (1,1,1,1),
    (2,1,1,2),
    (3,1,1,3),
    (4,1,1,4),
    (5,1,2,1),
    (6,1,2,2),
    (7,1,2,3),
    (8,1,2,4),
    (9,1,3,1),
    (10,1,3,2),
    (11,1,3,3),
    (12,1,3,4),
    (13,1,4,1),
    (14,1,4,2),
    (15,1,4,3),
    (16,1,4,4),
    (17,1,5,1),
    (18,1,5,2),
    (19,1,5,3),
    (20,1,5,4),
    (21,2,1,6),
    (22,2,1,3),
    (23,2,1,4),
    (24,2,1,5),
    (25,2,2,6),
    (26,2,2,3),
    (27,2,2,4),
    (28,2,2,5),
    (29,2,3,6),
    (30,2,3,3),
    (31,2,3,4),
    (32,2,3,5),
    (33,2,4,6),
    (34,2,4,3),
    (35,2,4,4),
    (36,2,4,5),
    (37,2,5,6),
    (38,2,5,3),
    (39,2,5,4),
    (40,2,5,5),
    (41,2,6,7),
    (42,2,6,6);

INSERT INTO product_fitting(p_fitting_id,p_id,fitting_id)
VALUES
    (1,3,1),
    (2,3,2),
    (3,3,3),
    (4,3,4),
    (5,3,5);

INSERT INTO granites(granite_id,category)
VALUES
    (1,'Rajasthani'),
    (2,'South Indian'),
    (3,'North Indian');

INSERT INTO thick(thick_id,thick)
VALUES
    (1,'11mm'),
    (2,'13mm'),
    (3,'15mm'),
    (4,'18mm');

INSERT INTO granitethick(gt_id,granite_id,thick_id,p_id)
VALUES
    (1,1,1,4),
    (2,1,2,4),
    (3,1,3,4),
    (4,1,4,4),
    (5,2,1,4),
    (6,2,2,4),
    (7,2,3,4),
    (8,2,4,4),
    (9,3,1,4),
    (10,3,2,4),
    (11,3,3,4),
    (12,3,4,4)