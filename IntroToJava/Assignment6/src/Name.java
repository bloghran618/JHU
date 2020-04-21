/*
 * This class models and employees full name
 */

public class Name
{
    public String first;
    public String last;

    Name(String first, String last)
    {
        this.first = first;
        this.last = last;
    }

    // formats name information
    public void printName()
    {
        System.out.println("Name");
        System.out.println(this.first + " " + this.last);
    }

}
