/*
 * This class creates and outputs employee information
 */

import java.util.Scanner;

public class MakeEmployees
{
    public static void main(String[] args)
    {
        int num_employees = 3;

        // create employee array object
        Employee[] employees = new Employee[num_employees];

        // create salaried employee
        Name name1 = new Name("Brian", "Loughran");
        Date date1 = new Date(10, 7, 2017);
        Address address1 = new Address("Cambridge", "Denville",
                "NJ", "07834");
        SalariedEmployee employee1 = new SalariedEmployee(name1, address1,
                date1, 50000);

        // create hourly employee that is a hard worker
        Name name2 = new Name("Brian", "Murray");
        Date date2 = new Date(1, 6, 2017);
        Address address2 = new Address("Ardmore", "West Hartford",
                "CT", "06119");
        HourlyEmployee employee2 = new HourlyEmployee(name2, address2,
                date2, 20.0, 60.0);

        // create hourly employee that is lazy
        Name name3 = new Name("Johnathan", "Magulio");
        Date date3 = new Date(10, 7, 2017);
        Address address3 = new Address("Farmington", "Hartford",
                "CT", "06120");
        HourlyEmployee employee3 = new HourlyEmployee(name3, address3,
                date3, 40.0, 30.0);

        // assign employees to employee array
        employees[0] = employee1;
        employees[1] = employee2;
        employees[2] = employee3;


        // output employee information
        for (int n = 0; n < num_employees; n++)
        {
            employees[n].printEmployee();
        }
    }
}
