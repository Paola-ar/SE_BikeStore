from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product

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
    def get_category():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM category"""
        cursor.execute(query)
        for row in cursor:
            results.append(Category(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_products_by_cat(category):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select p.id,p.product_name, p.brand_id, p.category_id, p.model_year, p.list_price
                    from product p, category c 
                    where p.category_id = c.id
                    and c.category_name = 'Road Bikes'"""
        cursor.execute(query)
        for row in cursor:
            results.append(Product(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_edges(cat,date1,date2,id_prod_map):
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
                       ORDER BY peso DESC, n1 ASC, n2 ASC"""
        # t1.num >= t2.num peso deve essere maggiore cosi elimina il viceversa
        cursor.execute(query,(date1,date2,cat.id,date1,date2,cat.id))
        for row in cursor:
            results.append((id_prod_map[row["n1"]],id_prod_map[row["n2"]],row["peso"])) #per archi aggiungo sempre tuple
        cursor.close()
        conn.close()
        return results





