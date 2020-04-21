import java.io.*;

public class FixShittyOnlineInputFiles
{
    public static void main(String args[])
    {
        String inputFile = "rev1K.dat";
        String outputFile = "validInputFiles/" + inputFile;
        String line = "";

        clearOutput(outputFile);

        try {
            BufferedReader br = new BufferedReader(new FileReader(inputFile));
            line = br.readLine();
        }
        catch(NullPointerException npe)
        {
            // do nothing
        }
        catch(FileNotFoundException fnf)
        {
            throw new RuntimeException("File was not found");
        }
        catch(Exception e)
        {
            System.out.println("Idk what this exception is");
        }

        String[] delimited = line.split(" +");

        for(String d: delimited)
        {
            Writer output;
            try
            {
                if(!d.isEmpty())
                {
                    // write the string to the end of the file
                    output = new BufferedWriter(new FileWriter(outputFile, true));
                    output.append(d + "\n");
                    output.close();
                }
            }
            catch (Exception exception)
            {
                // do nothing
            }
        }

        System.out.println("Done.");
    }

    public static void clearOutput(String file)
    {
        try
        {
            PrintWriter pw = new PrintWriter(file);
            pw.close();
        }
        catch (FileNotFoundException fileNotFound)
        {
            // do nothing
        }
    }
}
