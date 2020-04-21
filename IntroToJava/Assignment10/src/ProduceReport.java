 /*
  * This class reads data from serialized file and produces a report
  */

 import java.io.*;

public class ProduceReport
{
    public static void main(String[] args)
    {
        // inputs
        String inputFilePath = args[0];
        int records = Integer.valueOf(args[1]); // should be # states (51)!!!

        // print input file path
        System.out.println("File: " + inputFilePath);

        // initializers
        ObjectInputStream infile = null;
        SummaryLine[] report = null;

        try
        {
            // restore infmation from serializable file
            infile = new ObjectInputStream(new BufferedInputStream(
                    new FileInputStream(inputFilePath)));

            report = (SummaryLine[]) infile.readObject();
            infile.close();
            System.out.println("Report restored from file");
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

        // print report
        report[0].printReportHeader();
        for (int i = 0; i < records; i++)
        {
            report[i].printReportLine();
        }
    }
}
