info = {
    "db": "mydb",
    "host": "localhost",
    "user": "root",
    "passwd": "root",
    "port": 3306,
    "charset": "utf8"
}


# CREATE TABLE `client` (
#   `client_id` INT NOT NULL AUTO_INCREMENT,
#   `name` VARCHAR(10) NOT NULL,
#   `grade` VARCHAR(5) NOT NULL,
#   `phone` VARCHAR(20) NULL,
#   PRIMARY KEY (`client_id`));
#
# CREATE TABLE `purchase` (
#   `client_id` INT NOT NULL,
#   `product_name` VARCHAR(20) NOT NULL,
#   `price` INT NOT NULL,
#   `buy_price` INT NOT NULL,
#   `date` DATETIME NOT NULL DEFAULT NOW(),
#     FOREIGN KEY (`client_id`)
#     REFERENCES `client` (`client_id`)
#     ON DELETE CASCADE
#     ON UPDATE NO ACTION);
#
# create view all_info as
# select a.name as "이름", IFNULL(b.cnt, 0) as "거래수",
#         IFNULL(b.p,0) as "원가합", IFNULL(b.bp,0) as "구매금액합"
#         from client as a left outer join(
#         	select client_id, count(*) as cnt, sum(price) as p, sum(buy_price) as bp
#         	from purchase
#         	group by client_id
#         ) as b on a.client_id = b.client_id
#         order by b.p desc;
#
# create view search_view as select name, phone, grade from client;
#
# create view purchase_client_view as select a.name, b.product_name, b.price, a.grade, b.buy_price, b.date from client as a, purchase as b where a.client_id=b.client_id;