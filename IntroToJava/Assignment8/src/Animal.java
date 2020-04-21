/*
 / Animal class defines an animal which extends an AllCapabilitiesObject
 */

public class Animal implements AllCapabilitiesObject
{
    private String name;

    public Animal(String name)
    {
        if (name != "")
        {
            this.name = name;
        }
        else
        {
            throw new RuntimeException("Animal must have non-blank name");
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

    public void drawObject()
    {
        System.out.println("Drawing an Animal");
    }

    public void rotateObject()
    {
        System.out.println("Rotating an Animal");
    }

    public void resizeObject()
    {
        System.out.println("Resizing an Animal");
    }

    public void playSound()
    {
        System.out.println("Animal sound");
    }
}
