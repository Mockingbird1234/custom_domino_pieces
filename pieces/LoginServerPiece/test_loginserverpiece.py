#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/10/31 11:27
# @File    : test_loginserverpiece.py
# @Software: PyCharm
from domino.testing import piece_dry_run

server_ip =""
port =""
username=""
password=""
auth_method="password"
private_key_path=""
connection_timeout = 30

def test_loginserverpiece():
    input_data = dict(
        server_ip="",
        port="",
        username="",
        password="",
        auth_method="",
        private_key_path="",
        connection_timeout="",
        base64_bytes_data="",
    )
    piece_output = piece_dry_run(
        piece_name="LoginServerPiece",
        input_data=input_data
    )
    assert piece_output is not None
    assert piece_output.get('base64_bytes_data')