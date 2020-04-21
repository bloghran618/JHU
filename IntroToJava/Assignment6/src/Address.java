/*
 * This class models an employees address
 */

public class Address
{
    String street;
    String city;
    String state;
    String zip;

    Address(String street, String city, String state, String zip)
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

        // set these values regardless of format
        this.street = street;
        this.city = city;
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
