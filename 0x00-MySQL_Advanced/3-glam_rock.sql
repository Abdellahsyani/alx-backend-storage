-- writing a sql script that lists all bands
-- band_name using IFNULL and FIND_IN_SET
SELECT band_name, (IFNULL(split, '2020') - formed) AS lifespan
	FROM metal_bands
	WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
	ORDER BY lifespan DESC;
