import java.io.UnsupportedEncodingException;
import java.security.*;
import java.math.BigInteger;  
import java.nio.charset.StandardCharsets;

public class Hash {
    
    public static void main(String[] args)  {
        try {
            System.out.println(MD5("22"));
            //System.out.println("\n" + toHexString(getSHA("22")));
        } catch (NoSuchAlgorithmException e) {
            // For specifying wrong message digest algorithms
            System.out.println("Exception thrown for incorrect algorithm: " + e);
        }
    }
    
    public static String MD5(String md5) throws NoSuchAlgorithmException {
        java.security.MessageDigest md = java.security.MessageDigest.getInstance("MD5");
        byte[] array = md.digest(md5.getBytes());
        StringBuffer sb = new StringBuffer();

        for (int i = 0; i < array.length; ++i) {
            sb.append(Integer.toHexString((array[i] & 0xFF) | 0x100).substring(1,3));
        }

        return sb.toString();
    }
    
    public static byte[] getSHA(String input) throws NoSuchAlgorithmException {
        // Static getInstance method is called with hashing SHA
        java.security.MessageDigest md = java.security.MessageDigest.getInstance("SHA-256");

        // digest() method called
        // to calculate message digest of an input
        // and return array of byte
        return md.digest(input.getBytes(StandardCharsets.UTF_8));
    }
    
    public static String toHexString(byte[] hash) {
        // Convert byte array into signum representation
        BigInteger number = new BigInteger(1, hash);

        // Convert message digest into hex value
        StringBuilder hexString = new StringBuilder(number.toString(16));

        // Pad with leading zeros
        while (hexString.length() < 32) {
            hexString.insert(0, '0');
        }

        return hexString.toString();
    }
    
}
