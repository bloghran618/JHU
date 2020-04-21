/*
  This class utilizes methods to print the month as specified by the user
 */

import java.util.Scanner;

public class DisplayMonth
{
    public static void main(String[] args)
    {
        Scanner input = new Scanner(System.in);

        // user inputs month
        System.out.print( "Enter Month (1-12): " );
        int month_int = input.nextInt();

        // user inputs year
        System.out.print( "Enter year (A.D. please): " );
        int year = input.nextInt();

        printMonthCalendar(month_int, year);
        System.out.println();
    }

    /****
     The method printMonthCalendar() formats and prints a calendar from year
     and month input
     example:
              June  2018
     -----------------------------
     Sun Mon Tue Wed Thu Fri Sat
     1   2
     3   4   5   6   7   8   9
     10  11  12  13  14  15  16
     17  18  19  20  21  22  23
     24  25  26  27  28  29  30
     end example

     @param month is an integer value for given month
     @param year is an integer value for given year

     Pre-Conditions: The month value is 1-12
     the year value is a positive integer

     Post-Conditions: There is no return value, output to the screen
     ****/
    public static void printMonthCalendar( int month, int year )
    {
        printMonthHeader(month, year);
        printMonthBody(month, year);
    }

    /****
     The method printMonthHeader() formats and prints a header for a
     calendar.
     example:
             February  2018
     -----------------------------
     end example

     @param month is an integer value for given month
     @param year is an integer value for given year

     Pre-Conditions: The month value is 1-12
     the year value is a positive integer

     Post-Conditions: There is no return value, output to the screen.
     If you do not give proper month information the month will be blank
     ****/
    public static void printMonthHeader( int month, int year)
    {
        System.out.println();
        // convert integer month to string format
        String month_str = getMonthName(month);

        // format month, year header
        System.out.format("       %9s  " + year + "\n", month_str);
        System.out.println("-----------------------------");
    }

    /****
     The method printMonthBody() formats and prints a body for a
     calendar.
     example:
     Sun Mon Tue Wed Thu Fri Sat
                           1   2
       3   4   5   6   7   8   9
      10  11  12  13  14  15  16
      17  18  19  20  21  22  23
      24  25  26  27  28  29  30
     end example

     @param month is an integer value for given month
     @param year is an integer value for given year

     Pre-Conditions: The month value is 1-12
     the year value is a positive integer

     Post-Conditions: There is no return value, output to the screen.
     If you do not give proper month information it will not print any numbers
     ****/
    public static void printMonthBody( int month, int year )
    {
        // days_in_month will be used to determine if we are done printing
        int days_in_month = getNumDaysInMonth(month, year);

        // start_day is used to initialize the day of the week
        int start_day = getStartDay(month, year);

        // month_day and week_day are iterators
        int month_day = 1;
        int week_day = start_day;

        // week_string is modified until it is ready to print the week
        String week_string = "";

        // print days of the week
        System.out.println(" Sun Mon Tue Wed Thu Fri Sat ");

        while (month_day <= days_in_month) // iterate over all days in month
        {
            // iterate until week_day = 7 (Saturday)
            while (week_day <= 7 && month_day <= days_in_month)
            {
                week_string += String.format(" %2d ", month_day);
                month_day += 1;
                week_day += 1;
            }

            if (month_day < 15) // right align first half of month
            {
                System.out.format("%29s\n", week_string);
            }
            else // left align last half of month (helps with formatting)
            {
                System.out.format(" %-29s\n", week_string);
            }

            // reset the value of the week_string
            week_string = "";

            // reinitialize week_day to Monday (1)
            week_day = 1;
        }
    }

