 /*
  * This is the "first" program in assignment 10
  * The goal of this class is to
  */

 import java.io.*;

 public class CreateDataFile
{
    public static void main(String[] args)
    {
        // get args
        String dataFilePath = args[0];
        String outFilePath = args[1];
        String recordsString = args[2]; // should be 13486
        Integer records = Integer.valueOf(recordsString);

        USSDTxtLine[] fileLines = new USSDTxtLine[records];

        try
        {
            // read file
            File dataFile = new File(dataFilePath);
            FileReader fileReader = new FileReader(dataFile);
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            String line;
            for(int i = 0; i < records; i++)
            {
                line = bufferedReader.readLine();

                // convert string index to proper field
                String stateCode = line.substring(0,2);
                String districtID = line.substring(3, 8);
                String districtName = line.substring(9,81);
                Integer totalPopulation = Integer.valueOf(line.substring(
                        82, 90).trim());
                Integer relevantPopulation = Integer.valueOf(line.substring(
                        91, 99).trim());
                Integer povertyChildren = Integer.valueOf(line.substring(
                        100, 108).trim());
                String tag = line.substring(109, 130);

                fileLines[i] = new USSDTxtLine(stateCode, districtID,
                        districtName, totalPopulation, relevantPopulation,
                        povertyChildren, tag);
            }
            fileReader.close();
        }
        catch(NullPointerException e)
        {
            System.out.println("Records var (args[2]) is too high");
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

        // must specify number of different district codes
        SummaryLine[] finalReport = new SummaryLine[51]; // Puerto Rico?

        // keep track of current districtID
        String stateCode = "";

        //keep track of index for summary file
        int stateIndex = -1;

        for(int j = 0; j < records; j++)
        {
            // if we are still in the same district as previous iteration
            if(stateCode.equals(fileLines[j].getStateCode()))
            {
                finalReport[stateIndex].addDistrict(fileLines[j]);
            }
            // if we have switched districts
            else
            {
                // iterate districtIndex
                stateIndex++;

                // set new districtID
                stateCode = fileLines[j].getStateCode();


                // create new SummaryLine at index
                finalReport[stateIndex] = new SummaryLine(
                        fileLines[j].getStateCode(),
                        fileLines[j].getDistrictID(),
                        fileLines[j].getDistrictName(),
                        fileLines[j].getTotalPopulation(),
                        fileLines[j].getRelevantPopulation(),
                        fileLines[j].getPovertyChildren(),
                        fileLines[j].getTag());
            }
        }

        try
        {
            // write serializable file
            ObjectOutputStream outfile = new ObjectOutputStream(
                    new BufferedOutputStream(
                            new FileOutputStream(outFilePath)));
            outfile.writeObject(finalReport);
            outfile.close();
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    }
}
