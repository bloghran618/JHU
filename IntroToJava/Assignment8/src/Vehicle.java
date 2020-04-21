/*
 / Vehicle class defines an vehicle which extends an AllCapabilitiesObject
 */

public class Vehicle implements AllCapabilitiesObject
{
    private String name;
    private int age;

    public Vehicle(String name, int age)
    {
        if (name != "")
        {
            this.name = name;
        }
        else
        {
            throw new RuntimeException("Vehicle must have non-blank name");
        }

        if (age >= 0)
        {
            this.age = age;
        }
        else
        {
            throw new RuntimeException("Vehicle age must be positive");
        }
    }

    public void setName(String name)
    {
        this.name = name;
    }

    public String getName()
    {
        return this.name;
    }

    public void setAge(int age)
    {
        this.age = age;
    }

    public int getAge()
    {
        return this.age;
    }

    public void drawObject()
    {
        System.out.println("Drawing a Vehicle");
    }

    public void rotateObject()
    {
        System.out.println("Rotating a Vehicle");
    }

    public void resizeObject()
    {
        System.out.println("Resizing a Vehicle");
    }

    public void playSound()
    {
        System.out.println("Vehicle sound");
    }
}
