/*
 * A single node in a linked list
 */

public class Node
{
    private Node next;
    private int val;

    /**
     * Initializer for object of type Node
     *
     * @param value the value of the node
     */
    Node(int value)
    {
        if(value < 0)
        {
            throw new RuntimeException("Value must be positive");
        }
        else
        {
            this.next = null;
            this.val = value;
        }
    }

    /**
     * get the value of the node
     *
     * @return the value
     */
    public int getVal()
    {
        return this.val;
    }

    /**
     * Sets the value of the node
     *
     * @param value the value of the node
     */
    public void setVal(int value)
    {
        this.val = value;
    }

    /**
     * get the next Node in the linked list
     *
     * @return the next Node
     */
    public Node getNext()
    {
        return next;
    }

    /**
     * Sets the next Node in the linked list
     *
     * @param next the next Node
     */
    public void setNext(Node next)
    {
        this.next = next;
    }
}
