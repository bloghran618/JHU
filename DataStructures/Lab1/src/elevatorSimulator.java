/**
 * This class is the main class to run the elevator simulation
 *
 * It is a simple simulation of people entering an exiting a narrow elevator
 * which is modeled with a stack.
 *
 * @author Brian Loughran
 */

import java.io.*;

public class elevatorSimulator {

    public static void main(String args[]) {
        // read the name of the input file as a string
        String loadFile = args[0];

        String outputFile = args[1];

        // clear contents of output file, if it exists
        try {
            PrintWriter pw = new PrintWriter(outputFile);
            pw.close();
        } catch (FileNotFoundException fileNotFound) {
            // do nothing
        }

        // read the input file and create a list of type Person
        Person[] loadList = readLoadList(loadFile, outputFile);

        // print parsed input to output file
        writeToOutputFile(outputFile, "\nRecognized Input: ");
        writeToOutputFile(outputFile, "Format: Name  Origin  Destination " +
                "(same as input file)");
        // used to iterate over people in loadList
        int j = 0;
        while(loadList[j] != null)
        {
            writeToOutputFile(outputFile, loadList[j].getPersonString());
            j++;
        }

        // to keep track of the number of people who could not get on
        int stairsPeople = 0;

        // keep track of people who rode
        int riders = 0;

        // keep track of the number of times the elevator was empty
        int timesEmpty = 0;

        elevatorStack stack = new elevatorStack();
        int floor = 1; // start on the first floor
        boolean goingUp = true;
        int nextFloorPassengerRequest;
        int nextFloorOutsideRequest;
        boolean isPeopleWaiting = true; // condition to see if we are done

        j = 0; // iterator

        while (loadList[j] != null) {
            // write to output arrival floor and passengers
            writeToOutputFile(outputFile, "");
            writeToOutputFile(outputFile, "Arriving at floor " +
                    floor);
            writeToOutputFile(outputFile, "Arriving with " +
                    stack.getNames());

            // write if the elevator is empty
            if (stack.isEmpty()) {
                writeToOutputFile(outputFile, "Elevator is empty");
                timesEmpty++;
            }

            // first unload people from the elevator
            handlePeopleDeparting(stack, floor, outputFile);

            // next load the people waiting on the current floor
            while (loadList[j].getOriginFloor() == floor &&
                    isPeopleWaiting == true) {

                if(stack.isFull())
                {
                    stairsPeople++; // keep track if have to take the stairs
                }
                stack = handlePeopleEntering(stack, loadList[j], outputFile);

                if(loadList[j+1] != null)
                {
                    j++;
                    riders++;
                }
                else
                {
                    isPeopleWaiting = false;
                }
            }

            // print if elevator is full
            if (stack.getTopIndex() == 4) {
                writeToOutputFile(outputFile, "Elevator is full");
            }

            // get next floor for passengers and outsiders
            nextFloorPassengerRequest = stack.getNextFloor(floor, goingUp);
            nextFloorOutsideRequest = loadList[j].getOriginFloor();

            // change status of going up if we have to
            goingUp = checkGoingUp(goingUp, floor, nextFloorPassengerRequest,
                    nextFloorOutsideRequest);

            // move to the next floor
            floor = getNextFloor(goingUp, floor, nextFloorPassengerRequest,
                    nextFloorOutsideRequest);

            // write out who we are leaving with
            writeToOutputFile(outputFile, "Departing with " +
                    stack.getNames());

            if(isPeopleWaiting == false)
            {
                // increment iterable to trigger end case
                j++;
                riders++;
            }
        }


        // depart the current floor and unload final passengers
        nextFloorPassengerRequest = stack.getNextFloor(floor, goingUp);
        goingUp = simpleCheckGoingUp(goingUp, floor, nextFloorPassengerRequest);
        floor = stack.getNextFloor(floor, goingUp);

        // unload the last of the people from the elevator
        while(stack.isEmpty() == false)
        {
            // write to output arrival floor and passengers
            writeToOutputFile(outputFile, "");
            writeToOutputFile(outputFile, "Arriving at floor " +
                    floor);
            writeToOutputFile(outputFile, "Arriving with " +
                    stack.getNames());

            // unload people from the elevator
            handlePeopleDeparting(stack, floor, outputFile);

            if(stack.isEmpty() == false)
            {
                // depart the current floor and unload final passengers
                nextFloorPassengerRequest = stack.getNextFloor(floor, goingUp);
                goingUp = simpleCheckGoingUp(goingUp, floor,
                        nextFloorPassengerRequest);
                floor = stack.getNextFloor(floor, goingUp);
                writeToOutputFile(outputFile, "Departing with " +
                        stack.getNames());
            }
        }

        // write some stats to the output file
        writeToOutputFile(outputFile, "\n");
        writeToOutputFile(outputFile, "Number of people who " +
            "rode: " + riders);
        writeToOutputFile(outputFile, "Number of people who " +
            "took the stairs: " + stairsPeople);
        writeToOutputFile(outputFile, "Number of times the " +
            "elevator was empty: " + timesEmpty);

        writeToOutputFile(outputFile, "The simulation is complete");
    }

