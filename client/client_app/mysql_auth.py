info = {
    "db": "mydb",
    "host": "localhost",
    "user": "root",
    "passwd": "root",
    "port": "3306",
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
# CREATE TABLE `grade_table` (
#   `grade` VARCHAR(5) NOT NULL,
#   `discount` INT NOT NULL
# );
#
# insert into grade_table(grade, discount) values("A", 20);
# insert into grade_table(grade, discount) values("B", 15);
# insert into grade_table(grade, discount) values("C", 10);
# insert into grade_table(grade, discount) values("D", 5);
# insert into grade_table(grade, discount) values("E", 0);
#
# create view all_info as
# select a.name as "name", IFNULL(b.cnt, 0) as "purchase_count",
#         IFNULL(b.p,0) as "sum_price", IFNULL(b.bp,0) as "sum_buyprice"
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