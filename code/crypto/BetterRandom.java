import java.security.SecureRandom;

public class BetterRandom {

    public static void main(String args[])
    {
        // create instance of SecureRandom class
        SecureRandom rand = new SecureRandom();

	for(int i=0; i<10; i++) {
        // Generate random integer in range 0 to 9
        int rand_int1 = rand.nextInt(10);
        int rand_int2 = rand.nextInt(10);

        // Print random integers
        System.out.println(rand_int1 + "\t" + rand_int2);
	}
    }
}
