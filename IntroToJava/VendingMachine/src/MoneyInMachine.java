/**
 * This class keeps track of the money in the vending machine
 *
 * @author Brian Loughran
 */

import java.util.Scanner;

public class MoneyInMachine
{
    private int hundredth_coins; // e.g. number of pennies
    private int twentieth_coins; // e.g. number of nickels
    private int tenth_coins;     // e.g number of dimes
    private int quarter_coins;   // e.g. number of quarters
    private int half_coins;      // e.g. number of half-dollars
    private int one_bills;       // e.g. number of one dollar bills
    private int five_bills;      // e.g. number of five dollar bills
    private int ten_bills;       // e.g. number of ten dollar bills

    /**
     * Initialize the MoneyInMachine object
     *
     * @param hundredth_coins an integer representing 0.01 currency
     * @param twentieth_coins an integer representing 0.05 currency
     * @param tenth_coins an integer representing 0.10 currency
     * @param quarter_coins an integer representing 0.25 currency
     * @param half_coins an integer representing 0.50 currency
     * @param one_bills an integer representing 1.00 currency
     * @param five_bills an integer representing 5.00 currency
     * @param ten_bills an integer representing 10.00 currency
     */
    public MoneyInMachine(int hundredth_coins, int twentieth_coins,
                          int tenth_coins, int quarter_coins, int half_coins,
                          int one_bills, int five_bills, int ten_bills)
    {
        // make sure there are positive number of each denomination
        if (hundredth_coins >= 0 && twentieth_coins >= 0 && tenth_coins >= 0 &&
            quarter_coins >= 0 && half_coins >= 0 && one_bills >= 0 &&
                five_bills >= 0 && ten_bills >= 0)
        {
            this.hundredth_coins = hundredth_coins;
            this.twentieth_coins = twentieth_coins;
            this.tenth_coins = tenth_coins;
            this.quarter_coins = quarter_coins;
            this.half_coins = half_coins;
            this.one_bills = one_bills;
            this.five_bills = five_bills;
            this.ten_bills = ten_bills;
        }
        else
        {
            throw new RuntimeException("Must have positive number of each " +
                    "denomination");
        }
    }

    /**
     * Display the money in the machine
     */
    public void displayCurrentMoney()
    {
        System.out.println();
        System.out.println("Hundredth coins: " + this.hundredth_coins);
        System.out.println("Twentieth coins: " + this.twentieth_coins);
        System.out.println("Tenth coins: " + this.tenth_coins);
        System.out.println("Quarter coins: " + this.quarter_coins);
        System.out.println("Half coins: " + this.half_coins);
        System.out.println("One Bills: " + this.one_bills);
        System.out.println("Five Bills: " + this.five_bills);
        System.out.println("Ten Bills: " + this.ten_bills);
        System.out.println("Total (denomination = 0.01): " + this.getTotalMoney());
        System.out.println();
    }


    /**
     * Calculate change
     *
     * @param total_change an integer representing change (in pennies)
     *
     * @return an array of length 8 designating the change
     * format: [hundredth_coins, twentieth_coins, tenth_coins, quarter_coins,
     *          half_coins, one_bills, five_bills, ten_bills]
     */
    public int[] getChange(int total_change)
    {
        int[] change_array = new int[] {0, 0, 0, 0, 0, 0, 0, 0};

        // give change for ten bills if needed
        while (total_change >= 1000)
        {
            if (this.ten_bills > 0)
            {
                total_change -= 1000;
                this.ten_bills -= 1;
                change_array[0] += 1;
            }
            else
            {
                break;
            }
        }

        // give change for five bills if needed
        while (total_change >= 500)
        {
            if (this.five_bills > 0)
            {
                total_change -= 500;
                this.five_bills -= 1;
                change_array[1] += 1;
            }
            else
            {
                break;
            }
        }

        // give change for one bills if needed
        while (total_change >= 100)
        {
            if (this.one_bills > 0)
            {
                total_change -= 100;
                this.one_bills -= 1;
                change_array[2] += 1;
            }
            else
            {
                break;
            }
        }

        // give change for half coins if needed
        while (total_change >= 50)
        {
            if (this.half_coins > 0)
            {
                total_change -= 50;
                this.half_coins -= 1;
                change_array[3] += 1;
            }
            else
            {
                break;
            }
        }

        // give change for quarter coins if needed
        while (total_change >= 25)
        {
            if (this.quarter_coins > 0)
            {
                total_change -= 25;
                this.quarter_coins -= 1;
                change_array[4] += 1;
            }
            else
            {
                break;
            }
        }

        // give change for tenth coins if needed
        while (total_change >= 10)
        {
            if (this.tenth_coins > 0)
            {
                total_change -= 10;
                this.tenth_coins -= 1;
                change_array[5] += 1;
            }
            else
            {
                break;
            }
        }

        // give change for twenthieth coins if needed
        while (total_change >= 5)
        {
            if (this.twentieth_coins > 0)
            {
                total_change -= 5;
                this.twentieth_coins -= 1;
                change_array[6] += 1;
            }
            else
            {
                break;
            }
        }

        // give change for half coins if needed
        while (total_change >= 1)
        {
            if (this.hundredth_coins > 0)
            {
                total_change -= 1;
                this.hundredth_coins -= 1;
                change_array[7] += 1;
            }
            else
            {
                break;
            }
        }

        if (total_change != 0)
        {
            System.out.println("Error: Inadequate change in machine!");
        }

        System.out.println("Ten Bills returned: " + change_array[0]);
        System.out.println("Five Bills returned: " + change_array[1]);
        System.out.println("One Bills returned: " + change_array[2]);
        System.out.println(".50 Coins returned: " + change_array[3]);
        System.out.println(".25 Coins returned: " + change_array[4]);
        System.out.println(".10 Coins returned: " + change_array[5]);
        System.out.println(".05 Coins returned: " + change_array[6]);
        System.out.println(".01 Coins returned: " + change_array[7]);

        return change_array;
    }

