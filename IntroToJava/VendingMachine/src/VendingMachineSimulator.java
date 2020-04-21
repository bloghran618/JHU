/**
 * This class is the vending machine main() method
 *
 * @author Brian Loughran
 */

import java.util.Arrays;
import java.util.Scanner;

public class VendingMachineSimulator
{
    public static void main(String[] args)
    {
        VendingItem[] VendingMachine = loadVendingMachine();
        MoneyInMachine money = new MoneyInMachine(5,
                10, 5, 0, 0,
                33, 0, 0);

        // Initialize user_selection to 1 so the menu prints on program open
        int user_selection = 1;

        Scanner input = new Scanner(System.in);

        while (user_selection != 5)
        {
            // print some empty lines to keep nice spacing
            System.out.println("\n");

            switch(user_selection)
            {
                case 1:
                {
                    // print menu
                    printMenu();
                    break;
                }

                case 2:
                {
                    // print vending inventory
                    printVendingInventory(VendingMachine);
                    break;
                }

                case 3:
                {
                    // display total money in the machine
                    money.displayCurrentMoney();
                    break;
                }

                case 4:
                {
                    // buy an item
                    buyItem(VendingMachine, money);
                    break;
                }

                default:
                {
                    System.out.println("Must enter an integer between 1-5");
                }
            }
            // get next user choice
            System.out.print("\nEnter Selection (1 for menu): ");
            user_selection = input.nextInt();

            if (user_selection == 5)
            {
                System.out.println("Thank you for shopping, have a nice day!");
            }
        }
    }

    /**
     * This function is used to create a loaded vending machine
     * This can be easily modified to load results from a file (.csv?)
     *
     * e.g.
     * Coke, Bottle, 150
     * Water, Bottle, 100
     * Lays, Bag, 100
     * ...
     *
     * @returns a list of VendingItems, representing a full vending machine
     */
    public static VendingItem[] loadVendingMachine()
    {
        /*
         * num_items designates the number of items to be loaded
         * if loading from a file one could scan the number of lines in the file
         */
        int num_items = 8;
        VendingItem[] Vend = new VendingItem[num_items];
        Vend[0] = new VendingItem("Coke", "Bottle", 150, 5);
        Vend[1] = new VendingItem("Water", "Bottle", 100, 3);
        Vend[2] = new VendingItem("Lays", "Bag", 100, 7);
        Vend[3] = new VendingItem("Doritos", "Bag", 100, 9);
        Vend[4] = new VendingItem("Twinkies", "Bag", 75, 1);
        Vend[5] = new VendingItem("Skittles", "Bag", 100, 7);
        Vend[6] = new VendingItem("Tic-Tacs", "Bin", 150, 6);
        Vend[7] = new VendingItem("Gum", "Pack", 50, 3);

        return Vend;
    }

    /**
     * This function prints the menu of available commands
     */
    public static void printMenu()
    {
        System.out.println("1. Print Menu");
        System.out.println("2. Display Inventory");
        System.out.println("3. Display Money In Machine");
        System.out.println("4. Purchase Item");
        System.out.println("5. Exit");
    }

    /**
     * This function prints the inventory of a given array of VendingItems
     *
     * @param machine Vending machine object from which to print inventory
     */
    public static void printVendingInventory(VendingItem[] machine)
    {
        System.out.println("\nMachine Inventory:\n\n");
        for(int i = 0; i < machine.length; i++)
        {
            System.out.format("%6s%-16s%9s%-4d\n", "Item: ", machine[i].getItem(),
                              "Quantity: ", machine[i].getQuantity());
        }
    }

    /**
     * This function prints the indexed inventory of a given array of VendingItems
     *
     * @param machine Vending machine from which to print the item indexx
     */
    public static void printVendingIndex(VendingItem[] machine)
    {
        System.out.println("\nMachine Inventory by Index:\n\n");
        for(int i = 0; i < machine.length; i++)
        {
            System.out.format("%7s%-4d%6s%-16s%9s%-4d\n", "Index: ", i,
                    "Item: ", machine[i].getItem(),
                    "Quantity: ", machine[i].getQuantity());
        }
    }

    /**
     * This function is used to buy an item
     *
     * @param machine an array of VendingItem[] representing inventory
     * @param cash_handler an object to help handle vending cash
     */
    public static void buyItem(VendingItem[] machine,
                               MoneyInMachine cash_handler)
    {
        Scanner input = new Scanner(System.in);

        printVendingIndex(machine);

        // get the index of selected item
        System.out.print("\nEnter index of desired item: ");
        int index = input.nextInt();

        // check that the given index is accessible in machine
        if (index >= 0 && index < machine.length &&
                machine[index].getQuantity() > 0)
        {
            // display key information about the item
            System.out.format("%6s%-12s%13s%-7d\n\n", "Item: ",
                    machine[index].getItem(), "Cost (*.01): ",
                    machine[index].getCost());

            // money is entered into the machine
            int total_input = cash_handler.userEntersMoney();

            if (total_input >= machine[index].getCost())
            {
                System.out.println("\nVending " + machine[index].getItem() +
                                   "...");
                machine[index].buyOne();

                // calculate and return appropriate change
                int return_change = total_input - machine[index].getCost();
                cash_handler.getChange(return_change);
            }
            else
            {
                System.out.println("\nDid not enter enough money, " +
                        "returning change...");
                // if a user did not enter enough money they are reimbursed
                cash_handler.getChange(total_input);
            }
        }
        else
        {
            System.out.println("Product not available for specified index");
        }
    }
}
