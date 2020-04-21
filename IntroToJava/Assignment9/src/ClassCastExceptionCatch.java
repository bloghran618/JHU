/**
 * This class creates ClassCastException
 *
 * @author Brian Loughran
 */

public class ClassCastExceptionCatch
{
    public static void main(String[] args) {
        Object i = Integer.valueOf(42);
        try
        {
            // create a ClassCastException
            String string = (String)i;
        }
        catch (ClassCastException except)
        {
            // display unique information about the exception
            System.out.println("Class Name: " +
                    except.getStackTrace()[0].getClassName());
            System.out.println("Method Name: " +
                    except.getStackTrace()[0].getMethodName());
        }
    }
}

