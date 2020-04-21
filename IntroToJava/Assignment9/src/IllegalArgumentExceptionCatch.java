/**
 * This class creates IllegalArgumentException
 *
 * @author Brian Loughran
 */

public class IllegalArgumentExceptionCatch
{
    public static void main(String[] args) {
        try
        {
            // create IllegalArgumentException (found online)
            Character.toChars(-1);
        }
        catch (IllegalArgumentException except)
        {
            // display unique information about the exception
            System.out.println("Class Name: " +
                    except.getStackTrace()[0].getClassName());
            System.out.println("Method Name: " +
                    except.getStackTrace()[0].getMethodName());
        }
    }
}
