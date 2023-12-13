from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from flask_restful import Resource

from mysql.connector import Error
from mysql_connection import get_connection

class MovieResource(Resource) :         # 영화정보
    @jwt_required()
    def get(self) :
        
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select m.id, m.title, count(r.id) as countReview, avg(r.rating) as avgRating, m.createdAt
                        from movie as m
                        left join review as r
                        on m.id = r.movieId
                        group by m.id
                        order by countReview desc, avgRating desc
                        limit ''' + offset + ''', ''' + limit + ''';'''
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['avgRating'] = float(row['avgRating'])
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
    
class MovieDetailResource(Resource) :
    @jwt_required()
    def get(self, movieId) :
        try :
            connection = get_connection()
            query = '''select m.id, m.title, m.summary, m.year, m.attendance, avg(r.rating) as ratingAvg, count(r.id) as reviewCnt, r.createdAt, r.updatedAt
                        from movie as m
                        left join review as r
                        on m.id = r.movieId
                        where m.id = %s
                        group by m.id;'''
            record = (movieId, )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['year'] = row['year'].isoformat()
                result_list[i]['ratingAvg'] = float(row['ratingAvg'])
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
                "item" : result_list}, 200
    
class MovieSearchResource(Resource) :
    @jwt_required()
    def get(self, find) :
        try :
            connection = get_connection()
            query = '''select m.id, m.title, count(r.id)as reviewCnt, avg(r.rating) as ratingAvg, r.createdAt, r.updatedAt
                        from movie as m
                        left join review as r
                        on m.id = r.movieId
                        group by m.id
                        having m.title like CONCAT('%',%s,'%')
                        order by reviewCnt desc;'''

            record = (find,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                if result_list[i]['createdAt'] != None :
                    result_list[i]['ratingAvg'] = float(row['ratingAvg'])
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