    /**
     * Parse the input
     *
     * @param loadFile the path of the input file (.txt)
     * @param outputFile the path of the output file (.txt)
     *
     * @return a list of Person that is the order people enter the elevator
     */
    public static Person[] readLoadList(String loadFile, String outputFile) {
        String line;

        // max memory of the Person array is 1000 people
        Person[] elevatorList = new Person[1000];

        // iterator to keep track where in array we are
        int i = 0;

        try {
            BufferedReader br = new BufferedReader(new FileReader(loadFile));

            // throw out the first two lines of the file
            br.readLine();
            br.readLine();

            while ((line = br.readLine()) != null && line != "") {
                try {
                    String[] tabDelimitedLine = line.split("\t");

                    String name = tabDelimitedLine[0];
                    int originFloor = Integer.parseInt(tabDelimitedLine[1]);
                    int destinationFloor = Integer.parseInt(tabDelimitedLine[2]);

                    Person thisPerson = new Person(name, originFloor, destinationFloor);
                    elevatorList[i] = thisPerson;

                    i++;
                } catch (Exception e) {
                    writeToOutputFile(outputFile,
                            "Unrecognized input: " + line);
                }
            }
        } catch (FileNotFoundException notFound) {
            System.out.println("File not found");
        } catch (IOException e) {
            e.printStackTrace();
        }
        return elevatorList;
    }

    /**
     * Deal with people wanting to leave the elevator
     *
     * @param stack the people lined up in the elevator
     * @param destinationFloor the floor we have arrived at
     * @param outputFile the path of the output file (.txt)
     *
     * @return the updated stack of people lined up in the elevator
     */
    public static elevatorStack handlePeopleDeparting(elevatorStack stack,
                                                      int destinationFloor,
                                                      String outputFile) {
        int departingCount = stack.countDeparting(destinationFloor);
        int departed = 0;

        // keep track of people need to be reloaded into elevator
        int numInHallway = 0;
        Person[] inHallway = new Person[5];

        while (departed < departingCount)
        {
            Person offElevator = stack.pop();
            if (offElevator.getDestinationFloor() == destinationFloor) {
                departed++;

                // write some info to the file when a person leaves
                writeToOutputFile(outputFile, offElevator.getName() +
                " has left the elevator\n" + offElevator.getName() +
                " had to leave the elevator temporarily " +
                offElevator.getExitedTemporarily() + " times");

            }
            else
            {
                // put the person in the hallway before they reload
                inHallway[numInHallway] = offElevator;
                offElevator.incExitedTemporarily();
                numInHallway++;
            }
        }

        while (numInHallway > 0) {
            numInHallway--;
            // write to output file if person had to leave temporarily
            writeToOutputFile(outputFile,
                    inHallway[numInHallway].getName() +
                    " had to leave the elevator temporarily");

            // load people back onto the elevator
            stack.push(inHallway[numInHallway]);
        }

        return stack;
    }

