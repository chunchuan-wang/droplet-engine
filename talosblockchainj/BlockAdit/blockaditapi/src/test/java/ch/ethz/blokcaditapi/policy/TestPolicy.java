package ch.ethz.blokcaditapi.policy;

import org.junit.Test;

import java.util.List;

import ch.ethz.blokcaditapi.storage.Util;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
/**
 * Created by lukas on 09.05.17.
 */

public class TestPolicy {

    private static String testPolicyJSON = "{\"owner\": \"mhJ7QEzyZhPA9D2f9Vaab1saKgBAUMQ9qx\", \"s" +
            "treamid\": \"1\", \"owner_pk\": \"02735e3741093c3a1f1c04c99bb6af80fe83601094aa917648bb5546dc90542d54\"," +
            " \"nonce\": \"OU2HliHRUUZJokNvn84a+A==\", \"txid\": \"8cf71b7ed09acf896b40fc087e56d3d4dbd8cc346a869bb8" +
            "a81624153c0c2b8c\", \"shares\": [{\"pk_addr\": \"mtuVSpDMrtZi5GfZgEJbdR5dSD3ULsQ81y\", \"txid\": \"297" +
            "0564756cddc6487227304fbbda906f567c870ea619fda52943b88998c697f\"}], \"times\": [{\"ts_start\": 1491309499" +
            ", \"ts_interval\": 86400, \"txid\": \"8cf71b7ed09acf896b40fc087e56d3d4dbd8cc346a869bb8a81624153c0c2b8c\"}, " +
            "{\"ts_start\": 1491309508, \"ts_interval\": 43200, \"txid\": \"8db362cc6301183d2bbb026498d42cb113a85a20233" +
            "32205bb8024f6e5e1f5eb\"}]}";

    private static String POL_CREATE_CMD = "74612b01010000006400000000000000c80000000000000000000000000000000000000000000000";

    @Test
    public void checkJSON() throws Exception {
        Policy pol = new Policy("a", 1, "asdads", "sdads", "asdadasd");
        pol.addShare(new Policy.PolicyShare("aa", "sdasd"));
        pol.addTimeIndex(new Policy.IndexEntry(1,2,"asdasd"));
        String jsonPol = pol.toJson();
        System.out.println(jsonPol);
        Policy after = Policy.createFromJsonString(jsonPol);
        assertEquals(pol.getOwner(), after.getOwner());
        assertEquals(pol.getShares().size(), after.getShares().size());
        assertEquals(pol.getTimes().size(), after.getTimes().size());
    }

    @Test
    public void checkJSON2() throws Exception {
        Policy after = Policy.createFromJsonString(testPolicyJSON);
        assertEquals("mhJ7QEzyZhPA9D2f9Vaab1saKgBAUMQ9qx", after.getOwner());
        assertEquals(1, after.getShares().size());
        assertEquals(2, after.getTimes().size());
    }

    @Test
    public void testClient() throws Exception {
        PolicyVcApiClient client = new PolicyVcApiClient("46.101.113.112", 5000);
        List<String> owners = client.getPolicyOwners(10, 0);
        assertTrue(owners.size()>0);

        for (String owner : owners) {
            List<Integer> streams = client.getStreamIdsForOwner(owner);
            assertTrue(streams.size()>0);
            for (Integer id : streams) {
                Policy a = client.getPolicy(owner, id);
                assertEquals(a.getOwner(), owner);
            }
        }
    }


    @Test
    public void testOPCreate() throws Exception {
        byte[] result = PolicyOPReturn.createPolicyCMD(1, 100, 200, new byte[16]);
        byte[] expected = Util.hexStringToByteArray(POL_CREATE_CMD);
        System.out.println(POL_CREATE_CMD);
        System.out.println(Util.bytesToHexString(result));
        assertArrayEquals(expected, result);
    }


}
