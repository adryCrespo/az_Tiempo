CREATE TABLE IF NOT EXISTS ciudades (
    ciudad TEXT,
    fecha  text,
    t_min NUMERIC(10,2),
    t_max NUMERIC(10,2)
    );

INSERT INTO ciudades (ciudad,fecha, t_min, t_max)
VALUES
    ('madrid', '01-11-2024', 10,11),
    ('madrid', '02-11-2024', 11,12),
    ('madrid', '03-11-2024', 12,13),
    ('getafe', '01-11-2024', 10.5,11),
    ('getafe', '02-11-2024', 11.5,12),
    ('getafe', '03-11-2024', 12.5,13);