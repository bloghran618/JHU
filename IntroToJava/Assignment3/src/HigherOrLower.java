/**
 * This class takes advantage of Java's Math.random() function to play
 * a game of "higher or lower" with the computer
 **/

import java.util.Scanner;
import java.util.Random;

public class HigherOrLower
{
    public static void main( String [] args )
    {
        Scanner input = new Scanner( System.in );

        // User will keep playing until playAgain is set to 0
        int playAgain = 1;

        while (playAgain != 0)
        {
            // get highest number the computer will generate
            System.out.println("Computer will generate a number between 1 and N ");
            System.out.print("Enter N: ");
            int N = input.nextInt();

            // get number of guesses
            System.out.print("How many guesses would you like to make? ");
            int guesses = input.nextInt();

            // turn variable will keep count of how many guesses the user has made
            int turn = 1;

            // initialize guess as 0 will never be randomNumber
            int guess = 0;
            int randomNumber = (int) (N * Math.random()) + 1;
            System.out.println("\n");

            while (turn <= guesses && guess != randomNumber) {
                // get user guess
                System.out.print("Guess a number between 1 and " + N + ": ");
                guess = input.nextInt();

                if (guess < randomNumber) {
                    System.out.println("Too Low!");
                } else if (guess > randomNumber) {
                    System.out.println("Too High!");
                } else if (guess == randomNumber) {
                    System.out.println("You got it!");
                    System.out.println("It only took you " + turn + " attempt(s)!");
                }
                // iterate turn variable
                turn++;
            }
            if (guess != randomNumber) {
                System.out.println("Out of turns, you lose!");
                System.out.println("The number you were looking for was: " + randomNumber);
            }
            // User decides if he/she wants to play again
            System.out.print("Would you like to play again (0 for no, anything else for yes)");
            playAgain = input.nextInt();
            System.out.println("\n\n");
        }
        System.out.println("Thank you for playing!");
    }
}
