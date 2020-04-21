/**
 * This class throws ArrayIndexOutOfBoundsException
 *
 * @author Brian Loughran
 */

public class ArrayIndexOutOfBoundsExceptionThrow
{
    public static void main(String[] args) {
        try
        {
            // throw ArrayIndexOutOfBoundsException
            throw new ArrayIndexOutOfBoundsException("Array out of bounds");
        }
        catch (ArrayIndexOutOfBoundsException except)
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