import java.util.Random;

public class UnsecureRandom {

    public static void main(String args[])
    {
        // create instance of Random class
        Random rand = new Random();
	//Random rand = new Random(10);

	for(int i=0; i<10; i++) {
        // Generate random integer in range 0 to 9
        int rand_int1 = rand.nextInt(10);
        int rand_int2 = rand.nextInt(10);

        // Print random integers
        System.out.println(rand_int1 + "\t" + rand_int2);
	}
    }
}
