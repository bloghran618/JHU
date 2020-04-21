 /*
  * This class represents a single contact
  */

 import java.io.Serializable;

 public class Contact
{
    private String first;
    private String last;
    private String company;
    private String phone;
    private String email;
    private String firstLastKey;

    public Contact(String first, String last, String company,
                   String phone, String email)
    {
        if(first != "" && last != "" && company != "" && phone != ""
                && email != "")
        {
            this.first = first;
            this.last = last;
            this.company = company;
            this.phone = phone;
            this.email = email;
            this.firstLastKey = last + " " + first;
        }
        else
        {
            throw new RuntimeException("Contact fields cannot be blank");
        }
    }

    // format string for file format
    public String writeFileString()
    {
        return String.format("%-10s%-15s%-25s%-20s%-40s", this.first, this.last,
                this.company, this.phone, this.email);
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

    public String getCompany()
    {
        return this.company;
    }

    public void setCompany(String company)
    {
        this.company = company;
    }

    public String getPhone()
    {
        return this.phone;
    }

    public void setPhone(String phone)
    {
        this.phone = phone;
    }

    public String getEmail()
    {
        return this.email;
    }

    public void setEmail(String email)
    {
        this.email = email;
    }

    public String getFirstLastKey()
    {
        return this.firstLastKey;
    }

    public void setFirstLastKey(String firstLastKey)
    {
        this.firstLastKey = firstLastKey;
    }
}
