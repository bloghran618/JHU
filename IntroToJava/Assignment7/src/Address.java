/*
 * This class models an employees address
 */

public class Address
{
    private String street;
    private String city;
    private String state;
    private String zip;

    public Address(String street, String city, String state, String zip)
    {
        // check that state is two characters long
        if (state.length() != 2)
        {
            throw new RuntimeException("State String not two characters");
        }
        else
        {
            this.state = state;
        }

        // make sure zip is 5 character long integer
        if (zip.length() == 5)
        {
            this.zip = zip;
        }
        else
        {
            throw new RuntimeException("Invalid zip code");
        }

        if (street != "")
        {
            this.street = street;
        }
        else
        {
            throw new RuntimeException("Street can not be blank");
        }

        if (city != "")
        {
            this.city = city;
        }
        else
        {
            throw new RuntimeException("City can not be blank");
        }
    }

    public String getStreet()
    {
        return this.street;
    }

    public void setStreet(String street)
    {
        this.street = street;
    }

    public String getCity()
    {
        return this.city;
    }

    public void setCity(String city)
    {
        this.city = city;
    }

    public String getState()
    {
        return this.state;
    }

    public void setState(String state)
    {
        this.state = state;
    }

    public String getZip()
    {
        return this.zip;
    }

    public void setZip(String zip)
    {
        this.zip = zip;
    }

    public String toString()
    {
        return this.street + ", " + this.city + "\n" +
                this.state + ", " + this.zip;
    }

    // formats address information
    public void printAddress()
    {
        System.out.println("Address");
        System.out.println("Street: " + this.street);
        System.out.println("City: " + this.city);
        System.out.println("State: " + this.state);
        System.out.println("Zip: " + this.zip);
    }
}
