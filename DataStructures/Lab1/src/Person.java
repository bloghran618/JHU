 /**
  * This class represents a person on the elevator
  *
  * @author Brian Loughran
  */

public class Person
{
    private String name;
    private int originFloor;
    private int destinationFloor;
    private int exitedTemporarily;

    public Person(String name, int originFloor, int destinationFloor)
    {
        if(name == "")
        {
            throw new RuntimeException("Name cannot be blank");
        }
        else if(name == null)
        {
            throw new RuntimeException("Name cannot be null");
        }
        else if(originFloor > 5 || originFloor <= 0)
        {
            throw new RuntimeException("Origin Floor must be 0-5");
        }
        else if(destinationFloor > 5 || destinationFloor < 0)
        {
            throw new RuntimeException("Destination Floor must be 0-5");
        }
        else
        {
            this.name = name;
            this.originFloor = originFloor;
            this.destinationFloor = destinationFloor;
            this.exitedTemporarily = 0; // initialize to 0
        }
    }

    /**
     * Format the person into a string
     *
     * @return a string representing the person
     */
    public String getPersonString()
    {
        return this.name + "\t" + this.originFloor + "\t" +
                this.destinationFloor;
    }

    /**
     * Add one to exitedTemporarily variable
     */
    public void incExitedTemporarily()
    {
        this.exitedTemporarily++;
    }

    /**
     * Set name variable
     *
     * @param name the name of the person
     */
    public void setName(String name)
    {
        this.name = name;
    }

    /**
     * Get name variable
     *
     * @return the name
     */
    public String getName()
    {
        return this.name;
    }

    /**
     * Set originFloor variable
     *
     * @param originFloor the origin floor of the person
     */
    public void setOriginFloor(int originFloor)
    {
        this.originFloor = originFloor;
    }

    /**
     * Get originFloor variable
     *
     * @return the origin floor
     */
    public int getOriginFloor()
    {
        return this.originFloor;
    }

    /**
     * Set destinationFloor variable
     *
     * @param destinationFloor the destinationFloor of the person
     */
    public void setDestinationFloor(int destinationFloor)
    {
        this.destinationFloor = destinationFloor;
    }

    /**
     * Get destinationFloor variable
     *
     * @return the destination floor
     */
    public int getDestinationFloor()
    {
        return this.destinationFloor;
    }

    /**
     * Set exitedTemporarily variable
     *
     * @param exitedTemporarily the # times had to exit temporarily
     */
    public void setExitedTemporarily(int exitedTemporarily)
    {
        this.exitedTemporarily = exitedTemporarily;
    }

    /**
     * Get exitedTemporarily variable
     *
     * @return the # times had to exit temporarily
     */
    public int getExitedTemporarily()
    {
        return this.exitedTemporarily;
    }

}