    /****
     The method getMonthName() returns a string representing the month of the
     year. The method assumes 1 = January, 2 = Febuary, ... (Just like you see
     the months on your credit card). If you enter a value that is not 1-12, it
     will return an empty String ""

     @param month is an integer value for given month
     @return the name of the month

     Pre-Conditions: The month value, m,  is 1-12

     Post-Conditions: A string is returned, unless the user input is
     outside of the 1-12 range, in which case "" is returned
     ****/
    public static String getMonthName( int month )
    {
        if (month == 1)
        {
            return "January";
        }
        else if (month == 2)
        {
            return "February";
        }
        else if (month == 3)
        {
            return "March";
        }
        else if (month == 4)
        {
            return "April";
        }
        else if (month == 5)
        {
            return "May";
        }
        else if (month == 6)
        {
            return "June";
        }
        else if (month == 7)
        {
            return "July";
        }
        else if (month == 8)
        {
            return "August";
        }
        else if (month == 9)
        {
            return "September";
        }
        else if (month == 10)
        {
            return "October";
        }
        else if (month ==11)
        {
            return "November";
        }
        else if (month == 12)
        {
            return "December";
        }
        else
        {
            return "";
        }
    }

    /****
     The method getStartDay() implements Zeller's Algorithm for determining the
     day of the week the first day of a month is. The method adjusts Zeller's
     numbering scheme for day of week ( 0=Saturday, ..., 6=Friday ) to conform
     to a day of week number that corresponds to common conventions (i.e.,
     1=Sunday, ..., 7=Saturday)

     Pre-Conditions: The month value, m,  is 1-12
     The year value, y, is the full year (e.g., 2012)

     Post-Conditions: A value of 1-7 is returned, representing the first day of
     the month: 1 = Sunday, ..., 7 = Saturday
     ****/

    public static int getStartDay( int month,  int year )
    {
        final int day = 1; // Must be set to day 1 for this to work.  JRD.


        // Adjust month number & year to fit Zeller's numbering system
        if ( month < 3 )
        {
            month = month + 12;
            year = year - 1;
        }

        int yearInCent = year % 100;      // k Calculate year within century
        int century = year / 100;      // j Calculate century term
        int firstDay  = 0;            // h Day number of first day in month 'm'

        firstDay = (day + (13 * (month + 1) / 5) + yearInCent +
                (yearInCent / 4) + (century / 4) + (5 * century)) % 7;

        // Convert Zeller's value to ISO value (1 = Mon, ... , 7 = Sun )
        int dayNum = ((firstDay + 6) % 7) + 1;

        return dayNum;
    }

    /****
     The method getNumDaysInMonth returns an integer value representing
     the number of days in a month (specified 1-12). The method takes
     into account leap years for February.

     @param month is an integer 1-12 representing the month
     @param year is a positive integer value representing the year
     @return the number of months

     Pre-Conditions: year is a positive integer
     month is 1-12

     Post-Conditions: An integer value is returned
     ****/
    public static int getNumDaysInMonth( int month, int year )
    {
        if (month == 1)
        {
            return 31;
        }
        else if (month == 2)
        {
            if (isLeapYear(year)) // leap years effect the number of days in Feb
            {
                return 29;
            }
            else
            {
                return 28;
            }
        }
        else if (month == 3)
        {
            return 31;
        }
        else if (month == 4)
        {
            return 30;
        }
        else if (month == 5)
        {
            return 31;
        }
        else if (month == 6)
        {
            return 30;
        }
        else if (month == 7)
        {
            return 31;
        }
        else if (month == 8)
        {
            return 31;
        }
        else if (month == 9)
        {
            return 30;
        }
        else if (month == 10)
        {
            return 31;
        }
        else if (month == 11)
        {
            return 30;
        }
        else if (month == 12) {
            return 31;
        }
        else
        {
            return 0;
        }
    }

    /****
     The method isLeapYear() returns a boolean value representing if the
     given year is a leap year or not

     @param year is a positive integer value representing the year
     @return true if leap year, false if not leap year

     Pre-Conditions: year is a positive integer

     Post-Conditions: A boolean value is returned
     ****/
    public static boolean isLeapYear( int year )
    {
        if (year % 4 != 0) {
            return false;
        }
        else if (year % 400 == 0)
        {
            return true;
        }
        else if (year % 100 == 0)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
}
