/*
 * This class models an employees hire date
 */

public class Date
{
    int day;
    int month;
    int year;

    Date(int day, int month, int year)
    {
        // set day if between 1-31
        if (day > 0 && day <= 31)
        {
            this.day = day;
        }
        else
        {
            throw new RuntimeException("Invalid day");
        }

        // set month if between 1-12
        if (month > 0 && month <= 12)
        {
            this.month = month;
        }
        else
        {
            throw new RuntimeException("Invalid month");
        }

        // set year if between 1900 and 2020
        if (year <= 1900)
        {
            throw new RuntimeException("This employee may be a vampire");
        }
        else if (year > 2020)
        {
            throw new RuntimeException("This employee was born in the future");
        }
        else
        {
            this.year = year;
        }
    }

    // formats date information
    public  void printDate()
    {
        System.out.println("Hire Date");
        System.out.println(this.month + "/" + this.day + "/" + this.year);
    }
}
