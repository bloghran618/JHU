/**
 * This class creates ArrayIndexOutOfBounds
 *
 * @author Brian Loughran
 */

public class ArrayIndexOutOfBoundsExceptionCatch
{
    public static void main(String[] args) {
        int[] list = new int[] {1, 2, 3};
        try
        {
            // create ArrayIndexOutOfBoundsException
            System.out.println(list[3]);
        }
        catch (ArrayIndexOutOfBoundsException except)
        {
            // display unique information about the exception
            System.out.println("Class Name: " +
                    except.getStackTrace()[0].getClassName());
            System.out.println("Method Name: " +
                    except.getStackTrace()[0].getMethodName());
        }
    }
}
