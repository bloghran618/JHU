/*
 * This class models and employees full name
 */

public class Name
{
    private String first;
    private String last;

    public Name(String first, String last)
    {
        if (first != "")
        {
            this.first = first;
        }
        else
        {
            throw new RuntimeException("First name can not be blank");
        }

        if (last != "")
        {
            this.last = last;
        }
        else
        {
            throw new RuntimeException("Last name can not be blank");
        }
    }

    public String getFirst()
    {
        return this.first;
    }

    public void setFirst(String first)
    {
        this.first = first;
    }

    public String getLast()
    {
        return this.last;
    }

    public void setLast(String last)
    {
        this.last = last;
    }

    public String toString()
    {
        return this.first + " " + this.last;
    }

    // formats name information
    public void printName()
    {
        System.out.println("Name");
        System.out.println(toString());
    }

}
