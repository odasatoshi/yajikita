CREATE TABLE RACE_FIELD (
    id INTEGER PRIMARY KEY,
    name TEXT,
    checkpoint_num INTEGER,
    distance REAL
);

CREATE TABLE FIELD_DETAIL (
    field_id INTEGER,
    waypoint_id INTEGER,
    name TEXT,
    distance REAL,
    PRIMARY KEY (field_id, waypoint_id)
);

INSERT INTO RACE_FIELD VALUES(0, "東海道五拾三次", 54, 495.5);
INSERT INTO RACE_FIELD VALUES(1, "箱根駅伝", 10, 217.1);

INSERT INTO FIELD_DETAIL VALUES(0,0,"江戸",0);
INSERT INTO FIELD_DETAIL VALUES(0,1,"品川",7.8);
INSERT INTO FIELD_DETAIL VALUES(0,2,"川崎",9.8);
INSERT INTO FIELD_DETAIL VALUES(0,3,"神奈川",9.8);
INSERT INTO FIELD_DETAIL VALUES(0,4,"程ヶ谷",4.9);
INSERT INTO FIELD_DETAIL VALUES(0,5,"戸塚",8.8);
INSERT INTO FIELD_DETAIL VALUES(0,6,"藤沢",7.8);
INSERT INTO FIELD_DETAIL VALUES(0,7,"平塚",13.7);
INSERT INTO FIELD_DETAIL VALUES(0,8,"大磯",3);
INSERT INTO FIELD_DETAIL VALUES(0,9,"小田原",15.7);
INSERT INTO FIELD_DETAIL VALUES(0,10,"箱根",16.6);
INSERT INTO FIELD_DETAIL VALUES(0,11,"三島",14.8);
INSERT INTO FIELD_DETAIL VALUES(0,12,"沼津",5.9);
INSERT INTO FIELD_DETAIL VALUES(0,13,"原",5.9);
INSERT INTO FIELD_DETAIL VALUES(0,14,"吉原",11.8);
INSERT INTO FIELD_DETAIL VALUES(0,15,"蒲原",11.2);
INSERT INTO FIELD_DETAIL VALUES(0,16,"由井",3.9);
INSERT INTO FIELD_DETAIL VALUES(0,17,"興津",9.2);
INSERT INTO FIELD_DETAIL VALUES(0,18,"江尻",4.1);
INSERT INTO FIELD_DETAIL VALUES(0,19,"府中",10.6);
INSERT INTO FIELD_DETAIL VALUES(0,20,"丸子",5.7);
INSERT INTO FIELD_DETAIL VALUES(0,21,"岡部",7.8);
INSERT INTO FIELD_DETAIL VALUES(0,22,"藤枝",6.8);
INSERT INTO FIELD_DETAIL VALUES(0,23,"島田",8.7);
INSERT INTO FIELD_DETAIL VALUES(0,24,"金谷",3.9);
INSERT INTO FIELD_DETAIL VALUES(0,25,"日坂",6.6);
INSERT INTO FIELD_DETAIL VALUES(0,26,"掛川",7.1);
INSERT INTO FIELD_DETAIL VALUES(0,27,"袋井",9.6);
INSERT INTO FIELD_DETAIL VALUES(0,28,"見付",5.9);
INSERT INTO FIELD_DETAIL VALUES(0,29,"浜松",16.5);
INSERT INTO FIELD_DETAIL VALUES(0,30,"舞阪",11.1);
INSERT INTO FIELD_DETAIL VALUES(0,31,"新井",5.9);
INSERT INTO FIELD_DETAIL VALUES(0,32,"白須賀",6.6);
INSERT INTO FIELD_DETAIL VALUES(0,33,"二川",5.8);
INSERT INTO FIELD_DETAIL VALUES(0,34,"吉田",6.1);
INSERT INTO FIELD_DETAIL VALUES(0,35,"御油",10.2);
INSERT INTO FIELD_DETAIL VALUES(0,36,"赤坂",1.8);
INSERT INTO FIELD_DETAIL VALUES(0,37,"藤川",8.8);
INSERT INTO FIELD_DETAIL VALUES(0,38,"岡崎",6.7);
INSERT INTO FIELD_DETAIL VALUES(0,39,"池鯉鮒",14.9);
INSERT INTO FIELD_DETAIL VALUES(0,40,"鳴海",11.1);
INSERT INTO FIELD_DETAIL VALUES(0,41,"宮",6.6);
INSERT INTO FIELD_DETAIL VALUES(0,42,"桑名",27.4);
INSERT INTO FIELD_DETAIL VALUES(0,43,"四日市",12.6);
INSERT INTO FIELD_DETAIL VALUES(0,44,"石薬師",10.8);
INSERT INTO FIELD_DETAIL VALUES(0,45,"庄野",2.8);
INSERT INTO FIELD_DETAIL VALUES(0,46,"亀山",7.8);
INSERT INTO FIELD_DETAIL VALUES(0,47,"関",5.9);
INSERT INTO FIELD_DETAIL VALUES(0,48,"坂ノ下",6.6);
INSERT INTO FIELD_DETAIL VALUES(0,49,"土山",9.8);
INSERT INTO FIELD_DETAIL VALUES(0,50,"水口",10.6);
INSERT INTO FIELD_DETAIL VALUES(0,51,"石部",13.7);
INSERT INTO FIELD_DETAIL VALUES(0,52,"草津",11.8);
INSERT INTO FIELD_DETAIL VALUES(0,53,"大津",14.4);
INSERT INTO FIELD_DETAIL VALUES(0,54,"京",11.8);
INSERT INTO FIELD_DETAIL VALUES(1,0,"大手町",0);
INSERT INTO FIELD_DETAIL VALUES(1,1,"鶴見",21.3);
INSERT INTO FIELD_DETAIL VALUES(1,2,"戸塚",23.1);
INSERT INTO FIELD_DETAIL VALUES(1,3,"平塚",21.4);
INSERT INTO FIELD_DETAIL VALUES(1,4,"小田原",20.9);
INSERT INTO FIELD_DETAIL VALUES(1,5,"箱根",20.8);
INSERT INTO FIELD_DETAIL VALUES(1,6,"小田原",20.8);
INSERT INTO FIELD_DETAIL VALUES(1,7,"平塚",21.3);
INSERT INTO FIELD_DETAIL VALUES(1,8,"戸塚",21.4);
INSERT INTO FIELD_DETAIL VALUES(1,9,"鶴見",23.1);
INSERT INTO FIELD_DETAIL VALUES(1,10,"大手町",23);

