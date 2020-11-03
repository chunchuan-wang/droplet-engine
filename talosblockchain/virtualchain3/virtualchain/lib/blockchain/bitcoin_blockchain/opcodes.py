#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Virtualchain
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org
    
    This file is part of Virtualchain
    
    Virtualchain is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Virtualchain is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Virtualchain.  If not, see <http://www.gnu.org/licenses/>.
"""

OPCODE_VALUES = {
   "OP_0": 0, 
   "OP_PUSHDATA1": 76,  # 0x4c
   "OP_PUSHDATA2": 77,  # 0x4d
   "OP_PUSHDATA4": 78,  # 0x4e
   "OP_1NEGATE": 79, 
   "OP_RESERVED": 80, 
   "OP_1": 81, 
   "OP_2": 82, 
   "OP_3": 83, 
   "OP_4": 84, 
   "OP_5": 85, 
   "OP_6": 86, 
   "OP_7": 87, 
   "OP_8": 88, 
   "OP_9": 89, 
   "OP_10": 90, 
   "OP_11": 91, 
   "OP_12": 92, 
   "OP_13": 93, 
   "OP_14": 94, 
   "OP_15": 95, 
   "OP_16": 96, 
   "OP_NOP": 97, 
   "OP_VER": 98, 
   "OP_IF": 99, 
   "OP_NOTIF": 100, 
   "OP_VERIF": 101, 
   "OP_VERNOTIF": 102, 
   "OP_ELSE": 103, 
   "OP_ENDIF": 104, 
   "OP_VERIFY": 105,  # 0x69
   "OP_RETURN": 106,  # 0x6a
   "OP_TOALTSTACK": 107, 
   "OP_FROMALTSTACK": 108, 
   "OP_2DROP": 109, 
   "OP_2DUP": 110, 
   "OP_3DUP": 111, 
   "OP_2OVER": 112, 
   "OP_2ROT": 113, 
   "OP_2SWAP": 114, 
   "OP_IFDUP": 115, 
   "OP_DEPTH": 116, 
   "OP_DROP": 117, 
   "OP_DUP": 118, 
   "OP_NIP": 119, 
   "OP_OVER": 120, 
   "OP_PICK": 121, 
   "OP_ROLL": 122, 
   "OP_ROT": 123, 
   "OP_SWAP": 124, 
   "OP_TUCK": 125, 
   "OP_CAT": 126, 
   "OP_SUBSTR": 127, 
   "OP_LEFT": 128, 
   "OP_RIGHT": 129, 
   "OP_SIZE": 130, 
   "OP_INVERT": 131, 
   "OP_AND": 132, 
   "OP_OR": 133, 
   "OP_XOR": 134, 
   "OP_EQUAL": 135,  # 0x87
   "OP_EQUALVERIFY": 136,  # 0x88
   "OP_RESERVED1": 137, 
   "OP_RESERVED2": 138, 
   "OP_1ADD": 139, 
   "OP_1SUB": 140, 
   "OP_2MUL": 141, 
   "OP_2DIV": 142, 
   "OP_NEGATE": 143, 
   "OP_ABS": 144, 
   "OP_NOT": 145, 
   "OP_0NOTEQUAL": 146, 
   "OP_ADD": 147, 
   "OP_SUB": 148, 
   "OP_MUL": 149, 
   "OP_DIV": 150, 
   "OP_MOD": 151, 
   "OP_LSHIFT": 152, 
   "OP_RSHIFT": 153, 
   "OP_BOOLAND": 154, 
   "OP_BOOLOR": 155, 
   "OP_NUMEQUAL": 156, 
   "OP_NUMEQUALVERIFY": 157, 
   "OP_NUMNOTEQUAL": 158, 
   "OP_LESSTHAN": 159, 
   "OP_GREATERTHAN": 160, 
   "OP_LESSTHANOREQUAL": 161, 
   "OP_GREATERTHANOREQUAL": 162, 
   "OP_MIN": 163, 
   "OP_MAX": 164, 
   "OP_WITHIN": 165, 
   "OP_RIPEMD160": 166, 
   "OP_SHA1": 167, 
   "OP_SHA256": 168, 
   "OP_HASH160": 169,  # 0xa9
   "OP_HASH256": 170, 
   "OP_CODESEPARATOR": 171, 
   "OP_CHECKSIG": 172,  # 0xac
   "OP_CHECKSIGVERIFY": 173,  # 0xad
   "OP_CHECKMULTISIG": 174,  # 0xae
   "OP_CHECKMULTISIGVERIFY": 175,  # 0xaf
   "OP_NOP1": 176, 
   "OP_NOP2": 177, 
   "OP_NOP3": 178, 
   "OP_NOP4": 179, 
   "OP_NOP5": 180, 
   "OP_NOP6": 181, 
   "OP_NOP7": 182, 
   "OP_NOP8": 183, 
   "OP_NOP9": 184, 
   "OP_NOP10": 185, 
   "OP_PUBKEYHASH": 253,  # 0xfd
   "OP_PUBKEY": 254,  # 0xfe
   "OP_INVALIDOPCODE": 255
}

OPCODE_NAMES = dict([(v, k) for (k, v) in list(OPCODE_VALUES.items())])

