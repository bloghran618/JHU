/**
 * This class throws IllegalArgumentException
 *
 * @author Brian Loughran
 */

public class IllegalArgumentExceptionThrow
{
    public static void main(String[] args) {
        try
        {
            // throw IllegalArgumentException
            throw new IllegalArgumentException("This is an IllegalArgumentException");
        }
        catch (IllegalArgumentException except)
        {
            // display unique information about the exception
            System.out.println("Exception: " + except.getMessage());
            System.out.println("Class Name: " +
                    except.getStackTrace()[0].getClassName());
            System.out.println("Method Name: " +
                    except.getStackTrace()[0].getMethodName());
        }
    }
}