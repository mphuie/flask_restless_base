
from myapp import db

## Many 2 Many

vmhost_datastore = db.Table('vmhosts_datastores',
    db.Column('vmhost_id', db.Integer, db.ForeignKey('vsphere_vmhosts.id')),
    db.Column('datastore_id', db.Integer, db.ForeignKey('vsphere_datastores.id'))
)

class Datastore(db.Model):
    __tablename__ = 'vsphere_datastores'
    id = db.Column(db.Integer, primary_key=True)
    vmhosts = db.relationship("VmHost", secondary=vmhost_datastore, backref="datastores")

class VmHost(db.Model):
    __tablename__ = 'vsphere_vmhosts'
    id = db.Column(db.Integer, primary_key=True)
    

class Vm(db.Model):
    __tablename__ = 'vsphere_vms'
    id = db.Column(db.Integer, primary_key=True)
    pool_id = db.Column(db.Integer, db.ForeignKey('pools.id'))
    pool = db.relationship("Pool")

    @property
    def serialize(self):
        return {
            'name'       : self.name,
            'power_state': self.power_state
        }

# Many to Many with extra data

class Pool(db.Model):
    __tablename__ = 'pools'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("UserPool", backref="pools")

class UserPool(db.Model):
    __tablename__ = 'users_pools'
    pool_id = db.Column(db.Integer, db.ForeignKey('pools.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role = db.Column(db.String(50))
    pool = db.relationship("Pool")


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    pools = db.relationship("UserPool", backref="user")

