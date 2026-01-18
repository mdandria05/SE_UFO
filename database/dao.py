from database.DB_connect import DBConnect
from model.state import State as s
class DAO:
    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """SELECT DISTINCT YEAR(s_datetime) FROM sighting ORDER BY s_datetime ASC;"""

        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """SELECT DISTINCT shape FROM sighting;"""

        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes(shape, year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT 
                    st.id,
                    st.lat,
                    st.lng, 
                    (COUNT(s.shape) + COUNT(s.s_datetime)) as weight
                    FROM state st
                    LEFT JOIN sighting s ON st.id = s.state 
                        AND s.shape = %s 
                        AND YEAR(s.s_datetime) = %s
                        GROUP BY st.id  
                    ORDER BY st.id ASC;"""

        #ATTENZIONE ad utilizzare il WHERE con il LEFT JOIN, avrebbe la priorità, invece con l' ON ricadrebbe sul LEFT JOIN

        cursor.execute(query,(shape,year))

        for row in cursor:
            result.append(s(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """SELECT * FROM neighbor"""

        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

