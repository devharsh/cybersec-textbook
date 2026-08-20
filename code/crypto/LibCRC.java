import java.util.zip.CRC32;

// Calculates CRC32 checksum for a string
public class LibCRC {

    public static void main(String[] args) {
        String input = "Hello World!";
        CRC32 crc = new CRC32();
        crc.update(input.getBytes());
        System.out.println("input:"+input);
        System.out.println("CRC32:"+crc.getValue());
    }
}
