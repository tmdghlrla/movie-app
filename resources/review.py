from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from flask_restful import Resource

from mysql.connector import Error
from mysql_connection import get_connection

class ReviewResource(Resource) :
    @jwt_required()
    def get(self, movieId) :
        try :
            connection = get_connection()
            query = '''select u.id, u.nickname, u.gender, r.rating, r.createdAt, r.updatedAt
                        from review as r
                        join user as u
                        on u.id = r.userId
                        where r.movieId = %s
                        order by r.createdAt desc;'''
            
            record = (movieId,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
                i = i+1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500
        
        return {"result" : "success",
                "items" : result_list,
                "count" : len(result_list)}, 200
    
    @jwt_required()
    def post(self, movieId) :
        data = request.get_json()
        userId = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into review
                    (movieId, userId, rating, content)
                    values
                    (%s, %s, %s, %s);'''
            record = (movieId, userId, data['rating'], data['content'])

            cursor = connection.cursor()
            cursor.execute(query, record)            
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500
        
        return {"result" : "success"}, 200