    /**
     * Get total amount of money in the machine
     *
     * @return the total money in the machine in pennies
     */
    public int getTotalMoney()
    {
        int total = 0;

        total += this.hundredth_coins;
        total += this.twentieth_coins * 5;
        total += this.tenth_coins * 10;
        total += this.quarter_coins * 25;
        total += this.half_coins * 50;
        total += this.one_bills * 100;
        total += this.five_bills * 500;
        total += this.ten_bills * 1000;

        return total;
    }

    /**
     * Handle the user inputting money
     *
     * @return the total money put in the machine in pennies
     */
    public int userEntersMoney()
    {
        Scanner input = new Scanner(System.in);
        int denomination_quant;
        int total = 0;

        // handle user enters number of ten_bills
        System.out.print("Enter number of 10 bills: ");
        denomination_quant = input.nextInt();
        total += 1000 * denomination_quant;
        this.ten_bills += denomination_quant;

        // handle user enters number of five_bills
        System.out.print("Enter number of 5 bills: ");
        denomination_quant = input.nextInt();
        total += 500 * denomination_quant;
        this.five_bills += denomination_quant;

        // handle user enters number of one_bills
        System.out.print("Enter number of 1 bills: ");
        denomination_quant = input.nextInt();
        total += 100 * denomination_quant;
        this.one_bills += denomination_quant;

        // handle user enters number of half_coins
        System.out.print("Enter number of .50 coins: ");
        denomination_quant = input.nextInt();
        total += 50 * denomination_quant;
        this.half_coins += denomination_quant;

        // handle user enters number of quarter_coins
        System.out.print("Enter number of .25 coins: ");
        denomination_quant = input.nextInt();
        total += 25 * denomination_quant;
        this.quarter_coins += denomination_quant;

        // handle user enters number of tenth_coins
        System.out.print("Enter number of .10 coins: ");
        denomination_quant = input.nextInt();
        total += 10 * denomination_quant;
        this.tenth_coins += denomination_quant;

        // handle user enters number of twentieth_coins
        System.out.print("Enter number of .05 coins: ");
        denomination_quant = input.nextInt();
        total += 5 * denomination_quant;
        this.twentieth_coins += denomination_quant;

        // handle user enters number of ten_bills
        System.out.print("Enter number of .01 coins: ");
        denomination_quant = input.nextInt();
        total += 1 * denomination_quant;
        this.hundredth_coins += denomination_quant;

        System.out.println("You entered " + total + " (in .01)");

        return total;
    }

    /**
     * Set hundredth coin variable
     *
     * @param hundredth_coins the number of hundredth coins
     */
    public void setHundredth_coins(int hundredth_coins)
    {
        this.hundredth_coins = hundredth_coins;
    }

    /**
     * Get hundredth coin variable
     *
     * @return the number of hundredth coins in the machine
     */
    public int getHundredth_coins()
    {
        return this.hundredth_coins;
    }

    /**
     * Set twentieth coin variable
     *
     * @param twentieth_coins the number of twentieth coins
     */
    public void setTwentieth_coins(int twentieth_coins)
    {
        this.twentieth_coins = twentieth_coins;
    }

    /**
     * Get twentieth coin variable
     *
     * @return the number of twentieth coins in the machine
     */
    public int getTwentieth_coins()
    {
        return this.twentieth_coins;
    }

    /**
     * Set tenth coin variable
     *
     * @param tenth_coins the number of tenth coins
     */
    public void setTenth_coins(int tenth_coins)
    {
        this.tenth_coins = tenth_coins;
    }

    /**
     * Get tenth coin variable
     *
     * @return the number of tenth coins in the machine
     */
    public int getTenth_coins()
    {
        return this.tenth_coins;
    }

    /**
     * Set quarter coin variable
     *
     * @param quarter_coins the number of quarter coins
     */
    public void setQuarter_coins(int quarter_coins)
    {
        this.quarter_coins = quarter_coins;
    }

    /**
     * Get quarter coin variable
     *
     * @return the number of quarter coins in the machine
     */
    public int getQuarter_coins()
    {
        return this.quarter_coins;
    }

    /**
     * Set half coin variable
     *
     * @param half_coins the number of half coins
     */
    public void setHalf_coins(int half_coins)
    {
        this.half_coins = half_coins;
    }

    /**
     * Get half coin variable
     *
     * @return the number of half coins in the machine
     */
    public int getHalf_coins()
    {
        return this.half_coins;
    }

    /**
     * Set one bill variable
     *
     * @param one_bills the number of one bills
     */
    public void setOne_bills(int one_bills)
    {
        this.one_bills = one_bills;
    }

    /**
     * Get one bill variable
     *
     * @return the number of one bills in the machine
     */
    public int getOne_bills()
    {
        return this.one_bills;
    }

    /**
     * Set five bill variable
     *
     * @param five_bills the number of five bills
     */
    public void setFive_bills(int five_bills)
    {
        this.five_bills = five_bills;
    }

    /**
     * Get five bill variable
     *
     * @return the number of five bills in the machine
     */
    public int getFive_bills()
    {
        return this.five_bills;
    }

    /**
     * Set ten bill variable
     *
     * @param ten_bills the number of ten bills
     */
    public void setTen_bills(int ten_bills)
    {
        this.ten_bills = ten_bills;
    }

    /**
     * Get ten bill variable
     *
     * @return the number of ten bills in the machine
     */
    public int getTen_bills()
    {
        return this.ten_bills;
    }
}
