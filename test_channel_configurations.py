from time import sleep

import pytest

from conftest import change_access_profile
from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.dll.access_profile import AccessProfile
from d7a.dll.sub_profile import SubProfile
from d7a.phy.channel_header import ChannelHeader, ChannelBand, ChannelCoding, ChannelClass
from d7a.phy.subband import SubBand
from d7a.sp.configuration import Configuration
from d7a.sp.qos import ResponseMode, QoS
from d7a.system_files.access_profile import AccessProfileFile
from d7a.types.ct import CT
from modem.modem import Modem


def validate_communication(test_device, dut, channel_header, channel_index):
  dut.clear_unsolicited_responses_received()  # TODO use pytest mechanism to do this for every test

  change_access_profile(dut, channel_header, channel_index, enable_channel_scan=True)
  change_access_profile(test_device, channel_header, channel_index, enable_channel_scan=False)

  sleep(0.2) # give some time to switch AP

  interface_configuration = Configuration(
    qos=QoS(resp_mod=ResponseMode.RESP_MODE_NO),
    addressee=Addressee(
      access_class=0x01,
      id_type=IdType.NOID,
    )
  )

  command = Command.create_with_return_file_data_action(
    file_id=0x40,
    data=range(10),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=interface_configuration
  )

  resp = test_device.execute_command(command, timeout_seconds=10)
  assert resp, "No response from test device"

  while len(dut.get_unsolicited_responses_received()) == 0:  # endless loop, ended by pytest-timeout if needed
    pass

  assert len(
    dut.get_unsolicited_responses_received()) == 1, "DUT should have received 1 unsolicited response from test device"

  assert dut.get_unsolicited_responses_received()[0].get_d7asp_interface_status().channel_header == channel_header, \
    "Received using unexpected channel header"

  assert dut.get_unsolicited_responses_received()[0].get_d7asp_interface_status().channel_index == channel_index, \
    "Received using unexpected channel index"

def test_868_N_000(test_device, dut):
  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868,
                                 channel_coding=ChannelCoding.PN9,
                                 channel_class=ChannelClass.NORMAL_RATE)
  validate_communication(test_device, dut, channel_header, 0)

def test_868_N_270(test_device, dut):
  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868,
                                 channel_coding=ChannelCoding.PN9,
                                 channel_class=ChannelClass.NORMAL_RATE)
  validate_communication(test_device, dut, channel_header, 270)

def test_868_H_000(test_device, dut):
  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868,
                                 channel_coding=ChannelCoding.PN9,
                                 channel_class=ChannelClass.HI_RATE)
  validate_communication(test_device, dut, channel_header, 0)

def test_868_H_270(test_device, dut):
  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868,
                                 channel_coding=ChannelCoding.PN9,
                                 channel_class=ChannelClass.HI_RATE)
  validate_communication(test_device, dut, channel_header, 270)

def test_868_L_000(test_device, dut):
  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868,
                                 channel_coding=ChannelCoding.PN9,
                                 channel_class=ChannelClass.LO_RATE)
  validate_communication(test_device, dut, channel_header, 0)

def test_868_L_279(test_device, dut):
  channel_header = ChannelHeader(channel_band=ChannelBand.BAND_868,
                                 channel_coding=ChannelCoding.PN9,
                                 channel_class=ChannelClass.LO_RATE)
  validate_communication(test_device, dut, channel_header, 279)