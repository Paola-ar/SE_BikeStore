from database.DB_connect import DBConnect
from model.product import Product
from model.category import Category

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_all_categories():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM category"

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_all_products_by_category(cat):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                        FROM product
                        WHERE category_id = %s """

        cursor.execute(query, (cat.id,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_edges(cat, d1, d2, id_map):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t1.id AS n1, t2.id AS n2, t1.num+t2.num AS peso
                        FROM (SELECT p.id , count(*) AS num
                              FROM product p, order_item oi, `order` o 
                              WHERE p.id = oi.product_id AND oi.order_id = o.id 
                                    AND o.order_date BETWEEN %s AND %s
                                    AND p.category_id = %s
                                    GROUP BY (p.id)
                                    ORDER BY p.id ) t1, 
                             (SELECT p.id , count(*) AS num
                              FROM product p, order_item oi, `order` o 
                              WHERE p.id = oi.product_id AND oi.order_id = o.id 
                                    AND o.order_date BETWEEN %s AND %s
                                    AND p.category_id = %s
                              GROUP BY (p.id)
                              ORDER BY p.id ) t2
                       WHERE t1.num >= t2.num
                             AND t1.id <> t2.id
                       ORDER BY peso DESC, n1 ASC, n2 ASC """

        cursor.execute(query, (d1, d2, cat.id, d1, d2, cat.id))

        for row in cursor:
            results.append((id_map[row["n1"]], id_map[row["n2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results