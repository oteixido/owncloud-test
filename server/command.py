import json
import uuid
from collections import OrderedDict

class Command:
  uid = None
  name = None
  parameters = None
  startTime = None
  endTime = None
  client = None
    
  def values(self):
    return OrderedDict({
      'uid': self.uid,
      'name': self.name,
      'parameters': self.parameters,
      'startTime': self.startTime,
      'endTime': self.endTime,
      'client': self.client.uid if self.client is not None else None
    })
  
  def json(self):
    return json.dumps(self.values())

  @staticmethod
  def createWait(seconds):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'wait'
    c.parameters = { 'seconds': seconds }
    return c

  @staticmethod
  def createWaitFile(path):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'wait-file'
    c.parameters = { 'path': path }
    return c

  @staticmethod
  def createCopyFile(src, dst):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'copy-file'
    c.parameters = { 'src': src, 'dst': dst }
    return c

class CommandDAO:
  _database = None

  def __init__(self, database):
    self._database = database
  
  def create():
    self._database.execute('create table commands (uid text, name text, parameters text, start_time integer, end_time integer, cliend_id text)')

  def save(self, command):
    found = self._database.find('commands', 'uid', { 'uid': command.uid })
    values = command.values()
    values['parameters'] = json.dumps(command.parameters)
    if found is None:
      self._database.insert('commands', values)
    else :
      self._database.update('commands', 'uid', values)
