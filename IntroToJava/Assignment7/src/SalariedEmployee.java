/*
 * This class models a salaried employee, which extends employee
 */

public class SalariedEmployee extends Employee
{
    private int annual_salary;

    public SalariedEmployee(Name name, Address address, Date date,
                            int annual_salary)
    {
        super(name, address, date);
        if (annual_salary >= 0)
        {
            this.annual_salary = annual_salary;
        }
        else
        {
            throw new RuntimeException("Annual salary must be positive");
        }
    }

    public int getAnnualSalary()
    {
        return this.annual_salary;
    }

    public void setAnnualSalary(int annual_salary)
    {
        this.annual_salary = annual_salary;
    }

    // new print function for salaried workers
    @Override
    public void printEmployee()
    {
        System.out.println("Employee\n");
        super.name.printName();
        System.out.println();
        this.address.printAddress();
        System.out.println();
        this.date.printDate();

        System.out.println("\nWages");
        System.out.println("Annual Salary: $" + this.annual_salary);

        System.out.println("\n\n");
    }
}
