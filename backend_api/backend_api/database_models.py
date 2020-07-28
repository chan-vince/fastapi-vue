import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, Index, func, JSON
from sqlalchemy.orm import relationship

from backend_api.database_connection import Base

association_practice_employee = Table('_association_practice_employee', Base.metadata,
                                      Column('practice_id', Integer, ForeignKey('practices.id', ondelete='CASCADE')),
                                      Column('employee_id', Integer, ForeignKey('employees.id', ondelete='CASCADE')))

association_practice_systems = Table('_association_practice_systems', Base.metadata,
                                     Column('practice_id', Integer, ForeignKey('practices.id', ondelete='CASCADE')),
                                     Column('access_system_id', Integer, ForeignKey('access_systems.id', ondelete='CASCADE')))

association_practice_partners = Table('_association_practice_partners', Base.metadata,
                                      Column('practice_id', Integer, ForeignKey('practices.id', ondelete='CASCADE')),
                                      Column('employee_id', Integer, ForeignKey('employees.id', ondelete='CASCADE')))


class Practice(Base):
    __tablename__ = "practices"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    national_code = Column(String(length=255))
    emis_cdb_practice_code = Column(String(length=255), nullable=False,  unique=True)
    go_live_date = Column(String(length=255))
    closed = Column(Boolean, default=False)

    Index('idx_practice_id', 'id')
    Index('idx_practice_name', 'name')
    Index('idx_practice_emis_cdb_practice_code', 'emis_cdb_practice_code')

    # These relationships allow SQLAlchemy to automatically load data from automatic table joins
    access_systems = relationship("AccessSystem", secondary=association_practice_systems)
    addresses = relationship("Address", back_populates="practice")
    employees = relationship("Employee", secondary=association_practice_employee, back_populates="practices")
    main_partners = relationship("Employee", secondary=association_practice_partners, back_populates="partner_of")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False, unique=False)
    professional_num = Column(String(length=255), nullable=False)
    desktop_num = Column(String(length=255), nullable=True)
    it_portal_num = Column(String(length=255), nullable=True)
    active = Column(Boolean, default=True)
    job_title_id = Column(Integer, ForeignKey("job_titles.id"), nullable=True)

    Index('idx_employee_id', 'id')
    Index('idx_employee_email', 'email', unique=True)

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
    phone_num = Column(String(length=255))
    dts_email = Column(String(length=255), nullable=False)
    practice_id = Column(Integer, ForeignKey("practices.id", ondelete='CASCADE'))

    # Ensure that each address is unique in its combination of fields
    Index('idx_address', 'line_1', 'line_2', 'town', 'county', 'postcode', unique=True)

    practice = relationship("Practice", back_populates="addresses")
    ip_ranges = relationship("IPRange")


class JobTitle(Base):
    __tablename__ = "job_titles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), nullable=False, unique=True)


class AccessSystem(Base):
    __tablename__ = "access_systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False, unique=True)


class IPRange(Base):
    __tablename__ = "ip_ranges"

    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(String(length=255), nullable=False, unique=True)
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete='CASCADE'))


class ChangeHistory(Base):
    __tablename__ = "_change_history"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    last_modified = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    requestor_id = Column(Integer, ForeignKey('employees.id'))
    approver_id = Column(Integer, ForeignKey('employees.id'))
    approval_status = Column(Boolean)  # can be null which means pending

    target_name = Column(String(length=255))
    target_id = Column(Integer)

    current_state = Column(JSON)
    new_state = Column(JSON)

    approver = relationship("Employee", foreign_keys=[approver_id])
    requestor = relationship("Employee", foreign_keys=[requestor_id])

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
