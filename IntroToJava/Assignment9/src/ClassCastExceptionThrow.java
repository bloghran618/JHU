/**
 * This class throws ClassCastException
 *
 * @author Brian Loughran
 */

public class ClassCastExceptionThrow
{
    public static void main(String[] args) {
        try
        {
            // throw an ClassCastException
            throw new ClassCastException("This is a ClassCastException");
        }
        catch (ClassCastException except)
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

