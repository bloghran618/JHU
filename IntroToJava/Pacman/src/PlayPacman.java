/*
  This is a text-based, pacman inspired game
 */

import java.util.Scanner;
import java.util.Random;

public class PlayPacman
{
    public static void main(String[] args)
    {
        Scanner input = new Scanner(System.in);

        // initialize pacman
        String pacman_symb = "<";
        int pacman_x = 0;
        int pacman_y = 0;
        int next_pacman_x = 0;
        int next_pacman_y = 0;
        int [] next_pacman_loc = {0, 0};

        // initialize stats
        int num_commands = 0;
        int num_cookies_eaten = 0;

        // user input for number of rows
        System.out.print( "How many rows for Pacman board? " );
        int rows = input.nextInt();

        // user input for number of columns
        System.out.print( "How many columns for Pacman board? " );
        int cols = input.nextInt();

        String[][] board = initializeBoard(rows, cols);

        int user_choice = 1;
        while (user_choice != 5)
        {
            switch(user_choice)
            {
                case 1:
                    // print menu
                    printMenu();
                    printBoard(board, rows, cols);
                    break;

                case 2:
                    // turn left
                    board = turnPacmanCCW(pacman_symb, board,
                            pacman_x, pacman_y);
                    pacman_symb = board[pacman_y][pacman_x];
                    printBoard(board, rows, cols);

                    // keep count for the number of commands
                    num_commands ++;
                    break;

                case 3:
                    // turn right
                    board = turnPacmanCW(pacman_symb, board,
                            pacman_x, pacman_y);
                    pacman_symb = board[pacman_y][pacman_x];
                    printBoard(board, rows, cols);

                    // keep count for the number of commands
                    num_commands ++;
                    break;

                case 4:
                    // move pacman

                    // only move Pacman if he behaves and stays on the board
                    if (willPacmanLeaveBoard(pacman_symb, pacman_x, pacman_y,
                        rows, cols) == false)
                    {
                        next_pacman_loc = getPacamnNextLoc(pacman_symb,
                                pacman_x, pacman_y);
                        next_pacman_x = next_pacman_loc[0];
                        next_pacman_y = next_pacman_loc[1];

                        // check if Pacman will eat a cookie
                        if (board[next_pacman_y][next_pacman_x].equals("O"))
                        {
                            System.out.println("Pacman ate a cookie!\n");
                            num_cookies_eaten ++;
                        }
                        board = movePacman(board, pacman_x, pacman_y,
                                next_pacman_x, next_pacman_y, pacman_symb);
                        pacman_x = next_pacman_x;
                        pacman_y = next_pacman_y;
                    }
                    printBoard(board, rows, cols);

                    // keep count for the number of commands
                    num_commands ++;
                    break;

                default:
                    System.out.println("You must enter a number 1-5");
                    printMenu();
                    break;

            }

            // get next user choice
            System.out.print("\nEnter Selection (1 for menu): ");
            user_choice = input.nextInt();
            System.out.println();

            // exit the program and print stats
            if (user_choice == 5)
            {
                System.out.println("Number of commands: " + num_commands);
                float commands_per_cookie = (float)num_cookies_eaten /
                        num_commands;
                System.out.println("Number of cookies per command: " +
                        commands_per_cookie);
                System.out.println("Thank you for playing!");
            }

        }
    }

    /****
     The method initializeBoard returns a 2D array that is a representation
     of the Pacman board
     example (5x5):
     <..0.
     .0...
     00.00
     0....
     end example

     @param rows is an integer value for the number of rows
     @param cols is an integer value for the number of columns

     Pre-Conditions: rows and cols are positive integers

     Post-Conditions: board[][] is a 2D String array that represents the board
     < - Pacman
     . - empty space
     0 - cookie
       - Pacman has visited already
     ****/
    public static String[][] initializeBoard(int rows, int cols)
    {
        String[][] board = new String[rows][cols];
        for (int j = 0; j < cols; j++)
        {
            for (int i = 0; i < rows; i++)
            {
                // fill (rows x cols) array with "empty"
                board[i][j] = ".";
            }
        }

        // number of cookies is 8% of the board, rounded down
        double num_cookies = Math.floor(rows * cols * 8 / 100);

        // initialize x and y positions for cookie placement
        int x_coord = 0;
        int y_coord = 0;

        //iterable value to count the number of cookies placed
        int iter = 0;

        System.out.println("Number of cookies: " + num_cookies);
        while(iter < num_cookies)
        {
            // randomize position of the cookie
            x_coord = (int) (cols * Math.random());
            y_coord = (int) (rows * Math.random());

            /*
             * Cookies are allowed everywhere that they are not already and
             * not where Pacman will start (top-left)
             */
            if (board[y_coord][x_coord] == "." &&
                    (x_coord != 0 || y_coord != 0))
            {
                board[y_coord][x_coord] = "O";
                iter++;
            }
        }

        // place Pacman at start
        board[0][0] = "<";



        return board;
    }

