/*
 * This class models an employee
 */

public class Employee
{
    // name address and date are class objects
    Name name;
    Address address;
    Date date;

    Employee(Name name, Address address, Date date)
    {
        this.name = name;
        this.address = address;
        this.date = date;
    }

    // formats employee information
    public void printEmployee()
    {
        System.out.println("Employee\n");
        this.name.printName();
        System.out.println();
        this.address.printAddress();
        System.out.println();
        this.date.printDate();
        System.out.println("\n\n");
    }
}
