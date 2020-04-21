/*
 * This class creates and outputs employee information
 */

import java.util.Scanner;

public class makeEmployees
{
    public static void main(String[] args)
    {
        Scanner input  = new Scanner(System.in);
        Scanner keyboard = new Scanner(System.in);

        // user inputs number of employees
        System.out.print("How many employees would you like to create: ");
        int num_employees = input.nextInt();

        // create employee array object
        Employee[] employees = new Employee[num_employees];

        for (int n = 1; n <= num_employees; n++)
        {
            System.out.println("Enter information for employee number " + n);

            // user inputs first name
            System.out.print("Enter employee " + n + " first name: ");
            String first = keyboard.nextLine();

            // user inputs last name
            System.out.print("Enter employee " + n + " last name: ");
            String last = keyboard.nextLine();

            // create name
            Name name = new Name(first, last);

            // user inputs street
            System.out.print("Enter employee " + n + " street: ");
            String street = keyboard.nextLine();

            // user inputs city
            System.out.print("Enter employee " + n + " city: ");
            String city = keyboard.nextLine();

            // user inputs state (two letters)
            System.out.print("Enter employee " + n + " state (NJ): ");
            String state = keyboard.nextLine();

            // user inputs zip
            System.out.print("Enter employee " + n + " zip code: ");
            String zip = keyboard.nextLine();

            // create address
            Address address = new Address(street, city, state, zip);

            // user inputs month
            System.out.print("Enter employee " + n + " start month (1-12): ");
            int month = input.nextInt();

            // user inputs day
            System.out.print("Enter employee " + n + " start day: ");
            int day = input.nextInt();

            // user inputs year
            System.out.print("Enter employee " + n + " start year: ");
            int year = input.nextInt();

            // create start date
            Date date = new Date(day, month, year);

            // create employee
            Employee employee = new Employee(name, address, date);

            employees[n - 1] = employee;

            System.out.println("\n");
        }

        System.out.println("User input summary: \n\n\n\n");

        // output employee information
        for (int n = 0; n < num_employees; n++)
        {
            employees[n].printEmployee();
        }
    }
}
