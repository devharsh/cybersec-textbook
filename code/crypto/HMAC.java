import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class HMAC {

    public static void main(String[] args) {
        try {
            String secret = "Secret";
            String message = "Message";
            
            Mac sha256_HMAC = Mac.getInstance("HmacSHA256");
            SecretKeySpec secret_key = new SecretKeySpec(secret.getBytes(), "HmacSHA256");
            
            sha256_HMAC.init(secret_key);
            //sha256_HMAC.update(more_data);
            System.out.println(sha256_HMAC.doFinal(message.getBytes()));
        }
        
        catch (Exception e) {
            System.out.println("Error");
        }
    }

}
