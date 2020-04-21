/**
 * This class creates NullPointerException
 *
 * @author Brian Loughran
 */

public class NullPointerExceptionCatch
{
    public static void main(String[] args) {
        String pointer = null;
        try
        {
            if (pointer.equals("string"))
            {
                // throw a NullPointerException
                System.out.println("Will never get executed!");
            }
        }
        catch (NullPointerException except)
        {
            // display unique information about the exception
            System.out.println("Class Name: " +
                    except.getStackTrace()[0].getClassName());
            System.out.println("Method Name: " +
                    except.getStackTrace()[0].getMethodName());
        }
    }
}
