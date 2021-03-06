package ch.ethz.blokcaditapi.storage.chunkentries;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by lukas on 09.05.17.
 */

public class EntryFactory {

    public static final int TYPE_DOUBLE_ENTRY = 0;
    public static final int TYPE_INT_ENTRY = 4;
    public static final int TYPE_MULTI_DOUBLE_ENTRY = 2;
    public static final int TYPE_PICTURE_ENTRY = 1;

    public static Map<Integer, EntryDecoder> decodersMap = new HashMap<>();

    static {
        decodersMap.put(TYPE_DOUBLE_ENTRY, new DoubleEntry.DoubleEntryDecoder());
        decodersMap.put(TYPE_MULTI_DOUBLE_ENTRY, new MultiDoubleEntry.MultiDoubleEntryDecoder());
        decodersMap.put(TYPE_INT_ENTRY, new IntegerEntry.IntegerEntryDecoder());
        decodersMap.put(TYPE_PICTURE_ENTRY, new PictureEntry.PictureEntryDecoder());
    }

    public static EntryDecoder getDecoderForType(int type) {
        return decodersMap.get(type);
    }


}
