 /*
  * This class is used to model a print job
  */

 import java.util.Random;

public class Job
{
    private int jobNumber;
    private int printTime;

    public Job(int jobNumber)
    {
        if(jobNumber >= 0)
        {
            this.jobNumber = jobNumber;

            // random print time is created on job initialization
            Random rnGenerator = new Random();
            this.printTime = rnGenerator.nextInt(991) + 10;
        }
        else
        {
            System.out.println("Invalid Printer Job Input");
        }
    }

    // print nice string to show job information
    public void formatJob()
    {
        System.out.format("%-10d%-10d\n", this.jobNumber, this.printTime);
    }

    public int getJobNumber()
    {
        return this.jobNumber;
    }

    public void setJobNumber(int jobNumber)
    {
        this.jobNumber = jobNumber;
    }

    public int getPrintTime()
    {
        return this.printTime;
    }

    public void setPrintTime(int printTime)
    {
        this.printTime = printTime;
    }
}
