from mockito import *
import unittest
import json

from octest.server import *
from octest.exception import *
from octest.command import * 
from octest.commands.system import *
from octest.response import *

class ServerTest(unittest.TestCase):

  def mockResponse(self, uid, command, parameters = {}, timeout = None): 
    response = mock()
    response.status_code = 200
    json = { 'uid': uid, 'command': command, 'parameters': parameters }
    if timeout is not None:
      json['timeout'] = timeout
    when(response).json().thenReturn(json)
    return response

  def setResponse(self, response): 
  	when(self.server._requests).get('http://www.test.com/clientUID').thenReturn(response)    

  def setUp(self):
    self.server = Server(baseUrl='http://www.test.com', clientId='clientUID')
    self.server._requests = mock()

  def testGetCommmandCopy(self):
    uid = 'CommandUID'
    command = 'copy'
    parameters = {'src': 'source', 'dst': 'destination' }
    timeout = 10
    self.setResponse(self.mockResponse(uid, command, parameters, timeout))

    response = self.server.get()
    
    self.assertIsInstance(response, Copy)
    self.assertEqual(response.uid, uid)
    self.assertEqual(response.parameters, parameters)
    self.assertIs(response.timeout, timeout)

  def testGetCommandNotFound(self):
    uid = 'CommandUID'
    command = 'Not found command'

    self.setResponse(self.mockResponse(uid, command))
    self.assertRaises(CommandNotFoundException, self.server.get)

  def testSendResponseAsJson(self):
    response = Response()
    response.uid = 'commandUID'
    response.status = Response.Status.ok
    response.message = ''
    self.server.send(response)
    verify(self.server._requests).post('http://www.test.com/clientUID/commandUID', response.json())