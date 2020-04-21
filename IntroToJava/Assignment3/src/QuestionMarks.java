/**
 * This class prints a user specified scalene right triangle of question marks
 *
 *         style1:            style2:     (height = 4)
 *         ????               ?
 *         ???                ??
 *         ??                 ???
 *         ?                  ????
 *
 **/

import java.util.Scanner;

public class QuestionMarks
{
    public static void main( String [] args )
    {
        Scanner input = new Scanner( System.in );

        // get max number of question marks on a line
        System.out.print( "Enter maximum number of question marks on a line: " );
        int triangle_height = input.nextInt();

        // get pattern
        System.out.print( "Enter pattern style (1 or 2): " );
        int style = input.nextInt();

        // iterate through each row of the triangle
        for (int row = 1; row <= triangle_height; row++)
        {
            // style == 1 prints the max # question marks on the first line
            if (style == 1)
            {
                for(int column = 1; column <= (triangle_height - row + 1); column++)
                {
                    System.out.print("?");
                }
                // move on to next line when specified columns are done printing
                System.out.print("\n");
            }
            // style == 2 prints the max # question marks on the last line
            else if (style == 2)
            {
                for (int column = 1; column <= row; column++)
                {
                    System.out.print("?");
                }
                // move on to next line when specified columns are done printing
                System.out.print("\n");
            }
        }
    }
}
