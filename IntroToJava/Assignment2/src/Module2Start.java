/**
 *  Output integers into an aligned table format
 **/

import java.util.Scanner;

public class Module2Start
{
    public static void main( String [] args )
    {
        // Define and initialize variables for values to be input
        int userNum1 = 0;
        int userNum2 = 0;
        int userNum3 = 0;
        int userNum4 = 0;
        int userNum5 = 0;
        int userNum6 = 0;

        // Use a Scanner to input integer values
        Scanner input = new Scanner( System.in );
        System.out.println( "\n\n" );
        System.out.print( "Enter 6 integers separated by a blank space:" );
        userNum1 = input.nextInt();     // Input first value
        userNum2 = input.nextInt();     // Input second value
        userNum3 = input.nextInt();     // Input third value
        userNum4 = input.nextInt();     // Input fourth value
        userNum5 = input.nextInt();     // Input fifth value
        userNum6 = input.nextInt();     // Input sixth value

        // Calculate values for "Total"
        int row1sum = userNum1 + userNum2;
        int row2sum = userNum3 + userNum4;
        int row3sum = userNum5 + userNum6;

        // Calculate values for the sum of the first three rows
        int col1sum = userNum1 + userNum3 + userNum5;
        int col2sum = userNum2 + userNum4 + userNum6;
        int col3sum = row1sum + row2sum + row3sum;

        // Display the table.
        System.out.println( "\n\n" );
        System.out.println( "\t" + "Value" + "\t" + "Value" + "\t" + "Total" );
        // System.out.format is used in case the int's are not the same length (e.g. 1 23 234 3 2 1)
        // Integer size is limited to 5 characters in length for proper table formatting
        System.out.format( "\t%-5d\t%-5d\t%-5d\n", userNum1, userNum2, row1sum );
        System.out.format( "\t%-5d\t%-5d\t%-5d\n", userNum3, userNum4, row2sum );
        System.out.format( "\t%-5d\t%-5d\t%-5d\n", userNum5, userNum6, row3sum );
        System.out.println( "\t" + "----" + "\t" + "----" + "\t" + "----");
        System.out.format( "\t%-5d\t%-5d\t%-5d\n", col1sum, col2sum, col3sum );
        System.out.println( "\n\n" );
    }
}
