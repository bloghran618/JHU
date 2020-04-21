/**
 * This class represents the stack of people in the narrow elevator
 *
 * @author Brian Loughran
 */

public class elevatorStack
{
    // using list implementation of stack, size is 5
    private Person[] stack;
    private int topIndex;

    public elevatorStack()
    {
        // intialize by creating size 5 stack
        this.stack = new Person[5];

        this.topIndex = -1;
    }

    /**
     * standard push stack operation
     *
     * @param person is the person to push to the stack
     */
    public void push(Person person)
    {
        // handle if the stack is full by throwing exception
        if(this.topIndex > 5)
        {
            throw new RuntimeException("Stack full");
        }
        else
        {
            this.stack[this.topIndex + 1] = person;
            this.topIndex ++;
        }
    }

    /**
     * Standard stack pop operation
     *
     * @return the Person on top of the stack
     */
    public Person pop()
    {
        // handle if stack is empty by throwing exception
        if(this.topIndex == -1)
        {
            throw new RuntimeException("Stack empty");
        }
        else
        {
            Person popPerson = this.stack[this.topIndex];
            this.stack[this.topIndex] = null;
            this.topIndex--;
            return popPerson;
        }
    }

    /**
     * Check if the stack is empty
     *
     * @return if the stack is empty
     */
    public boolean isEmpty()
    {
        if(this.topIndex == -1)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    /**
     * Check if the stack is full
     *
     * @return if the stack is full
     */
    public boolean isFull()
    {
        if(this.topIndex >= 4)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    /**
     * Count number of people leaving on floor
     *
     * @param destinationFloor the destination floor
     *
     * @return the number of people in stack departing at given floor
     */
    public int countDeparting(int destinationFloor)
    {
        int departingCount = 0;
        for(int i = 0; i < 5; i++)
        {
            if(this.stack[i] != null)
            {
                if(stack[i].getDestinationFloor() == destinationFloor)
                {
                    departingCount++;
                }
            }
        }
        return departingCount;
    }

    /**
     * Get the next requested floor in the elevator
     *
     * @param currentFloor the floor the elevator is currently on
     * @param goingUp determines if the elevator is going up (or down)
     *
     * @return the next floor requested by people in the elevator
     */
    public int getNextFloor(int currentFloor, boolean goingUp)
    {
        if(this.isEmpty())
        {
            return -1; //return code for empty elevator
        }

        int floor = currentFloor;

        // move next floor possible location
        if(goingUp)
        {
            floor ++;
        }
        else
        {
            floor--;
        }

        // look for destinations in our direction
        while(floor <= 5 && floor >= 1)
        {
            for(int i = 0; i < 5; i++) // iterate over each person in stack
            {
                if(this.stack[i] != null) // ignore empty entries
                {
                    if(this.stack[i].getDestinationFloor() == floor)
                    {
                        // get the next eligible floor
                        return floor;
                    }
                }
            }

            // move next floor possible location
            if(goingUp)
            {
                floor ++;
            }
            else
            {
                floor--;
            }
        }

        // if we did not find a floor going in our direction try the other way
        int currentDiff = 6;
        floor = currentFloor;

        for(int i = 0; i < 5; i++) // check each person in elevator
        {
            if(this.stack[i] != null) // check there is a person in this index
            {
                int diff = Math.abs(currentFloor -
                        this.stack[i].getDestinationFloor());
                if(diff < currentDiff) // check if this person is closer
                {
                    floor = this.stack[i].getDestinationFloor();
                    currentDiff = diff;
                }
            }
        }

        return floor;
    }

    /**
     * Get a list of names currently in the stack
     *
     * @return a list of space delimited names in the stack
     */
    public String getNames()
    {
        String returnString = "";

        if(this.topIndex == -1)
        {
            return "nobody";
        }
        else
        {
            for(int i = 0; i <= this.topIndex; i++)
            {
                returnString += this.stack[i].getName() + " ";
            }
        }
        return returnString;
    }

    /**
     * Set the stack variable
     *
     * @param stack a list Person of size 5
     */
    public void setStack(Person[] stack)
    {
        this.stack = stack;
    }

    /**
     * Get stack list
     *
     * @return the stack
     */
    public Person[] getStack()
    {
        return this.stack;
    }

    /**
     * Set topIndex variable
     *
     * @param topIndex the index of the top of the stack
     */
    public void setTopIndex(int topIndex)
    {
        this.topIndex = topIndex;
    }

    /**
     * Get topIndex variable
     *
     * @return the top index of the stack
     */
    public int getTopIndex()
    {
        return this.topIndex;
    }
}
