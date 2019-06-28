CREATE TABLE `face_info` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`format`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`userid`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`width`  int(11) NULL DEFAULT NULL ,
`height`  int(11) NULL DEFAULT NULL ,
`channel`  int(11) NULL DEFAULT NULL ,
`facebytes`  blob NULL ,
`features`  blob NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=38
ROW_FORMAT=DYNAMIC
;