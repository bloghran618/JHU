/*
 * This class models an employee
 */

public class Employee
{
    // name address and date are class objects
    protected Name name;
    protected Address address;
    protected Date date;

    public Employee(Name name, Address address, Date date)
    {
        this.name = name;
        this.address = address;
        this.date = date;
    }

    public Name getNane()
    {
        return this.name;
    }

    public void setName(Name name)
    {
        this.name = name;
    }

    public Address getAddress()
    {
        return this.address;
    }

    public void setAddress(Address address)
    {
        this.address = address;
    }

    public Date getDate()
    {
        return this.date;
    }

    public void setDate(Date date)
    {
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
