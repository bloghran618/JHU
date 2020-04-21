/*
 * This class models an hourly employee, which extends employee
 */

public class HourlyEmployee extends Employee
{
    double hourly_rate;
    double hours_worked;
    double earnings;

    public HourlyEmployee(Name name, Address address, Date date,
                          double hourly_rate, double hours_worked)
    {
        super(name, address, date);

        if (hourly_rate >= 0)
        {
            this.hourly_rate = hourly_rate;
        }
        else
        {
            throw new RuntimeException("Hourly rate must be positive");
        }

        if (hours_worked >= 0)
        {
            this.hours_worked = hours_worked;
        }
        else
        {
            throw new RuntimeException("Hours worked must be positive");
        }

        // calculate earnings based on class function
        this.earnings = calcEarnings(hourly_rate, hours_worked);
    }

    public double getHourlyRate()
    {
        return this.hourly_rate;
    }

    public void setHourlyRate(float hourly_rate)
    {
        this.hourly_rate = hourly_rate;
    }

    public double getHoursWorked()
    {
        return this.hours_worked;
    }

    public void setHoursWorked(float hours_worked)
    {
        this.hours_worked = hours_worked;
    }

    public double getEarnings()
    {
        return this.earnings;
    }

    // earnings is calculated based on hourly rate and hours worked
    public double calcEarnings(double hourly_rate, double hours_worked)
    {
        double earnings;

        // overtime hours are worth double the cash
        if (hours_worked > 40)
        {
            double overtime_hours = hours_worked - 40;
            earnings = (40 * hourly_rate) + (overtime_hours * hourly_rate *
                    15 / 10);
        }
        else
        {
            earnings = hourly_rate * hours_worked;
        }
        return earnings;
    }

    // new print function for hourly workers
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
        System.out.println("Hours Worked: " + this.hours_worked);
        System.out.println("Hourly Rate: " + this.hourly_rate);
        System.out.println("Total Earnings: $" + this.earnings);

        System.out.println("\n\n");
    }
}
