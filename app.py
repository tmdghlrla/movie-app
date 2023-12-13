from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.movie import MovieDetailResource, MovieResource, MovieSearchResource
from resources.review import ReviewResource

from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource
# 로그아웃 관련된 임포트문
from resources.user import jwt_blocklist

app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)
# JWT 매니저 초기화
jwt=JWTManager(app)

# 로그아웃된 토큰으로 요청하는 경우 실행되지 않도록 처리하는 코드
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app)

# 경로와 리소스를 연결한다.
api.add_resource(UserRegisterResource, '/user/register') # 회원가입
api.add_resource(UserLoginResource, '/user/login') # 로그인
api.add_resource(UserLogoutResource, '/user/logout') # 로그아웃
api.add_resource(MovieResource, '/movie') # 영화정보
api.add_resource(MovieDetailResource, '/movie/<int:movieId>') # 영화 상세정보
api.add_resource(MovieSearchResource, '/movie/search/<string:find>') # 영화 찾기
api.add_resource(ReviewResource, '/movie/<int:movieId>/review') # 영화 리뷰



if __name__ == '__main__' :
    app.run()