import logging
import socket
from typing import Union

from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .. import JchessMessage

_logger = logging.getLogger("j_chess_lib")


class ConnectionDecodeError(Exception):

    def __init__(self, message: str, raw_message: str):
        message = f"Client failed to decode received message{': ' if len(message) > 0 else ''}{message}"
        super().__init__(message)
        self._raw_message = raw_message

    @property
    def raw_message(self):
        return self._raw_message


class Connection:
    _PREFIX_BYTES = 4
    _ENDIAN_TYPE = "big"

    def __init__(self, address: str = "localhost", port: int = 5123):
        self._address = address
        self._port = port
        self._conn = socket.create_connection(address=(address, port))
        self._xml_parse = XmlParser()
        self._xml_serialize = XmlSerializer(config=SerializerConfig(pretty_print=False))
        self._send_count = 0
        self._recv_count = 0

    def __enter__(self):
        return self

    def disconnect(self):
        _logger.info("Disconnecting from connection")
        self._conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def send(self, message: Union[JchessMessage, str]):
        if isinstance(message, str):
            length = len(message)
            # print(f"Sending message with length of {length}")
            length = length.to_bytes(self._PREFIX_BYTES, self._ENDIAN_TYPE)
            self._conn.send(length + message.encode('utf-8'))
            self._send_count += 1
            return
        if isinstance(message, JchessMessage):
            # print(f"Send message of type {message.message_type}")
            return self.send(message=self._xml_serialize.render(message))
        raise Exception(f"Can't send data of type {type(message)}")

    def recv(self) -> JchessMessage:
        len_msg = self._conn.recv(self._PREFIX_BYTES)
        message_byte_len = int.from_bytes(len_msg, self._ENDIAN_TYPE)
        self._recv_count += 1
        rcv_msg = bytes()
        while message_byte_len > 0:
            new_rcv_msg = self._conn.recv(message_byte_len)
            message_byte_len -= len(new_rcv_msg)
            rcv_msg += new_rcv_msg
        raw_message = rcv_msg.decode("utf-8")
        try:
            message = self._xml_parse.from_string(source=raw_message, clazz=JchessMessage)
        except ParserError as e:
            raise ConnectionDecodeError(message="", raw_message=raw_message) from e
        return message

    @property
    def send_count(self):
        return self._send_count

    @property
    def recv_count(self):
        return self._recv_count

    def __str__(self):
        return f"Connection to {self._address}:{self._port}"
