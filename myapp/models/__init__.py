from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from myapp.database import Base



## Many 2 Many

vmhost_datastore = Table('vmhosts_datastores', Base.metadata,
    Column('vmhost_id', Integer, ForeignKey('vsphere_vmhosts.id')),
    Column('datastore_id', Integer, ForeignKey('vsphere_datastores.id'))
)

class Datastore(Base):
    __tablename__ = 'vsphere_datastores'
    id = Column(Integer, primary_key=True)
    vmhosts = relationship("VmHost", secondary=vmhost_datastore, backref="datastores")

class VmHost(Base):
    __tablename__ = 'vsphere_vmhosts'
    id = Column(Integer, primary_key=True)
    

class Vm(Base):
    __tablename__ = 'vsphere_vms'
    id = Column(Integer, primary_key=True)
    pool_id = Column(Integer, ForeignKey('pools.id'))
    pool = relationship("Pool")

    @property
    def serialize(self):
        return {
            'name'       : self.name,
            'power_state': self.power_state
        }

# Many to Many with extra data

class Pool(Base):
    __tablename__ = 'pools'
    id = Column(Integer, primary_key=True)
    users = relationship("UserPool", backref="pools")

class UserPool(Base):
    __tablename__ = 'users_pools'
    pool_id = Column(Integer, ForeignKey('pools.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role = Column(String(50))
    pool = relationship("Pool")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    pools = relationship("UserPool", backref="user")

