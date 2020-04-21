/**
 *  Calculates a person's BMI based on height and weight inputs
 **/

import java.util.Scanner;

public class BMICalculator
{
    public static void main( String [] args )
    {
        System.out.println( "Body Mass Calculator\n" );

        // height and weight need to be floats for proper division later
        double height = 0.0;
        double weight = 0.0;

        Scanner input = new Scanner( System.in );

        // get height in inches and convert to meters
        System.out.print( "Enter height in inches: " );
        height = input.nextInt() * 0.0254;

        // get weight in pounds and convert to kilograms
        System.out.print( "Enter weight in pounds: " );
        weight = input.nextInt() * 0.45359237;

        // Calculate and output BMI
        double BMI = weight / (height * height);
        System.out.println( "Body Mass Index: " + BMI + "\n" );

        // Prints helpful information from the National Institutes of Health
        System.out.println("\t\tUnderweight: less than 18.5" );
        System.out.println("\t\tNormal: 18.5 - 24.9" );
        System.out.println("\t\tOverweight: 25 - 29.9" );
        System.out.print("\t\tObease: 30 or greater" );
    }
}
