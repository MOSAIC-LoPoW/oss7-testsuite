from time import sleep

import struct
from pytest_bdd import scenario, given, when, then

from conftest import change_access_profile, create_access_profile, set_active_access_class
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.file import DataRequest
from d7a.alp.operands.length import Length
from d7a.alp.operands.offset import Offset
from d7a.alp.operands.query import QueryOperand, QueryType, ArithQueryParams, ArithComparisonType
from d7a.alp.operations.break_query import BreakQuery
from d7a.alp.operations.requests import ReadFileData
from d7a.alp.regular_action import RegularAction
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.types.ct import CT


@scenario('queries.feature',
          'When predicate of Break Query action fails all subsequent actions are dropped')
def test_break_query_fails():
  pass


@given("a command containing a Break Query action, which results in a fail, and a Read action")
def query_cmd_fail(context):
  cmd = Command()

  # we assume comparing the UID file to 0 results in a fail
  cmd.add_action(
    RegularAction(
      operation=BreakQuery(
        operand=QueryOperand(
          type=QueryType.ARITH_COMP_WITH_VALUE,
          mask_present=False,
          params=ArithQueryParams(comp_type=ArithComparisonType.EQUALITY, signed_data_type=True),
          compare_length=Length(8),
          compare_value=[0, 0, 0, 0, 0, 0, 0, 0],
          file_a_offset=Offset(id=0, offset=Length(0))
        )
      )
    )
  )
  cmd.add_action(
    RegularAction(
      operation=ReadFileData(
        operand=DataRequest(
          offset=Offset(id=0, offset=Length(0)),
          length=Length(8)
        )
      )
    )
  )

  context.query_cmd = cmd


@when("the testdevice executes the command")
def send_command(test_device, context):
  context.response = test_device.execute_command(context.query_cmd, timeout_seconds=10)


@then("the command executes successfully")
def executes_successfully(context):
  assert len(context.response) == 1, "expected one response"
  assert context.response[0].execution_completed, "execution should be completed"
  assert not context.response[0].completed_with_error, "the command should execute without error"

@then("the Read action does not return a result")
def does_not_return_result(context):
  assert len(context.response) == 1, "expected one response"
  assert len(context.response[0].actions) == 0, "expected no return file action"


@scenario('queries.feature',
          'When predicate of Break Query action succeeds all subsequent actions are executed')
def test_break_query_succeeds():
  pass

@given("a command containing a Break Query action, which results in a success, and a Read action")
def query_cmd_success(test_device, context):
  cmd = Command()

  # comparing the UID file to the UID results in a success
  cmd.add_action(
    RegularAction(
      operation=BreakQuery(
        operand=QueryOperand(
          type=QueryType.ARITH_COMP_WITH_VALUE,
          mask_present=False,
          params=ArithQueryParams(comp_type=ArithComparisonType.EQUALITY, signed_data_type=True),
          compare_length=Length(8),
          compare_value=[ord(b) for b in struct.pack(">Q", int(test_device.uid, 16))],
          file_a_offset=Offset(id=0, offset=Length(0))
        )
      )
    )
  )
  cmd.add_action(
    RegularAction(
      operation=ReadFileData(
        operand=DataRequest(
          offset=Offset(id=0, offset=Length(0)),
          length=Length(8)
        )
      )
    )
  )

  context.query_cmd = cmd

@then("the Read action does return a result")
def does_return_result(context):
  assert len(context.response) == 1, "expected one response"
  assert len(context.response[0].actions) == 1, "expected a return file action"