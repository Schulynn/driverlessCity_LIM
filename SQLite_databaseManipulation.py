# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 10:13:27 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project
"""

class SQLite_handle():
    def __init__(self,db_file):
        self.db_file=db_file
    
    
    
    def create_connection(self):
        import sqlite3
        from sqlite3 import Error
        """ create a database connection to a SQLite database """
        conn=None
        try:
            conn=sqlite3.connect(self.db_file)
            print('connected.',"SQLite version:%s"%sqlite3.version,)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
                
                
from sqlalchemy import Column, Integer, String


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# 定义映射类User，其继承上一步创建的Base
class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'users'
    # 如果有多个类指向同一张表，那么在后边的类需要把extend_existing设为True，表示在已有列基础上进行扩展
    # 或者换句话说，sqlalchemy允许类是表的字集
    # __table_args__ = {'extend_existing': True}
    # 如果表在同一个数据库服务（datebase）的不同数据库中（schema），可使用schema参数进一步指定数据库
    # __table_args__ = {'schema': 'test_database'}
    
    # 各变量名一定要与表的各字段名一样，因为相同的名字是他们之间的唯一关联关系
    # 从语法上说，各变量类型和表的类型可以不完全一致，如表字段是String(64)，但我就定义成String(32)
    # 但为了避免造成不必要的错误，变量的类型和其对应的表的字段的类型还是要相一致
    # sqlalchemy强制要求必须要有主键字段不然会报错，如果要映射一张已存在且没有主键的表，那么可行的做法是将所有字段都设为primary_key=True
    # 不要看随便将一个非主键字段设为primary_key，然后似乎就没报错就能使用了，sqlalchemy在接收到查询结果后还会自己根据主键进行一次去重
    # 指定id映射到id字段; id字段为整型，为主键，自动增长（其实整型主键默认就自动增长）
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形，
    name = Column(String(20))
    fullname = Column(String(32))
    password = Column(String(32))

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)                
                
def get_dynamic_table_name_class(table_name):
    # 定义一个内部类
    class TestModel(Base):
        # 给表名赋值
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}

        username = Column(String(32), primary_key=True)
        password = Column(String(32))
    # 把动态设置表名的类返回去
    return TestModel

                
                
                
if __name__=="__main__":
    db_file=r'./database/testdb.db'
    sqlH=SQLite_handle(db_file)
    sqlH.create_connection()
    
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///C:\\Users\\richi\\omen-richiebao_s\\omen_github\\driverlessCity_LIM\\database\\foo.db',echo=True)    
    print(User.__table__)
    #Base.metadata.create_all(engine, checkfirst=True)
    Base.metadata.create_all(engine,tables=[Base.metadata.tables['users']],checkfirst=True)
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    session.add(ed_user)
    session.add_all(
        [User(name='wendy', fullname='Wendy Williams', password='foobar'),
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='blah')]
        )    
    session.commit()
    
    our_user = session.query(User).filter_by(name='ed').first()
    print( our_user,ed_user is our_user)
    
    mod_user = session.query(User).filter_by(name='ed').first()
    mod_user.password = 'modify_passwd'
    session.commit()

    
    
    
    
    
    
    
    

    
    