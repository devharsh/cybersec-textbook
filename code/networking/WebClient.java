
import java.net.*;
import java.io.*;

public class WebClient {
    public static void main(String[] args)  {
      try{
        
    	String address = "www.google.com"; 
    	 // InetAddress address = InetAddress.getLocalHost(); //get local IP address
    	//  address="127.0.0.1" //localhost

    	  
        int port = 80;
        //Create Socket
        Socket sock=new Socket(address, port);


        //Create the streams to exchange data
        
        BufferedReader instream = new BufferedReader (new InputStreamReader (sock.getInputStream()));
        BufferedWriter outstream = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));

        //Follow the HTTP Protocol
        
        String request = "GET / HTTP/1.0\n\n";
        String response;

        System.out.println("Sending Messages to the Server... :"+request);
        System.out.println("Connecting to "+ sock.getInetAddress()+ " and port "+sock.getPort());
        System.out.println("Local Address :"+sock.getLocalAddress()+" Port :"+sock.getLocalPort());
           
        //write to the stream 
          outstream.write(request);
          outstream.flush();
           
         // read from the stream
           System.out.println("The server says: ");
           while ( (response = instream.readLine()) != null)
              System.out.println(response);
           
           
        instream.close();
        outstream.close();
        sock.close();
        System.out.println("Connection Closing...");
        
        }
      catch (IOException ex){
          System.out.println("Error during I/O");
          ex.getMessage();
          ex.printStackTrace();
        }
    }}
