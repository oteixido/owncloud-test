from exception import CommandNotFoundException
from commands import system

class CommandFactory:
  ID_COPY = 'copy'
  ID_WAIT = 'wait'
  ID_WAIT_FILE = 'wait-file'

  def __init__(self):
    self.commands = { 
      self.ID_COPY: system.Copy(),
      self.ID_WAIT: system.Wait(),
      self.ID_WAIT_FILE: system.WaitUntilFileSize(),
    }
  
  def create(self, id, parameters = {}):
    if id not in self.commands:
      raise CommandNotFoundException(id)
    command = self.commands[id]
    command.set(parameters);
    return command