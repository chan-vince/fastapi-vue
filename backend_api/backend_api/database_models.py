import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship

from .database import Base


association_practice_employee = Table('_association_practice_employee', Base.metadata,
                                      Column('practice_id', Integer, ForeignKey('practices.id')),
                                      Column('employee_id', Integer, ForeignKey('employees.id')))

association_practice_systems = Table('_association_practice_systems', Base.metadata,
                                     Column('practice_id', Integer, ForeignKey('practices.id')),
                                     Column('system_type_id', Integer, ForeignKey('system_types.id')))

association_practice_partners = Table('_association_practice_partners', Base.metadata,
                                      Column('practice_id', Integer, ForeignKey('practices.id')),
                                      Column('employee_id', Integer, ForeignKey('employees.id')))


class Practice(Base):
    __tablename__ = "practices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    phone_num = Column(String(length=255))
    emis_cdb_practice_code = Column(String(length=255), nullable=False, unique=True)
    go_live_date = Column(DateTime)
    closed = Column(Boolean, default=False)

    # These relationships allow SQLAlchemy to automatically load data from automatic table joins
    system_types = relationship("SystemType", secondary=association_practice_systems)
    address = relationship("Address", uselist=False, back_populates="practice")
    employees = relationship("Employee", secondary=association_practice_employee, back_populates="practices")
    main_partners = relationship("Employee", secondary=association_practice_partners, back_populates="partner_of")
    ip_ranges = relationship("IPRange")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False, unique=True)
    professional_num = Column(String(length=255), nullable=False)
    desktop_num = Column(String(length=255), nullable=True)
    it_portal_num = Column(String(length=255), nullable=True)
    active = Column(Boolean, default=True)
    job_title_id = Column(Integer, ForeignKey("job_titles.id"), nullable=True)

    job_title = relationship("JobTitle", uselist=False)
    practices = relationship("Practice", secondary=association_practice_employee, back_populates="employees")
    partner_of = relationship("Practice", secondary=association_practice_partners, back_populates="main_partners")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    line_1 = Column(String(length=255), nullable=False)
    line_2 = Column(String(length=255), nullable=True)
    town = Column(String(length=255), nullable=False)
    county = Column(String(length=255), nullable=False)
    postcode = Column(String(length=255), nullable=False)
    dts_email = Column(String(length=255), nullable=False)
    practice_id = Column(Integer, ForeignKey("practices.id"), unique=True)

    practice = relationship("Practice", back_populates="address")


class JobTitle(Base):
    __tablename__ = "job_titles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), nullable=False, unique=True)


class SystemType(Base):
    __tablename__ = "system_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False, unique=True)


class IPRange(Base):
    __tablename__ = "ip_ranges"

    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(String(length=255), nullable=False, unique=True)
    practice = Column(Integer, ForeignKey("practices.id"))


# class SystemUser(Base):
#     __tablename__ = "system_users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String(length=255))
#     last_name = Column(String(length=255))
#     email = Column(String(length=255))
#     role = Column(Integer, ForeignKey("system_roles.id"))
#     password_hash = Column(String(length=1024))
#     password_salt = Column(String(length=255))
#
#
# class SystemRole(Base):
#     __tablename__ = "system_roles"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(length=255))
