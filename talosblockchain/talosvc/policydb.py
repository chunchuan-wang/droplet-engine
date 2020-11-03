# 2017-2020, ETH Zurich, D-INFK, lubu@inf.ethz.ch

import sqlite3

import virtualchain

from config import *
from policy import create_policy_from_db_tuple, Policy

"""
Implementation of the talos virtualchain state machine.
A SQL Lite database is used for storing the state.
"""

################
# DB Functions #
################

DB_SCRIPT = """
CREATE TABLE policy(
                        stream_id TEXT NOT NULL,
                        owner TEXT NOT NULL,
                        owner_pubkey TEXT,
                        nonce TEXT NOT NULL,
                        txid TEXT NOT NULL,
                        PRIMARY KEY(owner, stream_id));

CREATE TABLE shares( tx_policy INT NOT NULL,
                        pubkey TEXT NOT NULL,
                        txid TEXT NOT NULL,
                        PRIMARY KEY(tx_policy, pubkey));

CREATE TABLE timeintervals( tx_policy INT NOT NULL,
                        starttime INT NOT NULL,
                        timeinterval INT NOT NULL,
                        txid TEXT NOT NULL,
                        PRIMARY KEY(tx_policy, txid));


CREATE INDEX shares_idx on shares(tx_policy);
CREATE INDEX time_idx on timeintervals(tx_policy);
CREATE INDEX policy_txid_idx on policy(txid);
CREATE INDEX owner_idx on policy(owner, stream_id);
"""

SQL_INSERT_POLICY = "INSERT INTO policy VALUES (?,?,?,?,?)"
SQL_INSERT_SHARES = "INSERT INTO shares VALUES (?,?,?)"
SQL_TIMEINTERVALS = "INSERT INTO timeintervals VALUES (?,?,?,?)"

SQL_DELETE_SHARE = "DELETE FROM shares WHERE shares.tx_policy=? AND shares.pubkey=?"
SQL_DELETE_INTERVALS_FOR_POLICY = "DELETE FROM timeintervals WHERE timeintervals.tx_policy=?"
SQL_DELETE_SHARES_FOR_POLICY = "DELETE FROM shares WHERE shares.tx_policy=?"
SQL_DELETE_POLICY = "DELETE FROM policy WHERE policy.txid=?"

SQL_FETCH_POLICY = "SELECT * FROM policy WHERE policy.stream_id=? AND policy.owner=?"
SQL_FETCH_SHARES = "SELECT shares.pubkey, shares.txid FROM shares WHERE shares.tx_policy=?"
SQL_FETCH_TIMES = "SELECT timeintervals.starttime, timeintervals.timeinterval, timeintervals.txid  " \
                  "FROM timeintervals WHERE timeintervals.tx_policy=?"
SQL_FETCH_POLICY_TXID = "SELECT policy.txid FROM policy WHERE policy.stream_id=? AND policy.owner=?"
SQL_FETCH_POLICIES_FOR_OWNER = "SELECT policy.stream_id FROM policy WHERE policy.owner=?"
SQL_FETCH_OWNERS = "SELECT DISTINCT policy.owner FROM policy LIMIT ? OFFSET ?"
SQL_FETCH_POLICY_WITH_TXID = "SELECT * FROM policy WHERE policy.txid=?"

SQL_FETCH_HAS_ACCESS = "SELECT owner, stream_id FROM policy WHERE txid in (SELECT tx_policy FROM shares WHERE pubkey=?);"


def create_db(db_filename):
    if os.path.exists(db_filename):
        raise Exception("Database '%s' already exists" % db_filename)
    con = sqlite3.connect(db_filename, timeout=2 ** 30)
    lines = [l + ";" for l in DB_SCRIPT.split(";")]
    for line in lines:
        con.execute(line)
    return con


def connect_to_db(db_filename):
    return sqlite3.connect(db_filename, timeout=2 ** 30)


def commit_create_policy(conn, stream_id, owner, owner_pubkey, txid, starttime, timeinterval, nonce):
    c = conn.cursor()
    try:
        c.execute(SQL_INSERT_POLICY, (stream_id, owner, owner_pubkey, nonce, txid))
        c.execute(SQL_TIMEINTERVALS, (txid, starttime, timeinterval, txid))
        conn.commit()
    finally:
        c.close()


def commit_addshare(conn, owner, stream_id, pubkey, txid):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_POLICY_TXID, (stream_id, owner))
        idx_policy = c.fetchone()[0]
        c.execute(SQL_INSERT_SHARES, (idx_policy, pubkey, txid))
        conn.commit()
    finally:
        c.close()


