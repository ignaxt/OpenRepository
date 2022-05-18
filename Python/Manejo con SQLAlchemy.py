from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Sequence,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased,relationship
from sqlalchemy.sql import exists ##Importo la clase exists para preguntar si existe
from sqlalchemy import Table,Text

Base=declarative_base()

engine= create_engine('sqlite:///:memory:')





##Relacion Muchos a Muchos
#Tabla de Relacion o intermedia
book_categories=Table('book_categories',Base.metadata,
                    Column('book_id',ForeignKey('book.id'),primary_key=True),
                    Column('category_id',ForeignKey('book_category.id'),primary_key=True)
)

class Author(Base):
    __tablename__='author'
    id=Column(Integer,Sequence('author_id_seq'),primary_key=True)
    firstname=Column(String)
    lastname=Column(String)
    books=relationship("Book",order_by='Book.id',back_populates='author',cascade="all,delete,delete-orphan")

    def __repr__(self):
        return "{} {}".format(self.firstname,self.lastname)

class Book(Base):
    __tablename__='book'
    id=Column(Integer,Sequence('book_id_seq'),primary_key=True)
    isbn=Column(String)
    title=Column(String)
    description=Column(String)
    author_id=Column(Integer,ForeignKey('author.id'))

    author=relationship("Author",order_by='Author.id',back_populates='books')
    categories=relationship('BookCategory',
                        secondary=book_categories,  ##Indico que es una tabla secundaria
                        back_populates='books')

    def __repr__(self) -> str:
        return "{}".format(self.title)

class BookCategory(Base):
    __tablename__='book_category'
    id=Column(Integer,Sequence('book_category_id_seq'),primary_key=True)
    name=Column(String)

    books=relationship('Book',
                        secondary=book_categories,  ##Indico que es una tabla secundaria
                        back_populates='categories')
    
    def __repr__(self) -> str:
        return "{}".format(self.name)

Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)

session=Session()

j_rowling=Author(firstname='Joanne',lastname='Rowling')
print(j_rowling.books)



author=Author(firstname='Pedro',lastname='Rowling')
author2=Author(firstname='Mario',lastname='Rowling')
author3=Author(firstname='Ramon',lastname='Rowling')

session.add_all([author,author2,author3])

j_rowling.books=[Book(isbn='123456789',title='Harry Potter y la piedra filosofal',description='Harry Potter y la piedra filosofal'),
                Book(isbn='123456780',title='Harry Potter y la Camara Secreta',description='Harry Potter y la Camara Secreta')]

print(j_rowling.books[1])

session.add(j_rowling)

session.commit()

our_author=session.query(Author).filter_by(firstname='Joanne').first()

j_rowling=session.query(Author).filter_by(firstname='Joanne').one()

print(j_rowling.books)

print(author is our_author)

for instance in session.query(Author).order_by(Author.id):
    print (instance.firstname,instance.lastname,instance.books)


print ( session.query(Author).order_by(Author.id).count())

print("#Query 1")
#Realizar un Join
print(session.query(Author).join(Book,Author.id==Book.author_id).all())

print(session.query(Book).join(Author,Book.author_id==Author.id).all())

print(session.query(Book).join(Author,Book.author_id==Author.id).filter(exists().where(Author.id==1)).all())

print(session.query(Author).join(Book,Author.id==Book.author_id).filter(Book.isbn=='123456789'))

books=[Book(isbn='123456789',title='Harry Potter y la piedra filosofal',description='Harry Potter y la piedra filosofal'),
                Book(isbn='123456780',title='Harry Potter y la Camara Secreta',description='Harry Potter y la Camara Secreta')]

books[1].categories.append(BookCategory(name='Aventura'))
books[1].categories.append(BookCategory(name='Accion'))

books[0].categories.append(BookCategory(name='Aventura'))

for book in books:
    book.author=j_rowling


print(session.query(Book).filter(Book.categories.any(name='Aventura')).all())

print(session.query(Book).filter(Book.author==j_rowling).filter(Book.categories.any(name='Accion')).all())



#session.delete(j_rowling) ##Borro a J_rowling
print(session.query(Author).outerjoin(Book,Author.id==Book.author_id).count()) #Left Join

