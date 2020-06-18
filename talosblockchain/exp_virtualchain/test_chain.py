#© 2017-2020, ETH Zurich, D-INFK, lubu@inf.ethz.ch

from util import *


# example plugin to a virtual chain that defines its behavior.

def get_virtual_chain_name():
    """
    Get the name of the virtual chain we're building.
    """
    return "virtualchain-test"


def get_virtual_chain_version():
    """
    Get the version string for this virtual chain.
    """
    print "reference implementation of get_virtual_chain_version"
    return "v0.01-beta"


def get_first_block_id():
    """
    Get the id of the first block to start indexing.
    """
    print "reference implementation of get_first_block_id"
    return 825


def get_db_state():
    """
    Return an opaque 'state' object that will be preserved across calls
    to the blockchain indexing callbacks.
    """
    return {}


def get_opcodes():
    """
    Return the set of opcodes we're looking for.
    """
    return OPCODES


def get_magic_bytes():
    """
    Return the magic byte sequence we're scanning OP_RETURNs for.
    """
    return MAGIC_BYTES


def get_op_processing_order():
    """
    Return a sequence of opcodes as a hint to the order in which
    the indexer should process opcodes.
    """
    return OPCODES


def db_parse(block_id, txid, txind, opcode, op_payload, senders, inputs, outputs, fee, db_state=None):
    """
    Given the block ID, and information from what looks like
    an OP_RETURN transaction that is part of the virtual chain, parse the
    transaction's OP_RETURN nulldata into a dict.

    Return the dict if this is a valid op.
    Return None if not.

    NOTE: the virtual chain indexer reserves all keys that start with 'virtualchain_'
    """
    print op_payload
    data = {}
    if opcode == ADD or opcode == CHANGE:
        data['uid'] = op_payload[0:2]
        data['data'] = op_payload[2:]
    else:
        data['uid'] = op_payload[0:2]
    return data


def db_scan_block(block_id, op_list, db_state=None):
    """
    Given the block ID and a tx-ordered list of operations, do any
    block-level initial preprocessing.  This method does not
    affect the operations (the op_list will be discarded), nor
    does it return anything.  It is only meant to give the state
    engine implementation information on what is to come in the
    sequence of db_check() calls.
    """
    print "reference implementation of db_check_block"
    return


def db_check(block_id, new_ops, opcode, op, txid, vtxindex, checked, db_state=None):
    """
    Given the block ID and a parsed operation, check to see if this is a *valid* operation
    for the purposes of this virtual chain's database.

    Return True if so; False if not.
    """
    print "reference implementation of db_check"
    return True


def db_commit(block_id, opcode, op, txid, vtxindex, db_state=None):
    """
    Given a block ID and checked opcode, record it as
    part of the database.  This does *not* need to write
    the data to persistent storage, since save() will be
    called once per block processed.
    This method must return either the updated op with the
    data to pass on to db_serialize, or False if the op
    is to be rejected.
    """
    print "reference implementation of db_commit"
    print op
    return op


def db_save(block_id, consensus_hash, y, filename, db_state=None):
    """
    Save all persistent state to stable storage.

    Return True on success
    Return False on failure.
    """
    print "reference implementation of db_save"
    return True


def db_continue(block_id, consensus_hash):
    """
    Signal to the implementation that all state for this block
    has been saved, and that this is now the new consensus hash.
    Return value indicates whether or not we should continue indexing.
    """
    print "reference implementation of db_continue"
    return True