def commit_addinterval(conn, owner, stream_id, starttime, timeinterval, txid):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_POLICY_TXID, (stream_id, owner))
        idx_policy = c.fetchone()[0]
        c.execute(SQL_TIMEINTERVALS, (idx_policy, starttime, timeinterval, txid))
        conn.commit()
    finally:
        c.close()


def commit_revokeshare(conn, owner, stream_id, pubkey):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_POLICY_TXID, (stream_id, owner))
        idx_policy = c.fetchone()[0]
        c.execute(SQL_DELETE_SHARE, (idx_policy, pubkey))
        conn.commit()
    finally:
        c.close()


def commit_invalidate_policy(conn, owner, stream_id):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_POLICY_TXID, (stream_id, owner))
        idx_policy = c.fetchone()[0]
        c.execute(SQL_DELETE_POLICY, (idx_policy,))
        c.execute(SQL_DELETE_SHARES_FOR_POLICY, (idx_policy,))
        c.execute(SQL_DELETE_INTERVALS_FOR_POLICY, (idx_policy,))
        conn.commit()
    finally:
        c.close()


def fetch_policy(conn, owner, stream_id):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_POLICY, (stream_id, owner))
        policy_data = c.fetchone()
        if policy_data is None:
            return None
        policy = create_policy_from_db_tuple(policy_data)

        # Add shares to policy
        c.execute(SQL_FETCH_SHARES, (policy.get_txid(),))
        for share in c:
            policy.add_share(share)

        c.execute(SQL_FETCH_TIMES, (policy.get_txid(),))
        for time in c:
            policy.add_time_tuple(time)
        return policy
    finally:
        c.close()


def fetch_poilicies_for_owner(conn, owner):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_POLICIES_FOR_OWNER, (owner,))
        return c.fetchall()
    finally:
        c.close()


def fetch_has_access_for_share_address(conn, address):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_HAS_ACCESS, (address,))
        return c.fetchall()
    finally:
        c.close()


def fetch_owners(conn, limit, offset):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_OWNERS, (limit, offset))
        return c.fetchall()
    finally:
        c.close()


def fetch_policy_with_txid(conn, txid):
    c = conn.cursor()
    try:
        c.execute(SQL_FETCH_POLICY_WITH_TXID, (txid,))
        policy_data = c.fetchone()
        if policy_data is None:
            return None
        policy = create_policy_from_db_tuple(policy_data)

        # Add shares to policy
        c.execute(SQL_FETCH_SHARES, (policy.get_txid(),))
        for share in c:
            policy.add_share(share)

        c.execute(SQL_FETCH_TIMES, (policy.get_txid(),))
        for time in c:
            policy.add_time_tuple(time)
        return policy
    finally:
        c.close()


#################
# State Machine #
#################


