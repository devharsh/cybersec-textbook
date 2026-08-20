
import java.io.*;
import java.net.*;
import java.util.Date;

public class WebServer {

	  public static void main(String args[]) {
		  
		  ServerSocket server;
		  
		  try {
		    
			  server = new ServerSocket(80); //listen to port 8080
			  System.out.println("Server is running");
			  while (true){
				  
				  Socket sock = server.accept();
				  System.out.println("Connection accepted");
				  BufferedReader input = new BufferedReader(new InputStreamReader(sock.getInputStream()));
				  BufferedWriter output = new BufferedWriter(new OutputStreamWriter (sock.getOutputStream()));
			 
				  String str = null;
				  do{
					  str = input.readLine();
				  }
			        while (!str.equals(""));  //read until black line 
			          
			        
			        output.write("HTTP/1.0 200 OK"+"\n");
			        output.write("Content-Type: text/html"+"\n");
			        output.write("Date : "+ new Date()+"\n");
			        output.write("Server: MyApache Java based"+"\n");
			        output.write(""+"\n"); //empty line - end of headers
			        output.write("<title>My first HTTP Page</title>"+"\n");
			        output.write("<h1>Welcome 383, Time to go!</h1>"+"\n");  // HTML page
			        output.flush();
			        sock.close();
			        System.out.println("Connection closed");
			        
			  }
			  
		    }
		  catch(IOException ex){
			  
			  ex.printStackTrace();
		  }
		  
		  }
}
