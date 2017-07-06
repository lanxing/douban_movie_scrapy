from peewee import *

db = MySQLDatabase('movie', user='root')


# 基础模板
class BaseModel(Model):
    class Meta:
        database = db


# 电影打平表
class MovieDetailModel(BaseModel):
    # 名称
    name = CharField(unique=True, max_length=256)

    # 年份
    year = IntegerField()

    # 区域(list)
    region = CharField(max_length=256)

    # 评级
    stars = FloatField()

    # 上映日期(list列表)
    runtime = CharField(max_length=256)

    # 类型（list列表）
    types = CharField(max_length=256)

    # 导演（list列表）
    directors = CharField(max_length=256)

    # 主演（list列表）
    actors = CharField(max_length=2048)

    # 语言
    language = CharField(max_length=256)

    # 时长（分钟）
    duration = IntegerField()

    # 详情链接
    detailurl = CharField(max_length=256)

    # IMDB链接
    IMDburl = CharField(max_length=256)


# class MovieDetail(BaseModel):
#     # 名称
#     name = CharField(unique=True, max_length=256)
#     year = IntegerField()
#     region = CharField(max_length=256, index=True)
#     stars = DoubleField()
#     types = CharField(max_length=256)
#     directors = CharField(max_length=256)

def createTable(table):
    db.connect()
    db.create_table(table)


# 保存电影数据
def saveMovie(item):
    name = item.get('name')
    year = item.get('year')
    region = item.get('region')
    stars = item.get('stars')
    runtime = item.get('runtime')
    types = item.get('types')
    directors = item.get('directors')
    actors = item.get('actors')
    language = item.get('language')
    duration = item.get('duration')
    detailurl = item.get('detailurl')
    IMDburl = item.get('IMDburl')

    if name is not None:
        name = name[0]
    if year is not None:
        year = int(year[0])
    if region is not None:
        region = region[0].strip()
    if stars is not None:
        stars = float(stars[0])
    if directors is not None:
        directors = directors[0]
    if duration is not None:
        duration = int(duration[0])
    if detailurl is not None:
        detailurl = detailurl[0]
    if IMDburl is not None:
        IMDburl = IMDburl[0]

    MovieDetailModel.create(name=name, year=year, region=region, stars=stars, runtime=runtime, types=types, directors=directors, actors=actors,
                            language=language, duration=duration, detailurl=detailurl, IMDburl=IMDburl)


# createTable(MovieDetailModel)