class PolicyState:
    """
    Class which implements the handlers and checkers
    for each operation found in the blockchain
    """

    def __init__(self, policy):
        self.policy = policy
        self.ops = []

    def handle_op(self, opcode, op):
        method = getattr(PolicyState, "handle_" + OPCODE_NAMES[opcode])
        method(self, op)

    def check_op(self, opcode, data):
        method = getattr(PolicyState, "check_" + OPCODE_NAMES[opcode])
        return method(self, data)

    @staticmethod
    def handle_CREATE_POLICY(policy_state, op):
        args = (op[OPCODE_FIELD_STREAM_ID], op[OPCODE_FIELD_OWNER], op[OPCODE_FIELD_OWNER_PK],
                op[OPCODE_FIELD_TXTID], op[OPCODE_FIELD_TIMESTAMP_START], op[OPCODE_FIELD_INTERVAL],
                op[OPCODE_FIELD_NONCE])
        policy_state.ops.append((commit_create_policy, args))
        policy_state.policy = Policy(op[OPCODE_FIELD_OWNER], op[OPCODE_FIELD_OWNER_PK], op[OPCODE_FIELD_STREAM_ID],
                                     op[OPCODE_FIELD_NONCE], op[OPCODE_FIELD_TXTID])
        policy_state.policy.add_time_tuple((op[OPCODE_FIELD_TIMESTAMP_START],
                                            op[OPCODE_FIELD_INTERVAL], op[OPCODE_FIELD_TXTID]))

    @staticmethod
    def handle_GRANT_ACCESS(policy_state, op):
        keys = op[OPCODE_FIELD_PUBLIC_KEYS].split(',')
        args = [(op[OPCODE_FIELD_OWNER], op[OPCODE_FIELD_STREAM_ID], key, op[OPCODE_FIELD_TXTID]) for key in keys]
        for arg in args:
            policy_state.ops.append((commit_addshare, arg))
        for key in keys:
            policy_state.policy.add_share((key, op[OPCODE_FIELD_TXTID]))

    @staticmethod
    def handle_REVOKE_ACCESS(policy_state, op):
        keys = op[OPCODE_FIELD_PUBLIC_KEYS].split(',')
        args = [(op[OPCODE_FIELD_OWNER], op[OPCODE_FIELD_STREAM_ID], key) for key in keys]
        for arg in args:
            policy_state.ops.append((commit_revokeshare, arg))
        for key in keys:
            policy_state.policy.remove_share(key)

    @staticmethod
    def handle_CHANGE_INTERVAL(policy_state, op):
        args = (op[OPCODE_FIELD_OWNER], op[OPCODE_FIELD_STREAM_ID],
                op[OPCODE_FIELD_TIMESTAMP_START], op[OPCODE_FIELD_INTERVAL], op[OPCODE_FIELD_TXTID])
        policy_state.ops.append((commit_addinterval, args))
        policy_state.policy.add_time_tuple(
            (op[OPCODE_FIELD_TIMESTAMP_START], op[OPCODE_FIELD_INTERVAL], op[OPCODE_FIELD_TXTID]))

    @staticmethod
    def handle_INVALIDATE_POLICY(policy_state, op):
        args = (op[OPCODE_FIELD_OWNER], op[OPCODE_FIELD_STREAM_ID])
        policy_state.ops.append((commit_invalidate_policy, args))
        policy_state.policy = None

    @staticmethod
    def check_CREATE_POLICY(policy_state, data):
        if policy_state.policy is not None:
            return False
        return True

    @staticmethod
    def check_GRANT_ACCESS(policy_state, data):
        if policy_state.policy is None:
            return False

        keys = data[OPCODE_FIELD_PUBLIC_KEYS].split(',')
        for key in keys:
            if policy_state.policy.has_shared_key(key):
                return False

        return True

    @staticmethod
    def check_REVOKE_ACCESS(policy_state, data):
        if policy_state.policy is None:
            return False
        keys = data[OPCODE_FIELD_PUBLIC_KEYS].split(',')
        for key in keys:
            if not policy_state.policy.has_shared_key(key):
                return False
        return True

    @staticmethod
    def check_CHANGE_INTERVAL(policy_state, data):
        if policy_state.policy is None:
            return False
        return True

    @staticmethod
    def check_INVALIDATE_POLICY(policy_state, data):
        if policy_state.policy is None:
            return False
        return True


class TalosPolicyDB(virtualchain.StateEngine):
    """
    Implements the state machine 
    """

    def __init__(self, db_filename, expected_snapshots={}, read_only=True):
        """
        Inititalizes a db state given a sql lite database.
        If the database not exists, a new database and state is created
        :param db_filename: the file name of the sql lite database
        :param expected_snapshots: the expected snapchosts (consensus hashes)
        :param read_only: indicates if the state is readonly
        """
        # set implementation of virtualchain
        import talosvirtualchain
        blockstack_impl = talosvirtualchain

        lastblock = self.get_lastblock(impl=blockstack_impl)

        self.db = None

        self.blockstate = {}

        self.db_filename = db_filename
        if os.path.exists(db_filename):
            self.db = connect_to_db(db_filename)
        else:
            self.db = create_db(db_filename)

        super(TalosPolicyDB, self).__init__(MAGIC_BYTES,
                                            OPCODES,
                                            OPCODE_FIELDS,
                                            impl=blockstack_impl,
                                            initial_snapshots={},
                                            state=self,
                                            expected_snapshots=expected_snapshots,
                                            read_only=read_only)

    def close(self):
        if self.db is not None:
            self.db.commit()
            self.db.close()
            self.db = None

    def get_db_path(self):
        return self.db_filename

    def _reset_temporary_blockstate(self):
        self.blockstate = {}

    def get_policystate_temporary(self, owner, streamid):
        if owner + str(streamid) in self.blockstate:
            return self.blockstate[owner + str(streamid)]
        else:
            policy_state = PolicyState(fetch_policy(self.db, owner, streamid))
            self.blockstate[owner + str(streamid)] = policy_state
            return policy_state

    def store_temporary_state(self):
        state = self.blockstate
        self._reset_temporary_blockstate()
        for _, value in state.iteritems():
            for op in value.ops:
                try:
                    op[0](self.db, *op[1])
                except RuntimeError:
                    return False

        return True

    def get_policy(self, owner, streamid):
        return fetch_policy(self.db, owner, streamid)

    def get_policies_for_owner(self, owner):
        return fetch_poilicies_for_owner(self.db, owner)

    def get_owners(self, limit, offset):
        return fetch_owners(self.db, limit, offset)

    def get_policy_with_txid(self, txid):
        return fetch_policy_with_txid(self.db, txid)

    def get_has_access(self, share_address):
        return fetch_has_access_for_share_address(self.db, share_address)
