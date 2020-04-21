/*
 * This class is the main method which manipulates both animals and vehicles
 */

public class ManipulateAnimals
{
    public static void main(String[] args) {

        // Create length 4 array of AllCapabilitiesObject Interface
        AllCapabilitiesObject[] vehiclesAndAnimals = new AllCapabilitiesObject[4];

        Animal animal1 = new Animal("Puppy");
        Vehicle vehicle1 = new Vehicle("Mazda", 4);
        Animal animal2 = new Animal("Turtle");
        Vehicle vehicle2 = new Vehicle("Toyota", 20);

        vehiclesAndAnimals[0] = animal1;
        vehiclesAndAnimals[1] = vehicle1;
        vehiclesAndAnimals[2] = animal2;
        vehiclesAndAnimals[3] = vehicle2;

        for (int i = 0; i < vehiclesAndAnimals.length; i++)
        {
            vehiclesAndAnimals[i].drawObject();
            vehiclesAndAnimals[i].rotateObject();
            vehiclesAndAnimals[i].resizeObject();
            vehiclesAndAnimals[i].playSound();
            System.out.println();
        }
    }
}
