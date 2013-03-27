from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from TestLabWeb.database import Base
from datetime import datetime

class Cluster(Base):
    __tablename__ = 'vsphere_clusters'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    vmhosts = relationship("VmHost", backref="cluster")
    cpu_total = Column(Integer)
    cpu_used = Column(Integer)
    memory_total = Column(Integer)
    memory_used = Column(Integer)
    vmcount = Column(Integer)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Cluster %r>' % (self.name)


vmhost_datastore = Table('vmhosts_datastores', Base.metadata,
    Column('vmhost_id', Integer, ForeignKey('vsphere_vmhosts.id')),
    Column('datastore_id', Integer, ForeignKey('vsphere_datastores.id'))
)

class Datastore(Base):
    __tablename__ = 'vsphere_datastores'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    freespace_mb = Column(Integer)
    capacity_mb = Column(Integer)
    vmhosts = relationship("VmHost", secondary=vmhost_datastore, backref="datastores")

    def __init__(self, name, freespace_mb, capacity_mb):
        self.name = name
        self.freespace_mb = freespace_mb
        self.capacity_mb = capacity_mb

    def __repr__(self):
        return '<Datastore %r>' % (self.name)

class VmHost(Base):
    __tablename__ = 'vsphere_vmhosts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    state = Column(String(50))
    power_state = Column(String(50))
    vsphere_id = Column(String(50))
    cpu_used = Column(Integer)
    cpu_total = Column(Integer)
    mem_used = Column(Integer)
    mem_total = Column(Integer)
    cluster_id = Column(Integer, ForeignKey('vsphere_clusters.id'))
    clusters = relationship("Cluster")
    vms = relationship("Vm")

    def __init__(self, name, state, power_state, vsphere_id, cpu_used, 
                 cpu_total, mem_used, mem_total):
        self.name = name
        self.state = state
        self.power_state = power_state
        self.vsphere_id = vsphere_id
        self.cpu_used = cpu_used
        self.cpu_total = cpu_total
        self.mem_used = mem_used
        self.mem_total = mem_total

class Vm(Base):
    __tablename__ = 'vsphere_vms'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    power_state = Column(String(50))
    mem_total = Column(Integer)
    vcpu_count = Column(Integer)
    vmhost_id = Column(Integer, ForeignKey('vsphere_vmhosts.id'))
    buildstatus = Column(String(50))
    guest_os = Column(String(50))
    vmhost = relationship("VmHost")
    pool_id = Column(Integer, ForeignKey('pools.id'))
    pool = relationship("Pool")

    def __init__(self, name, power_state, mem_total, vcpu_count):
        self.name = name
        self.power_state = power_state
        self.mem_total = mem_total
        self.vcpu_count = vcpu_count

    @property
    def serialize(self):
        return {
            'name'       : self.name,
            'power_state': self.power_state
        }

class Pool(Base):
    __tablename__ = 'pools'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    state = Column(String(50))
    business_function = Column(String(50))
    lease_end_date = Column(DateTime)
    requestor_id = Column(Integer, ForeignKey("users.id"))
    requestor = relationship('User', foreign_keys='Pool.requestor_id')
    viper_ticket = Column(String(20))
    environment = Column(String(50))
    purpose = Column(String(50))
    creation_date = Column(DateTime, default=datetime.now())
    modified_date = Column(DateTime)
    lane_id = Column(Integer, ForeignKey('lanes.id'))
    description = Column(String(200))
    notes = relationship("PoolNote")
    machines = relationship("Vm")
    users = relationship("UserPool", backref="pools")
    created_by_id = Column(Integer, ForeignKey('users.id'))
    modified_by_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<Pool name=%s>" % self.name

class Lane(Base):
    __tablename__ = 'lanes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    short_name = Column(String(10))
    business_unit = Column(String(20))
    pools = relationship("Pool", backref="lane")
    users = relationship("UserLane", backref="lanes")
    is_active = Column(Boolean, nullable = False)
    created_by_id = Column(Integer, ForeignKey('users.id'))
    modified_by_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, name, short_name, business_unit):
        self.name = name
        self.short_name = short_name
        self.business_unit = business_unit
        self.is_active=1
        
    def __repr__(self):
        return "[%s] %s" % (self.business_unit, self.name)

class PoolNote(Base):
    __tablename__ = 'poolnotes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pool_id = Column(Integer, ForeignKey('pools.id'))
    pool = relationship("Pool")
    creation_date = Column(DateTime, default=datetime.now())
    note_text = Column(String(100))

    @property
    def serialize(self):
        return {
            'creation_date'       : self.creation_date.strftime("%d %b %Y %H:%M"),
            'user': self.user.name
        }

class UserLane(Base):
    __tablename__ = 'users_lanes'
    lane_id = Column(Integer, ForeignKey('lanes.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role = Column(String(50))
    lane = relationship("Lane")

    def __init__(self, lane, user, role):
        self.lane = lane
        self.user = user
        self.role = role

    def __repr__(self):
        return "<UserLane Lane=%s User=%s Role=%s>" % (self.lane_id, self.user_id, self.role)

class UserPool(Base):
    __tablename__ = 'users_pools'
    pool_id = Column(Integer, ForeignKey('pools.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role = Column(String(50))
    pool = relationship("Pool")

    def __init__(self, pool, user, role):
        self.pool = pool
        self.user = user
        self.role = role

    def __repr__(self):
        return "<UserPool Pool=%s User=%s Role=%s>" % (self.pool_id, self.user_id, self.role)

class LogEntry(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    action = Column(String(50))
    username = Column(String(50))
    result = Column(String(50))
    timestamp = Column(DateTime, default=datetime.now)

    def __init__(self, action, username, result):
        self.action = action
        self.username = username
        self.result = result

    def __repr__(self):
        return "<LogEntry action=%s user=%s results=%s" % (self.action, self.username, self.result)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    visa_user = Column(String(50))
    qa_user = Column(String(50))
    name = Column(String(50))
    lanes = relationship("UserLane", backref="user")
    pools = relationship("UserPool", backref="user")
    notes = relationship("PoolNote", backref="user")

    def __repr__(self):
        return "%s (%s)" % (self.name, self.qa_user)

class VisaUser(Base):
    __tablename__ = 'visa_domain_users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50))

class QaUser(Base):
    __tablename__ = 'qa_domain_users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(50))

# class VmQueue(Base):
#     __tablename__ = 'vm_provision_queue'
#     folder = Column(String(50))
#     vm_name = Column(String(50))
#     template = Column(String(50))
#     customization = Column(String(50))
#     ip = Column(String(50))
#     cluster = Column(String(50))
#     datastore = Column(String(50))
#     status = Column(String(50))