    /**
     * Deal with when people come on to the elevator
     *
     * @param stack the stack of people on the elevator
     * @param person the person to put into the stack
     * @param outputFile the path of the output file (.txt)
     *
     * @return the stack of people in the elevator after loading
     */
    public static elevatorStack handlePeopleEntering(elevatorStack stack,
                                                     Person person,
                                                     String outputFile) {
        try {
            stack.push(person);
            writeToOutputFile(outputFile, person.getName() +
            " has entered the elevator, and will depart at floor " +
            person.getDestinationFloor());
        } catch (RuntimeException runtimeException) {
            writeToOutputFile(outputFile, person.getName() +
            " had to take the stairs\n");
        }
        return stack;
    }

    /**
     * Append a line to output
     *
     * @param file the path of the output file
     * @param outputString the line to write to the output file
     */
    public static void writeToOutputFile(String file, String outputString) {
        Writer output;
        try {
            // write the string to the end of the file
            output = new BufferedWriter(new FileWriter(file, true));
            output.append(outputString);
            output.append("\n");
            output.close();
        } catch (Exception exception) {
            // do nothing
        }
    }

    /**
     * Check to see if we need to switch direction of the elevator
     *
     * @param currentGoingUp the current direction of the elevator
     * @param currentFloor the floor the elevator is currently on
     * @param floorRequest1 one request for next floor
     * @param floorRequest2 a second request for next floor
     *
     * @return whether we are going up
     */
    public static boolean checkGoingUp(boolean currentGoingUp, int currentFloor,
                                   int floorRequest1, int floorRequest2)
    {
        if(currentGoingUp) // if we are currently going up
        {
            if(floorRequest1 < currentFloor && floorRequest2 < currentFloor)
            {
                return false; // now going down
            }
            else
            {
                return true; // now going up
            }
        }
        else // if we are going down
        {
            if(floorRequest1 > currentFloor && floorRequest2 > currentFloor)
            {
                return true; // now going up
            }
            else
            {
                return false; // now going down
            }
        }
    }

    /**
     * Check to see if we need to switch direction of the elevator
     *
     * @param currentGoingUp if we are currently going up
     * @param currentFloor the floor the elevator is currently on
     * @param floorRequest the stack of people in the elevator
     *
     * @return whether we are going up
     */
    public static boolean simpleCheckGoingUp(boolean currentGoingUp,
                                             int currentFloor,
                                             int floorRequest)
    {
        if(currentGoingUp) // if we are currently going up
        {
            if(floorRequest < currentFloor)
            {
                return false; // now going down
            }
            else
            {
                return true; // now going up
            }
        }
        else // if we are going down
        {
            if(floorRequest > currentFloor)
            {
                return true; // now going up
            }
            else
            {
                return false; // now going down
            }
        }
    }

    /**
     * Check to see if we need to switch direction of the elevator
     *
     * @param goingUp if the elevator is going up
     * @param currentFloor the floor the elevator is currently on
     * @param floorRequest1 one request for next floor
     * @param floorRequest2 a second request for next floor
     *
     * @return the next floor the elevator will stop at
     */
    public static int getNextFloor(boolean goingUp, int currentFloor,
                            int floorRequest1, int floorRequest2)
    {
        while(currentFloor >= 1 && currentFloor <= 5)
        {
            if (goingUp)
            {
                currentFloor++;
                if (currentFloor == floorRequest1 || currentFloor == floorRequest2)
                {
                    return currentFloor;
                }
            }
            else
            {
                currentFloor--;
                if (currentFloor == floorRequest1 || currentFloor == floorRequest2)
                {
                    return currentFloor;
                }
            }
        }
        return -1; // error code if this function did not complete properly
    }
}