    /****
     The method printBoard prints a 2D array that is a representation
     of the Pacman board
     example (5x5):
     <..0.
     .0...
     00.00
     0....
     end example

     @param board is a 2D array that is a representation of the board
     @param rows is an integer value for the number of rows
     @param cols is an integer value for the number of columns

     Pre-Conditions: board is 2D String array
     rows and cols are positive integers

     Post-Conditions: board[][] is a 2D String array that represents the board
     < - Pacman
     . - empty space
     0 - cookie
       - Pacman has visited already
     ****/
    public static void printBoard(String[][] board, int rows, int cols)
    {
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                System.out.print(board[i][j]);
            }
            System.out.println();
        }
    }

    /****
     The method printMenu() shows the user the commands available to
     them in this simple version of Pacman
     ****/
    public static void printMenu()
    {
        System.out.println();
        System.out.println("1. Menu");
        System.out.println("2. Turn Left");
        System.out.println("3. Turn Right");
        System.out.println("4. Move");
        System.out.println("5. Exit\n");
    }

    /****
     The method turnPacmanCCW takes the pacman symbol and returns a
     symbol of pacman rotated counter-clockwise

     @param pacman_symb specifies the current orientation of Pacman

     Pre-Conditions: Pacman is currently in orientation given

     Post-Conditions: board[][] is a 2D String array that represents the board
     < - Pacman
     . - empty space
     0 - cookie
       - Pacman has visited already
     ****/
    public static String[][] turnPacmanCCW(String pacman_symb, String[][] board,
                                          int pacman_x, int pacman_y)
    {
        String new_pacman_symb = "<";
        switch(pacman_symb)
        {
            case "<":
                new_pacman_symb = "V";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            case "V":
                new_pacman_symb = ">";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            case ">":
                new_pacman_symb = "^";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            case "^":
                new_pacman_symb = "<";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            default:
                System.out.println("Error in Pacman symbol!");
                break;
        }
        return board;
    }
    /****
     The method turnPacmanCW takes the pacman symbol and returns a
     symbol of pacman rotated clockwise

     @param pacman_symb specifies the current orientation of Pacman

     Pre-Conditions: Pacman is currently in orientation given

     Post-Conditions: board[][] is a 2D String array that represents the board
     < - Pacman
     . - empty space
     0 - cookie
       - Pacman has visited already
     ****/
    public static String[][] turnPacmanCW(String pacman_symb, String[][] board,
                                          int pacman_x, int pacman_y)
    {
        String new_pacman_symb = "<";
        switch(pacman_symb)
        {
            case "<":
                new_pacman_symb = "^";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            case "^":
                new_pacman_symb = ">";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            case ">":
                new_pacman_symb = "V";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            case "V":
                new_pacman_symb = "<";
                board[pacman_y][pacman_x] = new_pacman_symb;
                break;
            default:
                System.out.println("Error in Pacman symbol!");
                break;
        }
        return board;
    }

    /****
    The method willPacmanLeaveBoard checks to make sure Pacman is not
     going to leave the board

    @param pacman_symb specifies the current orientation of Pacman
    @param pacman_x specifies the current x location of Pacman
    @param pacman_y specifies the current y location of Pacman
    @param rows specifies the number of rows in the table
    @param cols specifies the number of columns in the table

    Pre-Conditions:  board is properly set up
    Pacman is currently at pacamn_x and pacman_y
    rows and cols are properly set up for the board

    Post-Conditions: return true if Pacman is trying to leave, false if not
     ****/
    public static boolean willPacmanLeaveBoard(String pacman_symb, int pacman_x,
                                               int pacman_y, int rows, int cols)
    {
        if (pacman_symb == "V" && pacman_y == 0)
        {
            return true;
        }
        else if (pacman_symb == "<" && pacman_x == cols - 1)
        {
            return true;
        }
        else if (pacman_symb == "^" && pacman_y == rows - 1)
        {
            return true;
        }
        else if (pacman_symb == ">" && pacman_x == 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    /****
     The method getPacmanNextLoc gets the next board location Pacman will
     occupy after a move has been fired

     @param pacman_symb specifies the current orientation of Pacman
     @param pacman_x specifies the current x location of Pacman
     @param pacman_y specifies the current y location of Pacman

     Pre-Conditions:  Pacman will not leave board
     Pacman is currently at pacamn_x and pacman_y

     Post-Conditions: return 1D array containing pacman_x and pacman_y
     If Pacman is not properly set up will likely return {0,0}
     ****/
    public static int[] getPacamnNextLoc(String pacman_symb, int pacman_x,
                                         int pacman_y)
    {
        int next_pacman_x = 0;
        int next_pacman_y = 0;

        switch(pacman_symb)
        {
            case "<":
                next_pacman_x = pacman_x + 1;
                next_pacman_y = pacman_y;
                break;
            case "^":
                next_pacman_x = pacman_x;
                next_pacman_y = pacman_y + 1;
                break;
            case ">":
                next_pacman_x = pacman_x - 1;
                next_pacman_y = pacman_y;
                break;
            case "V":
                next_pacman_x = pacman_x;
                next_pacman_y = pacman_y - 1;
                break;
            default:
                System.out.println("Error in Pacman symbol!");
                break;
        }

        int[] next_pacman_loc = {next_pacman_x, next_pacman_y};
        return next_pacman_loc;
    }

    /****
     The method movePacman edits the board with the new location of Pacman

     @param board is a 2D array specifying the board
     @param pacman_x specifies the current x location of Pacman
     @param pacman_y specifies the current y location of Pacman
     @param next_pacman_x specifies the next x location of Pacman
     @param next_pacman_y specifies the next y location of Pacman
     @param pacman_symb specifies the current orientation of Pacman

     Pre-Conditions:  Pacman will not leave board
     Pacman is currently at pacamn_x and pacman_y
     Pacman next location has been calculated correctly

     Post-Conditions: return a 2D array specifying the board
     ****/
    public static String[][] movePacman(String[][] board, int pacman_x,
                                        int pacman_y, int next_pacman_x,
                                        int next_pacman_y, String pacman_symb)
    {
        board[pacman_y][pacman_x] = " ";
        board[next_pacman_y][next_pacman_x] = pacman_symb;
        return board;
    }
}


