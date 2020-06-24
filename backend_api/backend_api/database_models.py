import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship

from .database import Base


association_practice_employee = Table('association_practice_employee', Base.metadata,
                                      Column('gp_practice_id', Integer, ForeignKey('gp_practices.id')),
                                      Column('employee_id', Integer, ForeignKey('employees.id')))

association_practice_systems = Table('association_practice_systems', Base.metadata,
                                     Column('gp_practice_id', Integer, ForeignKey('gp_practices.id')),
                                     Column('system_type_id', Integer, ForeignKey('system_types.id')))

association_practice_partners = Table('association_practice_partners', Base.metadata,
                                      Column('gp_practice_id', Integer, ForeignKey('gp_practices.id')),
                                      Column('employee_id', Integer, ForeignKey('employees.id')))


class GPPractices(Base):
    __tablename__ = "gp_practices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    phone_num = Column(String(length=255))
    emis_cdb_practice_code = Column(String(length=255), nullable=False, unique=True)
    go_live_date = Column(DateTime)
    closed = Column(Boolean, default=False)

    # These relationships allow SQLAlchemy to automatically load data from automatic table joins
    system_types = relationship("SystemTypes", secondary=association_practice_systems)
    address = relationship("GPAddresses", uselist=False, back_populates="gp_practice")
    employees = relationship("Employees", secondary=association_practice_employee, back_populates="practices")
    main_partners = relationship("Employees", secondary=association_practice_partners, back_populates="partner_of")
    ip_ranges = relationship("IPRanges")


class Employees(Base):
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

    job_title = relationship("JobTitles", uselist=False)
    practices = relationship("GPPractices", secondary=association_practice_employee, back_populates="employees")
    partner_of = relationship("GPPractices", secondary=association_practice_partners, back_populates="main_partners")


class GPAddresses(Base):
    __tablename__ = "gp_addresses"

    id = Column(Integer, primary_key=True, index=True)
    line_1 = Column(String(length=255), nullable=False)
    line_2 = Column(String(length=255), nullable=True)
    town = Column(String(length=255), nullable=False)
    county = Column(String(length=255), nullable=False)
    postcode = Column(String(length=255), nullable=False)
    dts_email = Column(String(length=255), nullable=False)
    gp_practice_id = Column(Integer, ForeignKey("gp_practices.id"), unique=True)

    gp_practice = relationship("GPPractices", back_populates="address")


class JobTitles(Base):
    __tablename__ = "job_titles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), nullable=False, unique=True)


class SystemTypes(Base):
    __tablename__ = "system_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False, unique=True)


class IPRanges(Base):
    __tablename__ = "ip_ranges"

    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(String(length=255), nullable=False, unique=True)
    gp_practice = Column(Integer, ForeignKey("gp_practices.id"))


class SystemUsers(Base):
    __tablename__ = "system_users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    email = Column(String(length=255))
    role = Column(Integer, ForeignKey("system_roles.id"))
    password_hash = Column(String(length=1024))
    password_salt = Column(String(length=255))


class SystemRoles(Base):
    __tablename__ = "system_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255))
