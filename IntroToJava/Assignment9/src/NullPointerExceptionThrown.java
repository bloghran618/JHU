/**
 * This class throws NullPointerException
 *
 * @author Brian Loughran
 */

public class NullPointerExceptionThrown
{
    public static void main(String[] args) {
        try
        {
            // throw a NullPointerException
            throw new NullPointerException("This is a NullPointerException");
        }
        catch (NullPointerException except)
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
